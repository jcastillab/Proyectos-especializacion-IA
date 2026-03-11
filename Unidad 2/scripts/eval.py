from ultralytics import YOLO
import torch

def main():
    device = 0 if torch.cuda.is_available() else "cpu"
    model = YOLO("runs/detect/train/weights/best.pt")
    metrics = model.val(data="cfg/data.yaml", imgsz=640, device=device)
    print(metrics)

if __name__ == "__main__":
    main()
