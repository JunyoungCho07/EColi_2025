# import os
# import pyheif
# from PIL import Image

# def convert_heic_to_png(input_path, output_path, size=(1024, 1024)):
#     heif_file = pyheif.read(input_path)
#     image = Image.frombytes(
#         heif_file.mode,
#         heif_file.size,
#         heif_file.data,
#         "raw",
#         heif_file.mode,
#         heif_file.stride,
#     )
#     image = image.resize(size, Image.LANCZOS)
#     image.save(output_path, format="PNG")
#     print(f"Converted: {input_path} -> {output_path}")

# def batch_convert(folder_path, output_folder="output_pngs", size=(1024, 1024)):
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     for filename in os.listdir(folder_path):
#         if filename.lower().endswith(".heic"):
#             input_path = os.path.join(folder_path, filename)
#             base_name = os.path.splitext(filename)[0]
#             output_path = os.path.join(output_folder, f"{base_name}.png")
#             try:
#                 convert_heic_to_png(input_path, output_path, size)
#             except Exception as e:
#                 print(f"Failed to convert {filename}: {e}")

# if __name__ == "__main__":
#     folder = "heic_images"  # HEIC 파일이 들어 있는 폴더 이름
#     batch_convert(folder)

import os
from PIL import Image

# 입력 및 출력 디렉터리 설정
input_dir = "raw_image"  # 원본 이미지 폴더명에 맞게 수정하세요
output_dir = "raw_image_cropped_256"
os.makedirs(output_dir, exist_ok=True)

# 지원할 확장자
exts = (".png", ".jpg", ".jpeg", ".bmp", ".tiff")

# 파일 리스트 정렬 후 순차 처리
files = sorted([f for f in os.listdir(input_dir) if f.lower().endswith(exts)])
counter = 1

for fname in files:
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
    resized = cropped.resize((1024, 1024), Image.LANCZOS)

    # 새로운 파일명 생성 (image_0001.png, image_0002.png, ...)
    new_name = f"image_{counter:04d}.png"
    out_path = os.path.join(output_dir, new_name)

    # 결과 저장
    resized.save(out_path)
    print(f"Processed {fname} -> {new_name}")

    counter += 1

print("All images processed and renamed!")
