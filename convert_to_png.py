# convert_to_png.py
from PIL import Image
import os

# 1) 변환할 원본 이미지들이 들어있는 폴더 경로
input_dir = "raw_images"        

# 2) 변환된 PNG를 저장할 폴더 경로 (없으면 자동 생성)
output_dir = "raw_images_png"
os.makedirs(output_dir, exist_ok=True)

# 3) 지원할 확장자 리스트
exts = (".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".gif")

for fname in os.listdir(input_dir):
    if not fname.lower().endswith(exts):
        continue
    src_path = os.path.join(input_dir, fname)
    img = Image.open(src_path)
    base = os.path.splitext(fname)[0]
    dst_path = os.path.join(output_dir, base + ".png")
    # PNG로 저장 (투명도 유지 가능)
    img.save(dst_path, format="PNG")
    print(f"{fname} → {base}.png 변환 완료")

print("모든 이미지 변환 완료!")
