"""
Operaciones básicas para el taller de Visión Computacional U1.
Cada función hace una sola cosa y maneja errores simples.
"""
from typing import Tuple
from pathlib import Path
import cv2
import numpy as np

def leer_imagen(ruta: Path):
    """Lee una imagen con OpenCV. Lanza FileNotFoundError si falla."""
    img = cv2.imread(str(ruta))
    if img is None:
        raise FileNotFoundError(f"No se pudo leer la imagen en {ruta}")
    return img

def a_grises(img_bgr):
    """Convierte BGR a escala de grises."""
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

def blur_gauss(img_gray, k=5, sigma=1.0):
    k = int(k)
    """Aplica desenfoque Gaussiano. Asegura que k sea impar."""
    if k % 2 == 0:
        k += 1
    return cv2.GaussianBlur(img_gray, (k, k), sigmaX=sigma)

def canny(edges_in, t1=100, t2=200):
    """Detecta bordes con Canny usando dos umbrales."""
    return cv2.Canny(edges_in, threshold1=int(t1), threshold2=int(t2))

def guardar(path: Path, mat) -> None:
    """Guarda una matriz de imagen en disco. Crea carpetas si no existen."""
    path.parent.mkdir(parents=True, exist_ok=True)
    ok = cv2.imwrite(str(path), mat)
    if not ok:
        raise IOError(f"No se pudo escribir {path}")

def info(img):
    """Devuelve ancho, alto, canales y tipo de dato."""
    h, w = img.shape[:2]
    c = 1 if len(img.shape) == 2 else img.shape[2]
    return {"ancho": w, "alto": h, "canales": c, "dtype": str(img.dtype)}

def resize_fit(img, max_w=1280, max_h=900):
    """Redimensiona manteniendo proporción para que quepa en max_w x max_h."""
    h, w = img.shape[:2]
    scale = min(max_w / w, max_h / h, 1.0)
    if scale < 1.0:
        new_w, new_h = int(w * scale), int(h * scale)
        return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return img