from ultralytics import YOLO
import torch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/"images_new"
OUT = ROOT/"runs/predict"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    device = 0 if torch.cuda.is_available() else "cpu"
    model = YOLO("runs/detect/train/weights/best.pt")
    results = model.predict(source=str(SRC), device=device, imgsz=640, save=True, project=str(OUT), name="latest")
    print("Resultados en", OUT/"latest")

if __name__ == "__main__":
    main()
