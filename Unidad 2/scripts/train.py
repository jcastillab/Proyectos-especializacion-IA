from ultralytics import YOLO
import torch, os

def main():
    device = 0 if torch.cuda.is_available() else "cpu"
    model = YOLO("yolov8n.pt")  
    model.train(
        data="cfg/data.yaml",
        epochs=50,
        imgsz=640,
        batch=1,
        device=device,
        workers=4,
        project="runs",
        name="train"
    )

if __name__ == "__main__":
    main()
