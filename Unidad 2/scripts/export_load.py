from ultralytics import YOLO

def main():
    model = YOLO("runs/detect/train/weights/best.pt")
    model.export(format="onnx", dynamic=True)
    print("Export ONNX listo")

    loaded = YOLO("runs/detect/train/weights/best.onnx")
    r = loaded.predict(source="images_new", imgsz=640)
    print("Inferencia con ONNX lista")

if __name__ == "__main__":
    main()
