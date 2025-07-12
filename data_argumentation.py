import os
from PIL import Image

# 설정: 입력 및 출력 디렉터리
input_img_dir = "dataset/images/train"
input_mask_dir = "dataset/masks/train"
output_img_dir = "dataset/images_aug"
output_mask_dir = "dataset/masks_aug"
os.makedirs(output_img_dir, exist_ok=True)
os.makedirs(output_mask_dir, exist_ok=True)

# 지원 확장자
exts = (".png", ".jpg", ".jpeg", ".bmp", ".tiff")

# 뒤집기 옵션: (name, function to apply)
flip_ops = [
    ("orig", lambda img: img),
    ("h", lambda img: img.transpose(Image.FLIP_LEFT_RIGHT)),
    ("v", lambda img: img.transpose(Image.FLIP_TOP_BOTTOM)),
    ("hv", lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM))
]

# 각 이미지마다 16개 증강 생성
for idx, fname in enumerate(sorted(os.listdir(input_img_dir)), start=1):
    if not fname.lower().endswith(exts):
        continue
    base_idx = f"{idx:04d}"  # 0001, 0002, ...
    
    img_path = os.path.join(input_img_dir, fname)
    mask_path = os.path.join(input_mask_dir, fname)
    
    img = Image.open(img_path)
    mask = Image.open(mask_path)
    
    aug_count = 1
    for flip_name, flip_fn in flip_ops:
        flipped_img = flip_fn(img)
        flipped_mask = flip_fn(mask)
        for rot_k in range(4):
            angle = rot_k * 90
            # 회전 (256x256 정사각이므로 expand=False)
            aug_img = flipped_img.rotate(angle)
            aug_mask = flipped_mask.rotate(angle)
            
            # 파일명: image_0001(1).png, mask_0001(1).png
            img_out_name = f"image_{base_idx}({aug_count}).png"
            mask_out_name = f"mask_{base_idx}({aug_count}).png"
            
            aug_img.save(os.path.join(output_img_dir, img_out_name))
            aug_mask.save(os.path.join(output_mask_dir, mask_out_name))
            
            aug_count += 1

print("Data augmentation complete! Generated 16 variants per original image.")
