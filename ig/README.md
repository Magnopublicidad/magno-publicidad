# Sistema de plantillas de Instagram — MAGNO Publicidad

Genera publicaciones (posts, carruseles, reels, historias) fieles a la identidad de
MAGNO. Cada pieza es un **HTML standalone con CSS embebido + Google Fonts** que se
renderiza a **PNG en alta resolución** con Playwright/Chromium.

## Estructura
```
ig/
  brand/            logo procesado (blanco/oscuro) y la "M" de marca de agua
  magno.py          tokens de marca, CSS y helpers de página (page, watermark, logo)
  logo_prep.py      genera brand/*.png a partir de img/magno-logo.jpg
  render.py         HTML -> PNG (Chromium, device_scale_factor=2)
  comfrut.py        Publicación #2: carrusel caso de éxito Comfrut (ejemplo)
  build/<pieza>/    HTML generado
  out/<pieza>/      PNG finales (entregables)
```

## Uso
```bash
source .venv/bin/activate           # entorno con playwright + pillow + numpy

# (una sola vez, o si cambia el logo fuente)
python ig/logo_prep.py

# generar una publicación y renderizarla
PYTHONPATH=ig python ig/comfrut.py          # escribe ig/build/comfrut/*.html
python ig/render.py ig/build/comfrut        # escribe ig/out/comfrut/*.png
```

## Tokens de marca
- Negro `#0A0A0A` · Lima `#C8F500` · Crema `#F4F1E8` · Blanco · Oliva (acento sobre claro) `#7A9000`
- Títulos: **Archivo Black** · Texto: **Sora**
- Medidas: cuadrado `1080×1080` (SQUARE), vertical `1080×1920` (STORY). Render a 2× → PNG de 2160 px.

## Crear una pieza nueva
En un script (p. ej. `ig/mi_post.py`):
```python
from magno import Doc, page, SQUARE, STORY, photo, watermark, logo_tag
doc = Doc("ig/build/mi_post")
body = '<div class="layer display" style="left:60px; top:300px; font-size:120px">HOLA</div>'
doc.write("01.html", page(SQUARE, bg="black", logo="white",
          watermark_html=watermark("white", bottom=-160, right=-150, opacity=0.07),
          body=body))
```
Clases útiles del CSS: `.display` (Archivo Black), `.body`/`.eyebrow` (Sora),
`.lime`/`.olive`, `.bg-black`/`.bg-cream`/`.bg-lime`, `.photo-bg`, `.overlay.shade`,
`.layer` (capa posicionada), `.bar`, `.btn`. Regla de feed: alternar piezas
oscuras y claras; nunca dos claras seguidas.
