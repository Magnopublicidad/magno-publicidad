"""
Renderiza piezas HTML a PNG de alta resolucion.

  python ig/render.py ig/build/comfrut            # todos los .html de la carpeta
  python ig/render.py ig/build/comfrut/01.html    # un archivo
  python ig/render.py ig/build/comfrut -o ig/out/comfrut

Patron: Chromium (Playwright), device_scale_factor=2, espera networkidle +
fuentes listas + 1000ms, y captura el elemento #frame (medidas exactas).
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

def collect(args):
    files, out = [], None
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("-o", "--out"):
            out = Path(args[i + 1]); i += 2; continue
        p = Path(a)
        if p.is_dir():
            files += sorted(p.glob("*.html"))
        elif p.suffix == ".html":
            files.append(p)
        i += 1
    return files, out

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(1)
    files, out = collect(args)
    if not files:
        print("No se encontraron archivos .html"); sys.exit(1)
    if out is None:
        out = Path("ig/out") / files[0].parent.name
    out.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for f in files:
            page = browser.new_page(device_scale_factor=2)
            page.goto(f.resolve().as_uri())
            page.wait_for_load_state("networkidle")
            try:
                page.evaluate("document.fonts.ready")
            except Exception:
                pass
            page.wait_for_timeout(1000)
            dst = out / (f.stem + ".png")
            page.locator("#frame").screenshot(path=str(dst), type="png")
            print("->", dst)
            page.close()
        browser.close()
    print(f"OK  {len(files)} pieza(s) -> {out}/")

if __name__ == "__main__":
    main()
