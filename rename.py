import os
import shutil

def rename_and_copy_separate(
    imgs_src_folder,
    txts_src_folder,
    dst_root_folder
):
    # 출력 폴더 경로 설정
    imgs_dst = os.path.join(dst_root_folder, "images", "train")
    txts_dst = os.path.join(dst_root_folder, "labels", "train")

    # 폴더 생성
    os.makedirs(imgs_dst, exist_ok=True)
    os.makedirs(txts_dst, exist_ok=True)

    # 파일 목록 수집 및 정렬
    images = sorted(
        f for f in os.listdir(imgs_src_folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    )
    txts = sorted(
        f for f in os.listdir(txts_src_folder)
        if f.lower().endswith('.txt')
    )

    # 개수 검증
    if len(images) != len(txts):
        raise ValueError(
            f"파일 개수 불일치: 이미지 {len(images)}개, TXT {len(txts)}개"
        )

    # 복사 및 이름 변경
    for i, (img_name, txt_name) in enumerate(zip(images, txts), start=1):
        base = f"image_{i:04d}"
        # 이미지 복사
        img_ext = os.path.splitext(img_name)[1]
        shutil.copy(
            os.path.join(imgs_src_folder, img_name),
            os.path.join(imgs_dst, base + img_ext)
        )
        # TXT 복사
        shutil.copy(
            os.path.join(txts_src_folder, txt_name),
            os.path.join(txts_dst, base + '.txt')
        )

    print(f"완료: {imgs_dst}에 이미지 {len(images)}개,")
    print(f"      {txts_dst}에 TXT  {len(txts)}개 저장됨")

if __name__ == "__main__":
    # ★ 여기를 실제 경로로 바꿔주세요.
    imgs_src = "path/to/original/images"
    txts_src = "path/to/original/labels"
    dst_root = "path/to/renamed_dataset"

    rename_and_copy_separate(imgs_src, txts_src, dst_root)
