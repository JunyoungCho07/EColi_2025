import os, shutil, random
from glob import glob

def split_dataset(
    imgs_src, labels_src, dst_root, val_ratio=0.2, seed=42
):
    random.seed(seed)
    imgs = sorted(glob(os.path.join(imgs_src, '*.*')))
    random.shuffle(imgs)
    n_val = int(len(imgs) * val_ratio)
    splits = {
        'val': imgs[:n_val],
        'train': imgs[n_val:]
    }

    for subset, files in splits.items():
        img_dst = os.path.join(dst_root, 'images', subset)
        lbl_dst = os.path.join(dst_root, 'labels', subset)
        os.makedirs(img_dst, exist_ok=True)
        os.makedirs(lbl_dst, exist_ok=True)

        for img_path in files:
            name, ext = os.path.splitext(os.path.basename(img_path))
            txt_path = os.path.join(labels_src, name + '.txt')
            shutil.copy(img_path, os.path.join(img_dst, name + ext))
            if os.path.exists(txt_path):
                shutil.copy(txt_path, os.path.join(lbl_dst, name + '.txt'))
            else:
                print(f'Warning: {name}.txt not found')

if __name__ == '__main__':
    # ★ 경로와 val 비율(val_ratio)을 필요에 맞게 수정하세요
    split_dataset(
        imgs_src='renamed_arg/images',
        labels_src='renamed_arg/labels',
        dst_root='renamed_arg',
        val_ratio=0.2
    )
    print('Dataset split complete.')
