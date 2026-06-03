"""
Genera variantes limpias del logo MAGNO a partir de img/magno-logo.jpg
(lockup blanco sobre fondo negro, con acentos en verde lima).

Salidas en ig/brand/:
  logo-white.png      lockup completo, fondo transparente, colores originales (blanco + lima)
  logo-dark.png       lockup completo, fondo transparente, recoloreado (negro + oliva) para fondos claros
  mark-white.png      solo la "M" con sonrisa, blanca, transparente (marca de agua sobre oscuro)
  mark-dark.png       solo la "M" con sonrisa, negra, transparente (marca de agua sobre claro)

Tecnica: el fondo es negro puro -> usamos la luminancia como canal alfa (cobertura)
y normalizamos el color de cada pixel a su tono pleno para evitar halos oscuros.
Para la version oscura clasificamos lima vs blanco por tono y recoloreamos.
"""
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "img" / "magno-logo.jpg"
OUT = ROOT / "brand"
OUT.mkdir(parents=True, exist_ok=True)

BLACK = (10, 10, 10)      # #0A0A0A
OLIVE = (122, 144, 0)     # #7A9000

im = Image.open(SRC).convert("RGB")
arr = np.asarray(im).astype(np.float32)
r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]

# Alfa = cobertura, derivada del canal mas brillante (fondo negro -> ~0 -> transparente)
mx = np.maximum(np.maximum(r, g), b)
alpha = np.clip(mx, 0, 255)
# Limpiar ruido del fondo: por debajo de 18 -> totalmente transparente
alpha[mx < 18] = 0

# Color normalizado a tono pleno (evita fringe oscuro en bordes antialias)
scale = np.where(mx > 0, 255.0 / np.maximum(mx, 1.0), 0.0)
rn = np.clip(r * scale, 0, 255)
gn = np.clip(g * scale, 0, 255)
bn = np.clip(b * scale, 0, 255)

# ---- WHITE: colores originales (blanco + lima) sobre transparente ----
white = np.zeros((*arr.shape[:2], 4), dtype=np.uint8)
white[..., 0], white[..., 1], white[..., 2] = rn, gn, bn
white[..., 3] = alpha.astype(np.uint8)
Image.fromarray(white, "RGBA").save(OUT / "logo-white.png")

# ---- DARK: blanco->negro, lima->oliva, sobre transparente ----
# lima normalizada ~ (R alto, G alto, B bajo); blanco ~ B alto
is_lime = (bn < 120) & (gn > 140) & (rn > 90)
dark = np.zeros_like(white)
dark[..., 0] = np.where(is_lime, OLIVE[0], BLACK[0])
dark[..., 1] = np.where(is_lime, OLIVE[1], BLACK[1])
dark[..., 2] = np.where(is_lime, OLIVE[2], BLACK[2])
dark[..., 3] = alpha.astype(np.uint8)
Image.fromarray(dark, "RGBA").save(OUT / "logo-dark.png")

# ---- MARK: recortar solo la "M" con sonrisa (parte izquierda del lockup) ----
W, H = im.size  # (1280, 832)
# Caja aproximada de la M (incluye la sonrisa); luego recortamos al contenido real.
box = (int(W * 0.11), int(H * 0.06), int(W * 0.50), int(H * 0.62))

def crop_trim(png_path, out_path):
    img = Image.open(png_path).crop(box)
    bbox = img.getbbox()  # recorta transparencia sobrante
    if bbox:
        img = img.crop(bbox)
    img.save(out_path)

crop_trim(OUT / "logo-white.png", OUT / "mark-white.png")
crop_trim(OUT / "logo-dark.png", OUT / "mark-dark.png")

for name in ["logo-white", "logo-dark", "mark-white", "mark-dark"]:
    s = Image.open(OUT / f"{name}.png").size
    print(f"{name}.png  {s[0]}x{s[1]}")
print("OK")
