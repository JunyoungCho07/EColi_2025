import os

# 1) 이미지가 있는 폴더 경로
imgs_dir = "path/to/your/dataset/images/train"

# 2) train.txt 열기(덮어쓰기 모드)
with open("train.txt", "w", encoding="utf-8") as f:
    # 3) 확장자별로 정렬해서 한 줄씩 기록
    for img in sorted(os.listdir(imgs_dir)):
        if img.lower().endswith(('.jpg', '.jpeg', '.png')):
            # (a) 절대 경로를 쓸 경우: os.path.abspath(...)
            # (b) 상대 경로를 쓸 경우:
            rel_path = os.path.join("images", "train", img)
            f.write(rel_path.replace("\\", "/") + "\n")

print("▶ train.txt 생성 완료!")
