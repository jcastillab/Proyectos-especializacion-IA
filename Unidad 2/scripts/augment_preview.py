import cv2, random
from pathlib import Path
import albumentations as A
from albumentations.pytorch import ToTensorV2

ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT/"data/yolo/train/images"
OUT_DIR = ROOT/"data/yolo/_aug_preview"
OUT_DIR.mkdir(parents=True, exist_ok=True)

aug = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.5),
    A.MotionBlur(blur_limit=5, p=0.2),
    A.Affine(scale=(0.9, 1.1), translate_percent=(0.0, 0.05), rotate=(-10, 10), p=0.3)
])

def main():
    imgs = list(IMG_DIR.glob("*.jpg"))
    random.shuffle(imgs)
    for i, imgp in enumerate(imgs[:20]):
        img = cv2.imread(str(imgp))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        aug_img = aug(image=img)["image"]
        aug_img = cv2.cvtColor(aug_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(OUT_DIR/f"aug_{i:03d}.jpg"), aug_img)
    print("Aumentos de muestra guardados en", OUT_DIR)

if __name__ == "__main__":
    main()
