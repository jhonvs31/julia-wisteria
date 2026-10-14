"""Convierte los logos de la cliente (JPG sobre crema) en PNG transparentes + favicons.
Uso: python3 tools/make_logos.py <wordmark.jpg> <monogram.jpg>"""
import sys, os
import numpy as np
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'brand')
os.makedirs(OUT, exist_ok=True)
BROWN = np.array([143, 103, 94], float)   # color de letras del logo
CREAM = np.array([249, 242, 235], float)  # versión clara para fondos oscuros

GOLD = np.array([217, 201, 155], float)   # hojas doradas del logo

def color_to_alpha(path):
    """Matting con dos tintas conocidas (marrón y dorado) sobre el fondo crema:
    cada píxel = a*tinta + (1-a)*fondo → se despeja a y se deja la tinta pura."""
    im = np.asarray(Image.open(path).convert('RGB')).astype(float)
    bg = np.median(im[:40].reshape(-1, 3), axis=0)
    best_a = np.zeros(im.shape[:2]); best_rgb = np.zeros(im.shape); best_err = np.full(im.shape[:2], np.inf)
    for ink in (BROWN, GOLD):
        v = ink - bg
        a = np.clip(((im - bg) @ v) / (v @ v), 0, 1)
        err = np.linalg.norm(im - (bg + a[..., None] * v), axis=2)
        pick = err < best_err
        best_err[pick] = err[pick]; best_a[pick] = a[pick]; best_rgb[pick] = ink
    best_a[best_a < 0.05] = 0
    out = np.dstack([best_rgb, best_a * 255]).astype(np.uint8)
    ys, xs = np.where(best_a > 0.05)
    pad = 12
    return out[max(ys.min() - pad, 0):ys.max() + pad, max(xs.min() - pad, 0):xs.max() + pad]

def light(rgba):
    """Pasa el marrón a crema y deja el dorado: para el footer vino."""
    px = rgba.astype(float)
    m = (np.linalg.norm(px[..., :3] - BROWN, axis=2) < 1) & (px[..., 3] > 0)
    px[m, :3] = CREAM
    return px.astype(np.uint8)

def save(arr, name, width=None):
    im = Image.fromarray(arr)
    if width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, name), optimize=True)
    return im

word = color_to_alpha(sys.argv[1]); mono = color_to_alpha(sys.argv[2])
save(word, 'logo-julia-wisteria.png', 900)
save(light(word), 'logo-julia-wisteria-light.png', 900)
save(mono, 'monogram-jw.png', 600)
save(light(mono), 'monogram-jw-light.png', 600)
# favicons: monograma centrado sobre fondo crema (se ve bien en pestañas claras y oscuras)
m = Image.fromarray(mono); side = max(m.size)
sq = Image.new('RGBA', (side, side), (245, 238, 229, 255)); sq.alpha_composite(m, ((side - m.width) // 2, (side - m.height) // 2))
for n, s in [('favicon-32.png', 32), ('favicon-192.png', 192), ('apple-touch-icon.png', 180), ('site-icon-512.png', 512)]:
    sq.resize((s, s), Image.LANCZOS).convert('RGB').save(os.path.join(OUT, n), optimize=True)
print('OK', os.listdir(OUT))
