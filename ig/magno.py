"""
Sistema de plantillas MAGNO Publicidad.

Cada pieza se emite como HTML *standalone* con CSS embebido y Google Fonts.
Se renderiza luego a PNG con ig/render.py (Playwright + Chromium, dsf=2).

Uso tipico desde un script de publicacion:

    from magno import Doc, page, SQUARE, STORY
    html = page(SQUARE, bg="black", logo="white", body=" ... ", watermark=True)
    Doc("ig/build/comfrut").write("01-portada.html", html)
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRAND = ROOT / "brand"
IMG = ROOT.parent / "img"

# --- Tokens de marca ---
BLACK = "#0A0A0A"
LIME = "#C8F500"
CREAM = "#F4F1E8"
WHITE = "#FFFFFF"
OLIVE = "#7A9000"

SQUARE = (1080, 1080)
STORY = (1080, 1920)

def asset(p: Path) -> str:
    """Ruta absoluta file:// para que el render y el HTML standalone funcionen."""
    return p.resolve().as_uri()

def photo(name: str) -> str:
    return asset(IMG / name)

CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Sora:wght@400;600;700;800&display=swap');

:root {{
  --black: {BLACK}; --lime: {LIME}; --cream: {CREAM}; --white: {WHITE}; --olive: {OLIVE};
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ background:#808080; }}

/* El marco es el lienzo exacto que se exporta */
#frame {{
  position: relative;
  overflow: hidden;
  font-family: 'Sora', sans-serif;
  -webkit-font-smoothing: antialiased;
  color: var(--white);
}}
#frame.square {{ width:1080px; height:1080px; }}
#frame.story  {{ width:1080px; height:1920px; }}

/* Fondos */
.bg-black {{ background: var(--black); color: var(--white); }}
.bg-cream {{ background: var(--cream); color: var(--black); }}
.bg-lime  {{ background: var(--lime);  color: var(--black); }}

/* Tipografia */
.display {{ font-family:'Archivo Black', sans-serif; line-height:0.92; letter-spacing:-0.01em; text-transform:uppercase; }}
.eyebrow {{ font-family:'Sora', sans-serif; font-weight:800; letter-spacing:0.22em; text-transform:uppercase; }}
.body    {{ font-family:'Sora', sans-serif; font-weight:600; line-height:1.35; }}
.lime    {{ color: var(--lime); }}
.olive   {{ color: var(--olive); }}
.k-black {{ color: var(--black); }}
.k-white {{ color: var(--white); }}

/* Logo esquina superior izquierda */
.logo {{ position:absolute; top:64px; left:64px; z-index:5; }}
.logo img {{ display:block; height:62px; width:auto; }}
.story .logo {{ top:80px; left:72px; }}
.story .logo img {{ height:78px; }}

/* Marca de agua: la M de fondo */
.wm {{ position:absolute; z-index:0; pointer-events:none; }}
.wm img {{ display:block; }}

/* Capas sobre foto */
.photo-bg {{ position:absolute; inset:0; z-index:0; background-size:cover; background-position:center; }}
.overlay {{ position:absolute; inset:0; z-index:1; }}
.shade {{ background:linear-gradient(180deg, rgba(10,10,10,.15) 0%, rgba(10,10,10,.30) 45%, rgba(10,10,10,.92) 100%); }}
.shade-full {{ background:rgba(10,10,10,.46); }}

.layer {{ position:absolute; z-index:2; }}

/* Barra de acento */
.bar {{ background: var(--lime); }}

/* Boton */
.btn {{ display:inline-block; background:var(--lime); color:var(--black);
  font-family:'Archivo Black',sans-serif; text-transform:uppercase;
  padding:26px 44px; font-size:36px; letter-spacing:0.01em; border-radius:4px; }}
"""

def watermark(variant="white", size=1180, top=None, left=None, bottom=None, right=None, opacity=0.06, rotate=0):
    mark = asset(BRAND / ("mark-white.png" if variant == "white" else "mark-dark.png"))
    pos = []
    if top is not None: pos.append(f"top:{top}px")
    if left is not None: pos.append(f"left:{left}px")
    if bottom is not None: pos.append(f"bottom:{bottom}px")
    if right is not None: pos.append(f"right:{right}px")
    if not pos: pos = ["top:50%", "left:50%", "transform:translate(-50%,-50%)"]
    transform = f" transform:rotate({rotate}deg);" if rotate else ""
    return (f'<div class="wm" style="{";".join(pos)};opacity:{opacity};{transform}">'
            f'<img src="{mark}" style="width:{size}px"></div>')

def logo_tag(variant="white"):
    src = asset(BRAND / ("logo-white.png" if variant == "white" else "logo-dark.png"))
    return f'<div class="logo"><img src="{src}"></div>'

def page(size, bg=None, logo="white", body="", watermark_html="", extra_css=""):
    cls = "square" if size == SQUARE else "story"
    bgcls = {"black": "bg-black", "cream": "bg-cream", "lime": "bg-lime", None: ""}[bg]
    extra = f"<style>{extra_css}</style>" if extra_css else ""
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<style>{CSS}</style>{extra}
</head><body>
<div id="frame" class="{cls} {bgcls}">
  {watermark_html}
  {logo_tag(logo)}
  {body}
</div>
</body></html>"""

class Doc:
    def __init__(self, outdir):
        self.dir = Path(outdir)
        self.dir.mkdir(parents=True, exist_ok=True)
    def write(self, name, html):
        p = self.dir / name
        p.write_text(html, encoding="utf-8")
        return p
