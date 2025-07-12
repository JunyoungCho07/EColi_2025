import os
from PIL import Image

# 입력 및 출력 디렉터리 설정
input_dir = "raw_image"
output_dir = "raw_image_cropped_256"
os.makedirs(output_dir, exist_ok=True)

# 지원할 확장자
exts = (".png", ".jpg", ".jpeg", ".bmp", ".tiff")

for fname in os.listdir(input_dir):
    if not fname.lower().endswith(exts):
        continue

    # 이미지 열기
    img_path = os.path.join(input_dir, fname)
    img = Image.open(img_path)

    # 중앙 정사각형 crop 계산
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    right = left + side
    bottom = top + side

    cropped = img.crop((left, top, right, bottom))

    # 256x256으로 resize
    resized = cropped.resize((256, 256), Image.LANCZOS)

    # 결과 저장
    out_path = os.path.join(output_dir, fname)
    resized.save(out_path)
    print(f"Processed and saved: {out_path}")

print("All images processed!")
