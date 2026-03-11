from pathlib import Path
import urllib.request, zipfile, shutil

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "yolo"

URL = "https://ultralytics.com/assets/coco128.zip"
ZIP_PATH = RAW / "coco128.zip"

def download(url: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        print(f"[INFO] Ya existe: {dest}")
        return
    print(f"[INFO] Bajando {url}")
    urllib.request.urlretrieve(url, dest)

def unzip(zippath: Path, dest: Path):
    print(f"[INFO] Descomprimiendo {zippath.name} en {dest}")
    with zipfile.ZipFile(zippath, "r") as zf:
        zf.extractall(dest)

def images_present() -> bool:
    train = OUT / "train" / "images"
    val = OUT / "val" / "images"
    return train.exists() and any(train.glob("*")) and val.exists() and any(val.glob("*"))

def prepare():
    tmp_dir = RAW / "coco128_tmp"
    if images_present():
        print(f"[INFO] Dataset mini ya presente en {OUT}")
        return

    tmp_dir.mkdir(parents=True, exist_ok=True)
    unzip(ZIP_PATH, tmp_dir)

    # El zip trae 'coco128/images/{train,val}' y 'coco128/labels/{train,val}'
    src = tmp_dir / "coco128"
    if not src.exists():
        raise RuntimeError(f"No se encontró carpeta esperada: {src}")

    for split in ["train", "val"]:
        img_src = src / "images" / split
        lbl_src = src / "labels" / split

        img_dst = OUT / split / "images"
        lbl_dst = OUT / split / "labels"
        img_dst.mkdir(parents=True, exist_ok=True)
        lbl_dst.mkdir(parents=True, exist_ok=True)

        copied_imgs = 0
        for p in img_src.glob("*"):
            shutil.copy2(p, img_dst / p.name)
            copied_imgs += 1

        copied_lbls = 0
        for p in lbl_src.glob("*.txt"):
            shutil.copy2(p, lbl_dst / p.name)
            copied_lbls += 1

        print(f"[OK] {split}: {copied_imgs} imágenes, {copied_lbls} etiquetas")

    # Limpieza temporal
    try:
        shutil.rmtree(tmp_dir)
        print(f"[INFO] Limpieza temporal ok: {tmp_dir}")
    except Exception as e:
        print(f"[WARN] No se pudo borrar temporal: {e}")

def main():
    download(URL, ZIP_PATH)
    prepare()
    print(f"[DONE] Mini COCO listo en {OUT}")

if __name__ == "__main__":
    main()