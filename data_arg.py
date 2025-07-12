import os
import cv2
import numpy as np

def load_poly(txt_path, img_w, img_h):
    polys = []
    with open(txt_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            cls = parts[0]
            coords = list(map(float, parts[1:]))
            # normalized → absolute
            pts = [(coords[i]*img_w, coords[i+1]*img_h)
                   for i in range(0, len(coords), 2)]
            polys.append((cls, np.array(pts, dtype=np.float32)))
    return polys

def save_poly(polys, save_path, out_w, out_h):
    with open(save_path, 'w') as f:
        for cls, pts in polys:
            # absolute → normalized
            norm = []
            for x,y in pts:
                norm += [x / out_w, y / out_h]
            line = ' '.join([cls] + [f"{v:.6f}" for v in norm])
            f.write(line + '\n')

def augment_image_and_poly(img, polys, angle, flip_h, flip_v):
    h, w = img.shape[:2]
    # 1) 회전
    M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)
    cos, sin = abs(M[0,0]), abs(M[0,1])
    # 회전 후 이미지 크기 계산
    nw = int(h * sin + w * cos)
    nh = int(h * cos + w * sin)
    M[0,2] += (nw/2 - w/2)
    M[1,2] += (nh/2 - h/2)
    img = cv2.warpAffine(img, M, (nw, nh), flags=cv2.INTER_LINEAR)
    new_polys = []
    for cls, pts in polys:
        # pts: Nx2
        ones = np.ones((pts.shape[0],1))
        pts_h = np.hstack([pts, ones])            # Nx3
        pts_rot = (M @ pts_h.T).T                # Nx2
        new_polys.append((cls, pts_rot))
    # 2) 플립
    if flip_h:
        img = cv2.flip(img, 1)
        for i,(cls, pts) in enumerate(new_polys):
            pts[:,0] = nw - pts[:,0]
            new_polys[i] = (cls, pts)
    if flip_v:
        img = cv2.flip(img, 0)
        for i,(cls, pts) in enumerate(new_polys):
            pts[:,1] = nh - pts[:,1]
            new_polys[i] = (cls, pts)
    return img, new_polys

def batch_augment(
    imgs_src, txts_src, dst_root
):
    imgs_dst = os.path.join(dst_root, "images")
    txts_dst = os.path.join(dst_root, "labels")
    os.makedirs(imgs_dst, exist_ok=True)
    os.makedirs(txts_dst, exist_ok=True)

    img_files = sorted([f for f in os.listdir(imgs_src)
                        if f.lower().endswith(('.png','.jpg','.jpeg'))])
    for fname in img_files:
        name, ext = os.path.splitext(fname)
        img_path = os.path.join(imgs_src, fname)
        txt_path = os.path.join(txts_src, name + '.txt')
        if not os.path.exists(txt_path):
            print(f"Annotation missing for {fname}, skip.")
            continue

        img = cv2.imread(img_path)
        h, w = img.shape[:2]
        polys = load_poly(txt_path, w, h)

        for angle in [0, 90, 180, 270]:
            for flip_h in (False, True):
                for flip_v in (False, True):
                    aug_img, aug_polys = augment_image_and_poly(
                        img.copy(), polys, angle, flip_h, flip_v
                    )
                    suffix = f"_r{angle}"
                    if flip_h: suffix += "_fh"
                    if flip_v: suffix += "_fv"

                    new_name = f"{name}{suffix}"
                    out_img_path = os.path.join(imgs_dst, new_name + ext)
                    out_txt_path = os.path.join(txts_dst, new_name + '.txt')

                    cv2.imwrite(out_img_path, aug_img)
                    save_poly(aug_polys, out_txt_path,
                              aug_img.shape[1], aug_img.shape[0])

    print("증강 완료!")

if __name__ == "__main__":
    batch_augment(
        imgs_src="renamed/images/train",
        txts_src="renamed/labels/train",
        dst_root="renamed_arg"
    )
