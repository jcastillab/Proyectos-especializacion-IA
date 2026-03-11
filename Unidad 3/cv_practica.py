import argparse, os, sys
import numpy as np
import cv2
from skimage import img_as_ubyte
from skimage.filters import gaussian, threshold_otsu, threshold_local

def ensure_out(out_dir):
    os.makedirs(out_dir, exist_ok=True)

def read_image(path):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        sys.exit(f"[ERROR] No pude leer la imagen: {path}")
    return img

def save(path, img):
    ok = cv2.imwrite(path, img)
    if not ok:
        sys.exit(f"[ERROR] No pude guardar: {path}")

def center_crop(img, size=200):
    h, w = img.shape[:2]
    ch, cw = size, size
    y1 = max(0, h//2 - ch//2); y2 = y1 + ch
    x1 = max(0, w//2 - cw//2); x2 = x1 + cw
    return img[y1:y2, x1:x2].copy()

def rotate(img, angle=45):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)
    return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT101)

def kmeans_segment(bgr, K=3, attempts=10):
    Z = bgr.reshape((-1, 3)).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    ret, labels, centers = cv2.kmeans(Z, K, None, criteria, attempts, cv2.KMEANS_PP_CENTERS)
    centers = np.uint8(centers)
    seg = centers[labels.flatten()].reshape(bgr.shape)
    return seg

def main():
    ap = argparse.ArgumentParser(description="Práctica OpenCV + Scikit-Image")
    ap.add_argument("--image", required=True, help="Ruta a la imagen de entrada")
    ap.add_argument("--out", default="outputs", help="Carpeta de salida")
    ap.add_argument("--roi", type=int, default=200, help="Tamaño del recorte centrado (px)")
    args = ap.parse_args()

    ensure_out(args.out)
    base = os.path.splitext(os.path.basename(args.image))[0]

    # 1) Leer y mostrar/guardar básico
    bgr = read_image(args.image)
    save(os.path.join(args.out, f"{base}_01_original.png"), bgr)

    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    save(os.path.join(args.out, f"{base}_02_gris.png"), gray)

    # 2) Transformaciones geométricas
    resized = cv2.resize(bgr, (200, 200), interpolation=cv2.INTER_AREA)
    save(os.path.join(args.out, f"{base}_03_redimension_200x200.png"), resized)

    rotated = rotate(bgr, 45)
    save(os.path.join(args.out, f"{base}_04_rotada_45.png"), rotated)

    cropped = center_crop(bgr, args.roi)
    save(os.path.join(args.out, f"{base}_05_crop_centro_{args.roi}px.png"), cropped)

    # 3) Filtros y transformaciones
    # Suavizado con Scikit-Image (gaussian trabaja en float [0..1])
    bgr_float = bgr[:, :, ::-1] / 255.0  
    blurred = gaussian(bgr_float, sigma=1.0, channel_axis=2)
    blurred_u8 = img_as_ubyte(blurred[:, :, ::-1])  # volver a BGR uint8
    save(os.path.join(args.out, f"{base}_06_suavizado_gauss.png"), blurred_u8)

    # Bordes Canny sobre gris
    edges = cv2.Canny(gray, 100, 200, L2gradient=True)
    save(os.path.join(args.out, f"{base}_07_bordes_canny.png"), edges)

    # 4) Detección de objetos (caras con Haar)
    face_xml = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
    if not os.path.exists(face_xml):
        sys.exit("[ERROR] No se encontró haarcascade_frontalface_default.xml")
    face_cascade = cv2.CascadeClassifier(face_xml)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
    faces_img = bgr.copy()
    for (x, y, w, h) in faces:
        cv2.rectangle(faces_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    save(os.path.join(args.out, f"{base}_08_caras_haar.png"), faces_img)

    # 5) Segmentación
    # 5.1 Umbralización global (Otsu) con skimage
    t_otsu = threshold_otsu(gray)
    bin_otsu = (gray >= t_otsu).astype(np.uint8) * 255
    save(os.path.join(args.out, f"{base}_09_otsu.png"), bin_otsu)

    # 5.2 Umbralización adaptativa (binarización local)
    # Con OpenCV (bloques 35x35, C=5)
    adapt = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 35, 5)
    save(os.path.join(args.out, f"{base}_10_adaptativa.png"), adapt)

    # Alternativa con scikit-image
    block_size = 35
    local_thresh = threshold_local(gray, block_size=block_size, offset=5)
    bin_local = (gray > local_thresh).astype(np.uint8) * 255
    save(os.path.join(args.out, f"{base}_10b_adaptativa_sk.png"), bin_local)

    # 5.3 Segmentación por K-Means (K=3)
    seg = kmeans_segment(bgr, K=3)
    save(os.path.join(args.out, f"{base}_11_kmeans_K3.png"), seg)

    print("[OK] Listo. Archivos generados en:", os.path.abspath(args.out))
    print("Caras detectadas:", len(faces))

if __name__ == "__main__":
    main()
