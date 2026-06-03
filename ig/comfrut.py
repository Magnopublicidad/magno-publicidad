"""
Publicacion #2 — Carrusel caso de exito: Rotulacion vehicular COMFRUT.
Genera 5 laminas HTML standalone en ig/build/comfrut/.

  python ig/comfrut.py        # genera el HTML
  python ig/render.py ig/build/comfrut   # renderiza a PNG en ig/out/comfrut/
"""
from magno import Doc, page, photo, watermark, SQUARE

doc = Doc("ig/build/comfrut")
LAT = photo("vehicular-comfrut-lateral.jpg")
ATR = photo("vehicular-comfrut-atras.jpg")

# --- Lamina 1: PORTADA (negro, tipografica, M de marca de agua) ---
body1 = f"""
<div class="layer eyebrow lime" style="left:64px; top:172px; font-size:26px">CASO DE ÉXITO</div>
<div class="layer display" style="left:52px; top:312px; font-size:138px; color:var(--white)">ROTULACIÓN<br>VEHICULAR</div>
<div class="layer body" style="left:66px; top:640px; width:760px; font-size:38px; font-weight:600; color:#D9D9D9">
  Le pusimos identidad a la flota de Comfrut: un camión que ahora vende en cada recorrido.
</div>
<div class="layer" style="left:64px; bottom:118px; display:flex; align-items:center; gap:22px">
  <span class="bar" style="width:56px; height:9px; display:block"></span>
  <span class="body" style="font-size:28px; font-weight:700; letter-spacing:0.04em">COMFRUT · Frutas y legumbres</span>
</div>
<div class="layer eyebrow lime" style="right:64px; bottom:120px; font-size:23px">DESLIZA →</div>
"""
doc.write("01-portada.html", page(SQUARE, bg="black", logo="white",
          watermark_html=watermark("white", size=1180, bottom=-180, right=-150, opacity=0.07),
          body=body1))

# --- Lamina 2: FOTO lateral ---
def foto(label, caption, src):
    return f"""
    <div class="photo-bg" style="background-image:url('{src}')"></div>
    <div class="overlay" style="background:linear-gradient(180deg, rgba(10,10,10,.62) 0%, rgba(10,10,10,0) 220px)"></div>
    <div class="overlay shade"></div>
    <div class="layer eyebrow lime" style="left:64px; bottom:302px; font-size:24px">{label}</div>
    <div class="layer display" style="left:60px; bottom:112px; width:960px; font-size:52px; color:var(--white)">{caption}</div>
    <div class="layer bar" style="left:64px; bottom:72px; width:120px; height:9px"></div>
    """

doc.write("02-lateral.html", page(SQUARE, bg="black", logo="white",
          body=foto("VISTA LATERAL", "Diseño full-wrap que<br>convierte cada km<br>en publicidad", LAT)))

# --- Lamina 3: FOTO trasera ---
doc.write("03-trasera.html", page(SQUARE, bg="black", logo="white",
          body=foto("VISTA TRASERA", "Marca, contacto y<br>producto: visibles<br>desde cualquier ángulo", ATR)))

# --- Lamina 4: DETALLE / que hicimos (crema) ---
bullets = [
    "Diseño del wrap a la medida",
    "Impresión en vinilo de alta duración",
    "Instalación profesional full-wrap",
    "Cobertura en Medellín y Barranquilla",
]
items = "".join(f"""
  <div style="display:flex; align-items:center; gap:26px; margin-bottom:34px">
    <span style="width:22px; height:22px; background:var(--olive); display:block; flex:0 0 auto"></span>
    <span class="body" style="font-size:40px; font-weight:700; color:var(--black)">{b}</span>
  </div>""" for b in bullets)
body4 = f"""
<div class="layer eyebrow olive" style="left:64px; top:172px; font-size:26px">QUÉ HICIMOS</div>
<div class="layer display" style="left:60px; top:240px; width:960px; font-size:96px; color:var(--black)">
  BRANDING<br>VEHICULAR</div>
<div class="layer" style="left:64px; top:520px; width:900px">{items}</div>
<div class="layer bar" style="left:0; bottom:0; width:1080px; height:18px"></div>
"""
doc.write("04-detalle.html", page(SQUARE, bg="cream", logo="dark",
          watermark_html=watermark("dark", size=1020, bottom=-160, right=-130, opacity=0.05),
          body=body4))

# --- Lamina 5: CIERRE / CTA (negro) ---
body5 = f"""
<div class="layer eyebrow lime" style="left:64px; top:172px; font-size:26px">¿LISTO PARA RODAR?</div>
<div class="layer display" style="left:56px; top:280px; width:980px; font-size:104px; color:var(--white)">
  ¿TU MARCA<br>LA <span class="lime">SIGUIENTE?</span></div>
<div class="layer body" style="left:66px; top:600px; width:820px; font-size:36px; font-weight:600; color:#D9D9D9">
  Hacemos que tu marca se sienta VIVA, dentro y fuera de tu local. Escríbenos y la ponemos a rodar.</div>
<div class="layer" style="left:64px; bottom:170px"><span class="btn">Escríbenos →</span></div>
<div class="layer body" style="left:66px; bottom:108px; font-size:30px; font-weight:700; color:var(--white)">@publicidad_magno</div>
"""
doc.write("05-cierre.html", page(SQUARE, bg="black", logo="white",
          watermark_html=watermark("white", size=1120, top=-160, right=-150, opacity=0.07),
          body=body5))

print("HTML generado en ig/build/comfrut/")
