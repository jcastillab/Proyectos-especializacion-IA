import json, os, shutil
from pathlib import Path
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT/"data/raw"
OUT = ROOT/"data/yolo"

SPLITS = {
    "train": {
        "img_dir": RAW/"train2017",
        "ann_file": RAW/"annotations"/"instances_train2017.json"
    },
    "val": {
        "img_dir": RAW/"val2017",
        "ann_file": RAW/"annotations"/"instances_val2017.json"
    }
}

def coco_to_yolo_bbox(bbox, w, h):
    x, y, bw, bh = bbox
    xc = x + bw/2
    yc = y + bh/2
    return [xc/w, yc/h, bw/w, bh/h]

def build_index(coco):
    imgs = {img["id"]: img for img in coco["images"]}
    cats = {cat["id"]: cat for cat in coco["categories"]}
    ann_by_img = {img_id: [] for img_id in imgs.keys()}
    for ann in coco["annotations"]:
        if ann.get("iscrowd", 0) == 1:
            continue
        ann_by_img[ann["image_id"]].append(ann)
    catid2yolo = {}
    for i, cat in enumerate(sorted(cats.values(), key=lambda c: c["id"])):
        catid2yolo[cat["id"]] = i
    return imgs, catid2yolo, ann_by_img

def convert_split(split, spec):
    img_dir = spec["img_dir"]
    ann_file = spec["ann_file"]

    with open(ann_file, "r") as f:
        coco = json.load(f)

    imgs, catid2yolo, ann_by_img = build_index(coco)

    img_out = OUT/split/"images"
    lbl_out = OUT/split/"labels"
    img_out.mkdir(parents=True, exist_ok=True)
    lbl_out.mkdir(parents=True, exist_ok=True)

    for img_id, img in tqdm(imgs.items(), desc=f"Procesando {split}"):
        src = img_dir/ img["file_name"]
        if not src.exists():
            continue
        dst = img_out/ img["file_name"]
        if not dst.exists():
            shutil.copy2(src, dst)

        anns = ann_by_img.get(img_id, [])
        if not anns:
            # archivo de etiqueta vacío para mantener consistencia
            open(lbl_out/(Path(img["file_name"]).stem + ".txt"), "w").close()
            continue

        w, h = img["width"], img["height"]
        lines = []
        for a in anns:
            cat_id = a["category_id"]
            if cat_id not in catid2yolo:
                continue
            yolo_id = catid2yolo[cat_id]
            bb = coco_to_yolo_bbox(a["bbox"], w, h)
            bb = [max(min(v, 1.0), 0.0) for v in bb]
            lines.append(f"{yolo_id} " + " ".join(f"{v:.6f}" for v in bb))
        with open(lbl_out/(Path(img["file_name"]).stem + ".txt"), "w") as f:
            f.write("\n".join(lines))

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for split, spec in SPLITS.items():
        convert_split(split, spec)
    print("Conversión lista")

if __name__ == "__main__":
    main()
