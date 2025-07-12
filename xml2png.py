import os
import xml.etree.ElementTree as ET
import cv2
import numpy as np

def xml_to_masks(xml_path, output_dir, class_to_id):
    """
    CVAT XML 어노테이션을 읽어 이미지를 기준으로 폴리곤을 그려
    픽셀 단위 마스크 PNG로 저장합니다.

    xml_path: CVAT XML 파일 경로
    output_dir: 마스크 PNG를 저장할 폴더
    class_to_id: {'Colony':1, 'InhibitionZone':2} 등 클래스별 ID 매핑
    """
    os.makedirs(output_dir, exist_ok=True)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for image in root.findall('image'):
        name = image.get('name')         # 원본 이미지 파일명
        width = int(image.get('width'))
        height = int(image.get('height'))

        mask = np.zeros((height, width), dtype=np.uint8)

        # 폴리곤 태그 처리
        for poly in image.findall('polygon'):
            label = poly.get('label')
            pts = []
            for xy in poly.get('points').split(';'):
                x, y = map(float, xy.split(','))
                pts.append([int(x), int(y)])
            pts = np.array([pts], dtype=np.int32)
            cv2.fillPoly(mask, pts, color=class_to_id[label])

        # 박스 태그 처리 (필요시)
        for box in image.findall('box'):
            label = box.get('label')
            xtl = int(float(box.get('xtl')))
            ytl = int(float(box.get('ytl')))
            xbr = int(float(box.get('xbr')))
            ybr = int(float(box.get('ybr')))
            cv2.rectangle(mask, (xtl, ytl), (xbr, ybr), color=class_to_id[label], thickness=-1)

        out_path = os.path.join(output_dir, os.path.splitext(name)[0] + "_mask.png")
        cv2.imwrite(out_path, mask)
        print(f"Saved mask: {out_path}")

# 사용 예시
if __name__ == "__main__":
    xml_file = "annotations.xml"  # CVAT XML 파일 경로
    out_folder = "masks_png"      # 저장할 폴더
    class_ids = {"Colony": 1, "InhibitionZone": 2}

    xml_to_masks(xml_file, out_folder, class_ids)

