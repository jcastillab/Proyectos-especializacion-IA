# Taller de Visión Computacional U1

Implementa un pipeline básico con OpenCV. Lee la imagen, convierte a grises, aplica Gauss, detecta bordes con Canny y guarda las salidas.

## Objetivo
- Ejecuta un flujo reproducible de preprocesamiento y detección de bordes.
- Genera archivos de salida listos para entregar.

## Requisitos
- Python 3.13 o 3.11
- pip actualizado

### Paquetes
```
opencv-python
numpy
scikit-image
```

## Estructura del proyecto
```
Unidad 1/
  .venv/
  data/
    entrada.png            # imagen de entrada
    out/                   # salidas
  src/
    ops.py
    pipeline.py
  requirements.txt
```

## Instalación rápida
**Windows PowerShell**
```powershell
cd "Ruta a la carpeta del proyecto"
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Uso básico
Guarda tu imagen en `data/entrada.png`.
```powershell
# Ejecuta sin ventanas, genera salidas
python .\src\pipeline.py -i .\data\entrada.png

# Muestra cada etapa con tamaño controlado
python .\src\pipeline.py -i .\data\entrada.png --show --fitw 1100 --fith 700
```

## Parámetros
- `--input, -i` ruta de la imagen. Por defecto `data/entrada.jpg`.
- `--outdir, -o` carpeta de salida. Por defecto `data/out`.
- `--k` tamaño de kernel Gauss. Impar. Por defecto 5.
- `--sigma` sigma de Gauss. Por defecto 1.0.
- `--t1` umbral bajo de Canny. Por defecto 100.
- `--t2` umbral alto de Canny. Por defecto 200.
- `--show` muestra ventanas.
- `--fitw` ancho máximo al mostrar. Por defecto 1280.
- `--fith` alto máximo al mostrar. Por defecto 900.

## Ejemplos
```powershell
python .\src\pipeline.py -i .\data\entrada.png --k 7 --sigma 1.4 --t1 40 --t2 120

# Visualiza cada etapa
python .\src\pipeline.py -i .\data\entrada.png --show --fitw 1280 --fith 900
```

## Salidas esperadas
Se guardan en `data/out`.
- `salida_grises.png`
- `salida_blur.png`
- `salida_bordes.png`

## Extras opcionales
Activa extras para generar overlay e histograma.
```powershell
python .\src\pipeline.py -i .\data\entrada.png --k 7 --sigma 1.4 --t1 40 --t2 120 --extras
```
Salidas adicionales:
- `salida_overlay.png` bordes en rojo sobre la imagen original.
- `histograma.png` histograma de intensidades.

## Notas de compatibilidad
- Si tu JPEG muestra aviso `Invalid SOS parameters for sequential JPEG`, convierte a PNG una vez.
```powershell
python -c "import cv2, pathlib; p=pathlib.Path('data/entrada.jpg'); img=cv2.imread(str(p)); out=pathlib.Path('data/entrada.png'); cv2.imwrite(str(out), img)"
```
- Si la ventana se ve gigante, usa `--fitw` y `--fith`.

## Problemas comunes y soluciones
- **No abre la imagen**. Verifica ruta y extensión. Usa `-i` con la ruta real.
- **Ventanas enormes**. Confirma que el log muestre `Mostrando ... en WxH`. Ajusta `--fitw` y `--fith`.
- **Permisos en PowerShell**. Activa scripts en la sesión actual:
```powershell
Set-ExecutionPolicy -Scope Process RemoteSigned
```

## Registro de comandos usados
Pega aquí el comando final que corriste en tu equipo.
```
python src/pipeline.py -i data/entrada.png --k 7 --sigma 1.4 --t1 40 --t2 120
```

## Licencia
Uso académico.
