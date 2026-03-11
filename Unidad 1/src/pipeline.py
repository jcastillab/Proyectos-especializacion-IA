"""
CLI del pipeline: grises, Gauss, Canny y extras opcionales.
Usa ops.py y guarda cada salida en data/out.
"""

import argparse
from pathlib import Path
# Importa funciones utilitarias del módulo ops
from ops import leer_imagen, a_grises, blur_gauss, canny, guardar, info, resize_fit
import cv2

def parse_args():
    """Define y parsea los argumentos de línea de comandos."""
    p = argparse.ArgumentParser(description="Taller CV U1. Grises, Gauss, Canny.")
    raiz = Path(__file__).resolve().parents[1]
    p.add_argument("--input", "-i", type=str, default=str(raiz / "data" / "entrada.jpg"))
    p.add_argument("--outdir", "-o", type=str, default=str(raiz / "data" / "out"))
    p.add_argument("--k", type=int, default=5)
    p.add_argument("--sigma", type=float, default=1.0)
    p.add_argument("--t1", type=int, default=100)
    p.add_argument("--t2", type=int, default=200)
    p.add_argument("--show", action="store_true")
    p.add_argument("--fitw", type=int, default=1280, help="Ancho máximo al mostrar")
    p.add_argument("--fith", type=int, default=900, help="Alto máximo al mostrar")
    return p.parse_args()


def mostrar(titulo, img, enable, fitw, fith):
    """Muestra una imagen redimensionada para visualización controlada."""
    if not enable:
        return
    vis = resize_fit(img, max_w=fitw, max_h=fith)
    h, w = vis.shape[:2]
    print(f"Mostrando {titulo} en {w}x{h}")
    cv2.namedWindow(titulo, cv2.WINDOW_NORMAL)
    cv2.imshow(titulo, vis)
    cv2.resizeWindow(titulo, w, h) 
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    """Flujo completo: leer, grises, blur, canny y extras opcionales."""
    args = parse_args()
    ruta = Path(args.input)
    outdir = Path(args.outdir)

    # 1. Leer
    bgr = leer_imagen(ruta)
    print("INFO:", info(bgr))
    mostrar("Original", bgr, args.show, args.fitw, args.fith)

    # 2. Grises
    gray = a_grises(bgr)
    mostrar("Grises", gray, args.show, args.fitw, args.fith)
    guardar(outdir / "salida_grises.png", gray)

    # 3. Blur Gauss
    blur = blur_gauss(gray, k=args.k, sigma=args.sigma)
    mostrar("Blur Gauss", blur, args.show, args.fitw, args.fith)
    guardar(outdir / "salida_blur.png", blur)

    # 4. Canny
    edges = canny(blur, t1=args.t1, t2=args.t2)
    mostrar("Bordes Canny", edges, args.show, args.fitw, args.fith)
    guardar(outdir / "salida_bordes.png", edges)

    print("Listo. Salidas en:", outdir)

if __name__ == "__main__":
    main()
