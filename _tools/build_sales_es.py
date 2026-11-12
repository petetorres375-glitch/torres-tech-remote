#!/usr/bin/env python3
"""Builds es/tarjetas-de-presentacion-digitales/index.html (Spanish sales page) from digital-business-cards.html.
Only writes that one file. Safe to re-run."""
import re, urllib.parse, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
s = (root / "digital-business-cards.html").read_text(encoding="utf-8")
s = re.sub(r'<link href="[^"]*" hreflang="[^"]*" rel="alternate"/>\n', "", s)  # English page has its own; each build adds the full set
s = re.sub(r'<nav class="langsw".*?</nav>\n', "", s, flags=re.S)
s = re.sub(r'\.langsw\{[^\n]*\n', "", s)

def variants(t):
    out = [t]
    for f in (lambda x: x.replace("&", "&amp;"), lambda x: x.replace("'", "’"),
              lambda x: x.replace("'", "’").replace("&", "&amp;"), lambda x: x.replace("’", "&rsquo;"),
              lambda x: x.replace("“", "&ldquo;").replace("”", "&rdquo;")):
        v = f(t)
        if v not in out: out.append(v)
    return out

def R(en, es, n=None):
    """replace en -> es (all occurrences of whichever spelling variant is present)"""
    global s
    total = 0
    for v in variants(en):
        c = s.count(v)
        if c:
            s = s.replace(v, es.replace("&", "&amp;") if v != en and "&amp;" in v else es); total += c
    assert total >= 1, f"not found: {en[:70]!r}"
    if n is not None: assert total == n, f"{en[:50]!r}: expected {n}, found {total}"

URL = "https://torrestechremote.com/es/tarjetas-de-presentacion-digitales/"
EN = "https://torrestechremote.com/digital-business-cards.html"

# ---------- head ----------
R('<html lang="en">', '<html lang="es">', 1)
R("<title>Digital Business Cards for Small Businesses Across the U.S. | Torres Tech Remote</title>", "<title>Tarjetas de presentación digitales para pequeños negocios en todo EE. UU. | Torres Tech Remote</title>", 1)
R('content="Digital business cards for one business, every location, and your whole team. One link and one QR code; customers call, text, email or save you in one tap, in up to 3 of 25 languages. Free setup, then $10/month. Free preview before you pay."',
  'content="Tarjetas de presentación digitales para un negocio, cada local y todo su equipo. Un enlace y un código QR; los clientes le llaman, le escriben, le envían un correo o le guardan con un solo toque, en hasta 3 de 25 idiomas. Instalación gratis, luego $10/mes. Vista previa gratis antes de pagar."', 1)
R(f'<link href="{EN}" rel="canonical"/>',
  f'<link href="{URL}" rel="canonical"/>\n<link href="{EN}" hreflang="en" rel="alternate"/>\n<link href="{URL}" hreflang="es" rel="alternate"/>\n<link href="{EN}" hreflang="x-default" rel="alternate"/>', 1)
R(f'<meta content="{EN}" property="og:url"/>', f'<meta content="{URL}" property="og:url"/>', 1)
OT = "Tarjetas de presentación digitales para su negocio, cada local y su equipo"
R('content="Digital Business Cards for Your Business, Every Location, and Your Team"', f'content="{OT}"', 2)
OD = "Para pequeños negocios en todo EE. UU.: un enlace y un código QR para cada local, una tarjeta para cada persona, y nosotros hacemos sus actualizaciones. Instalación gratis, luego $10/mes. Vista previa gratis antes de pagar."
R('content="For small businesses across the U.S.: one link and one QR code for each location, a card for each person, and we do your updates. Free setup, then $10/month. Free preview before you pay."', f'content="{OD}"', 2)
R('content="Torres Tech Remote: digital business cards for small businesses across the U.S., for one business, every location, and your whole team"',
  'content="Torres Tech Remote: tarjetas de presentación digitales para pequeños negocios en todo EE. UU., para un negocio, cada local y todo su equipo"', 1)
# JSON-LD
R(f'"@id": "{EN}#webpage",\n      "url": "{EN}",\n      "name": "Digital Business Cards for Small Businesses Across the U.S.",',
  f'"@id": "{URL}#webpage",\n      "url": "{URL}",\n      "inLanguage": "es",\n      "name": "Tarjetas de presentación digitales para pequeños negocios en todo EE. UU.",', 1)
R(f'"breadcrumb": {{ "@id": "{EN}#breadcrumb" }}', f'"breadcrumb": {{ "@id": "{URL}#breadcrumb" }}', 1)
R(f'"@id": "{EN}#breadcrumb",', f'"@id": "{URL}#breadcrumb",', 1)
R(f'"position": 2, "name": "Digital Business Cards", "item": "{EN}"', f'"position": 2, "name": "Tarjetas de presentación digitales", "item": "{URL}"', 1)
R('"description": "One link and one QR code for your business, every location, and your team. Customers call, text or email you in one tap, save you to their contacts, and read it in up to 3 of 25 languages. We design it, host it and keep it up to date.",',
  '"description": "Un enlace y un código QR para su negocio, cada local y su equipo. Los clientes le llaman, le escriben o le envían un correo con un solo toque, le guardan en sus contactos y la leen en hasta 3 de 25 idiomas. Nosotros la diseñamos, la alojamos y la mantenemos al día.",', 1)
# the Service block keeps pointing at the English #service id (shared entity); only its name is localized elsewhere

# language switch (class langsw: the page already uses .langs for the language grid)
R('</style>\n</head>', '.langsw{display:flex;gap:12px;font-size:14px;align-items:center;margin-right:6px}.langsw a{color:var(--muted,#65717e);text-decoration:none}.langsw a:hover{text-decoration:underline}.langsw b{color:var(--navy,#12192d)}@media(max-width:1100px){.nav{flex-wrap:wrap;row-gap:0;padding-block:6px}.nav-right{display:contents}.navlink{display:none}.langsw{order:3;width:100%;justify-content:center;margin:0;padding:4px 0 2px;font-size:13px}.nav .btn-plum{order:2;margin-left:auto}.nav .btn-wa{order:2;margin-left:8px}}\n</style>\n</head>', 1)
R('<div class="nav-right">\n', '<div class="nav-right">\n<nav class="langsw" aria-label="Idioma"><a href="/digital-business-cards.html" hreflang="en" lang="en">English</a><b aria-current="page">Español</b><a href="/pt/cartoes-de-visita-digitais/" hreflang="pt-PT" lang="pt-PT">Português</a></nav>\n', 1)

# ---------- absolute paths ----------
s = s.replace('src="img/', 'src="/img/').replace('poster="video/', 'poster="/video/').replace('src="video/', 'src="/video/')
R('`video/${clip}-', '`/video/${clip}-', 1)
R('href="tos.html"', 'href="/tos.html"'); R('href="privacy.html"', 'href="/privacy.html"')
R('<a class="brand" href="/">', '<a class="brand" href="/es/">', 2)
# always Spanish steps + videos on this page, whatever the phone language is
R('.find((l) => ["en", "es", "pt", "pt-PT"].includes(l))) || "en";', '.find((l) => ["en", "es", "pt", "pt-PT"].includes(l))) || "en";\n    const pageLang = "es"; // this page is the Spanish page', 1)
s2 = s.replace("const lang = ((navigator.languages", "const phoneLang = ((navigator.languages", 1)
assert s2 != s; s = s2
R("    if (STEPS[lang]) {", "    const lang = pageLang;\n    if (STEPS[lang]) {", 1)

# free preview buttons -> Spanish form
s = s.replace('href="/go/preview.html"', 'href="/go/preview-es.html"')

# ---------- header + hero ----------
R('rel="noopener" target="_blank">Demo card</a>', 'rel="noopener" target="_blank">Tarjeta de demostración</a>', 1)
R('<a class="navlink" href="#faq">FAQ</a>', '<a class="navlink" href="#faq">Preguntas frecuentes</a>', 1)
R('target="_blank">Free preview</a>', 'target="_blank">Vista previa gratis</a>', 1)
R('href="tel:+12017722106">Call</a>', 'href="tel:+12017722106">Llamar</a>', 1)
R('Digital Business Cards · Newark, NJ', 'Tarjetas de presentación digitales · Newark, NJ', 1)
R('<h1>A business card your customers <em>keep on their phone.</em></h1>', '<h1>Una tarjeta de presentación que sus clientes <em>guardan en el teléfono.</em></h1>', 1)
R("One link and one QR code for your shop. Customers call, text, WhatsApp or email you in one tap and save you to their contacts. Your card opens in your customer's own phone language, and they can tap to switch. We design it, host it and keep it up to date. You never touch an app.",
  "Un enlace y un código QR para su negocio. Sus clientes le llaman, le escriben, le envían un WhatsApp o un correo con un solo toque, y le guardan en sus contactos. Su tarjeta se abre en el idioma del teléfono de cada cliente, y ellos pueden tocar para cambiarlo. Nosotros la diseñamos, la alojamos y la mantenemos al día. Usted nunca toca una aplicación.", 1)
R('>Call (201) 772-2106</a>', '>Llamar al (201) 772-2106</a>', 2)
R('Hi%20Pedro%2C%20I%27d%20like%20a%20free%20preview%20for%20my%20business%3A%20', urllib.parse.quote("Hola Pedro, me gustaría una vista previa gratis para mi negocio: ", safe=""), 2)
R('>Text Pedro</a>', '>Escribir a Pedro</a>', 2)
R('>Request your free preview</a>', '>Pida su vista previa gratis</a>', 2)
R('Call and Text open on your phone. Email works from a computer or a phone.', 'Llamar y Escribir se abren en su teléfono. El correo funciona desde una computadora o un teléfono.', 2)
R('Free preview. No payment or credit card required. Just your name, business name, phone, and email to get started.', 'Vista previa gratis. Sin pago ni tarjeta de crédito. Solo su nombre, el nombre del negocio, teléfono y correo para empezar.', 2)
R('alt="Pedro Torres, owner of Torres Tech Remote"', 'alt="Pedro Torres, dueño de Torres Tech Remote"', 1)
R('>Email Pedro</a> · ', '>Escribir a Pedro por correo</a> · ', 1)
R('target="_blank">See the demo card</a>', 'target="_blank">Ver la tarjeta de demostración</a>', 1)
s, n = re.subn(r'<div class="tri">.*?</div>\n', '', s, flags=re.S); assert n == 1
R('alt="Torres Tech Remote\'s own digital business card on a phone: TTR logo, See a demo card button, call, text, WhatsApp, email and website buttons, Share, Save contact, Show QR code, and opening hours"',
  'alt="La tarjeta de presentación digital de Torres Tech Remote en un teléfono: logo de TTR, botón para ver una tarjeta de demostración, botones de llamada, mensaje, WhatsApp, correo y sitio web, Compartir, Guardar contacto, Mostrar código QR y horario"', 1)
R('<b>Our own card</b>', '<b>Nuestra propia tarjeta</b>', 1)
R('alt="Demo digital business card for a barbershop on a phone: logo, Book now button, call, text, WhatsApp, email, directions and website buttons, Save contact, Show QR code, and opening hours"',
  'alt="Tarjeta de presentación digital de demostración de una barbería en un teléfono: logo, botón de reservar, botones de llamada, mensaje, WhatsApp, correo, direcciones y sitio web, Guardar contacto, Mostrar código QR y horario"', 1)
R('<b>Demo card</b> for a made-up barbershop', '<b>Tarjeta de demostración</b> de una barbería inventada', 1)
R('aria-label="Service and pricing details"', 'aria-label="Servicio y precios"', 1)
R('<b>Free setup</b>', '<b>Instalación gratis</b>', 1)
R('<span>$10/month or $100/year</span>', '<span>$10/mes o $100/año</span>', 1)
R('<span>Up to 3 free previews</span>', '<span>Hasta 3 vistas previas gratis</span>', 1)
R('In-person service in the Ironbound, Newark NJ.', 'Servicio en persona en el Ironbound, Newark, NJ.', 1)
R('</svg>Now on Facebook</a>', '</svg>Ahora en Facebook</a>', 1)

# ---------- features ----------
R("<p class=\"kicker\">What's on your card</p>", '<p class="kicker">Qué lleva su tarjeta</p>', 1)
R('<h2>Everything a customer needs, one tap away.</h2>', '<h2>Todo lo que un cliente necesita, a un toque.</h2>', 1)
R('<p>Tap either card above to try the real thing.</p>', '<p>Toque cualquiera de las tarjetas de arriba para probar la real.</p>', 1)
R('<h3>Your brand</h3><p>Your logo and brand colors.</p>', '<h3>Su marca</h3><p>Su logo y los colores de su marca.</p>', 1)
R('<h3>One-tap buttons</h3><p>Call, text, WhatsApp, email, directions and website buttons.</p>', '<h3>Botones de un toque</h3><p>Botones de llamada, mensaje, WhatsApp, correo, direcciones y sitio web.</p>', 1)
R('<h3>Your business details</h3><p>Hours, services and prices, photos, payment links.</p>', '<h3>Los datos de su negocio</h3><p>Horario, servicios y precios, fotos y enlaces de pago.</p>', 1)
R('<h3>Opens in their language</h3><p>Their phone is set to Spanish? They see Spanish, and can tap to switch to your other languages. You pick up to 3 of 25.</p>',
  '<h3>Se abre en su idioma</h3><p>¿Su teléfono está en inglés? Ven inglés, y pueden tocar para cambiar a los otros idiomas de su negocio. Usted elige hasta 3 de 25.</p>', 1)
R('<h3>A spot for your offer</h3><p>Having a sale? Email me and I change it for you. It can turn itself off when your offer ends.</p>',
  '<h3>Un espacio para su oferta</h3><p>¿Tiene una promoción? Escríbame y se la cambio. Puede apagarse sola cuando termine la oferta.</p>', 1)
R('<h3>Easy to share</h3><p>QR code, Share and Save contact. <a href="#save-contact">See how</a>.</p>', '<h3>Fácil de compartir</h3><p>Código QR, Compartir y Guardar contacto. <a href="#save-contact">Vea cómo</a>.</p>', 1)
R('<h3>Like an app</h3><p>Installs like an app on iPhone and Android, no app store. <a href="#install">See how</a>.</p>', '<h3>Como una aplicación</h3><p>Se instala como una aplicación en iPhone y Android, sin tienda de aplicaciones. <a href="#install">Vea cómo</a>.</p>', 1)
R('<h3>A QR code that lasts</h3><p>Your QR code never changes, so printed codes keep working.</p>', '<h3>Un código QR que dura</h3><p>Su código QR nunca cambia, así que los códigos impresos siguen funcionando.</p>', 1)
R('<p class="kicker">Works like an app</p>', '<p class="kicker">Funciona como una aplicación</p>', 1)
R('<h3>Your card on their home screen.</h3>', '<h3>Su tarjeta en la pantalla de inicio de ellos.</h3>', 1)
R('<p>Customers save your card to their phone in a few taps. It gets its own icon, opens full screen like an app, and still opens without internet. No app store and no download. Pick your phone to watch how:</p>',
  '<p>Los clientes guardan su tarjeta en el teléfono en unos toques. Tiene su propio ícono, se abre a pantalla completa como una aplicación y abre incluso sin internet. Sin tienda de aplicaciones y sin descargar nada. Elija su teléfono para ver cómo:</p>', 1)
R('aria-label="Pick your phone"', 'aria-label="Elija su teléfono"', 2)
R('<p class="kicker">Saved in their contacts</p>', '<p class="kicker">Guardado en sus contactos</p>', 1)
R('<h3>In their contacts in seconds.</h3>', '<h3>En sus contactos en segundos.</h3>', 1)
R('<p>“Save contact” adds your business to their contacts with your logo, phone, email, address and website, so they can find you and call you later. Pick your phone to watch how:</p>',
  '<p>"Guardar contacto" agrega su negocio a los contactos del cliente con su logo, teléfono, correo, dirección y sitio web, para que puedan encontrarle y llamarle después. Elija su teléfono para ver cómo:</p>', 1)
# video aria-labels (screen readers)
R("Video: on an Android phone, open the card in Chrome, tap Add to home screen, tap Install, and the card's icon appears on the home screen", "Video: en un teléfono Android, abra la tarjeta en Chrome, toque Añadir a pantalla de inicio, toque Instalar, y el ícono de la tarjeta aparece en la pantalla de inicio", 1)
R("Video: on an iPhone, open the card in Safari, tap Share, tap Add to Home Screen, tap Add, and the card's icon appears on the home screen", "Video: en un iPhone, abra la tarjeta en Safari, toque Compartir, toque Añadir a pantalla de inicio, toque Añadir, y el ícono de la tarjeta aparece en la pantalla de inicio", 1)
R("Video: on an Android phone, tap Save contact on the card, it downloads, tap Open, then tap Import, and the business is in the phone's contacts", "Video: en un teléfono Android, toque Guardar contacto en la tarjeta, se descarga, toque Abrir, luego toque Importar, y el negocio queda en los contactos del teléfono", 1)
R("Video: on an iPhone, tap Save contact on the card, the contact opens, tap the check mark at the top left, and the business is in the phone's contacts", "Video: en un iPhone, toque Guardar contacto en la tarjeta, se abre el contacto, toque la marca de verificación arriba a la izquierda, y el negocio queda en los contactos del teléfono", 1)
# static (pre-JS) steps are replaced by the page script with the Spanish steps; make the static fallback Spanish too
for en, es in [('<li>Open the card in <b>Chrome</b>.</li>','<li>Abra la tarjeta en <b>Chrome</b>.</li>'),('<li>Tap <b>Add to home screen</b> on the card.</li>','<li>Toque <b>Añadir a pantalla de inicio</b> en la tarjeta.</li>'),('<li>Tap <b>Install</b>.</li>','<li>Toque <b>Instalar</b>.</li>'),
    ('<li>Open the card in <b>Safari</b> (iPhone or iPad).</li>','<li>Abra la tarjeta en <b>Safari</b> (iPhone o iPad).</li>'),('<li>Tap <b>Share</b> (the square with an arrow).</li>','<li>Toque <b>Compartir</b> (el cuadrado con una flecha).</li>'),
    ('<li>Tap <b>Add to Home Screen</b>, then <b>Add</b>.</li>','<li>Toque <b>Añadir a pantalla de inicio</b> y luego <b>Añadir</b>.</li>'),('<li>Tap <b>Save contact</b> on the card.</li>','<li>Toque <b>Guardar contacto</b> en la tarjeta.</li>'),
    ('<li>It downloads. Tap <b>Open</b>.</li>','<li>Se descarga. Toque <b>Abrir</b>.</li>'),('<li>Tap <b>Import</b> (some phones say <b>Save</b>).</li>','<li>Toque <b>Importar</b> (algunos teléfonos dicen <b>Guardar</b>).</li>'),
    ('<li>The contact opens. Tap <b>✓</b> at the top left.</li>','<li>Se abre el contacto. Toque <b>&#10003;</b> arriba a la izquierda.</li>')]:
    R(en, es)

# ---------- clients ----------
R('<p class="kicker">Real cards</p>', '<p class="kicker">Tarjetas reales</p>', 1)
R('<h2>Featured clients.</h2>', '<h2>Clientes destacados.</h2>', 1)
R('<p>These are screenshots. On the real card, every button works when you tap it.</p>', '<p>Son capturas de pantalla. En la tarjeta real, cada botón funciona al tocarlo.</p>', 1)
R('<p>English &amp; Acting Coach / Instructor<br/>Vietnam &amp; Japan</p>', '<p>Profesor y entrenador de inglés y actuación<br/>Vietnam y Japón</p>', 1)
R('Tap to see more', 'Toque para ver más', 2)
for en, es in [('Night · English','Noche · Inglés'),('Day · English','Día · Inglés'),('Night · Japanese','Noche · Japonés'),('Day · Japanese','Día · Japonés'),('Night · Vietnamese','Noche · Vietnamita'),('Day · Vietnamese','Día · Vietnamita'),('Night · Spanish','Noche · Español'),('Day · Spanish','Día · Español')]:
    R(en, es)
for nm in ['Keon Torres','Alpha Fit Club']:
    R(f'aria-label="Show all {nm} card screenshots"', f'aria-label="Ver todas las capturas de la tarjeta de {nm}"')
    R(f'aria-label="{nm} card screenshots"', f'aria-label="Capturas de la tarjeta de {nm}"')
    R(f'aria-label="Previous {nm} screenshot"', f'aria-label="Captura anterior de {nm}"')
    R(f'aria-label="Next {nm} screenshot"', f'aria-label="Captura siguiente de {nm}"')
R('aria-label="Choose a Keon Torres screenshot"', 'aria-label="Elegir una captura de Keon Torres"', 1)
R('aria-label="Choose an Alpha Fit Club screenshot"', 'aria-label="Elegir una captura de Alpha Fit Club"', 1)
R('alt="Keon Torres card, ', 'alt="Tarjeta de Keon Torres, '); R('alt="Alpha Fit Club card, ', 'alt="Tarjeta de Alpha Fit Club, ')
R('>Close</button>', '>Cerrar</button>', 2)
R('<p class="langnote">Three languages on one card: English, Japanese and Vietnamese.</p>', '<p class="langnote">Tres idiomas en una tarjeta: inglés, japonés y vietnamita.</p>', 1)
chips = [('<b>Message on LINE</b> opens a chat','<b>Mensaje por LINE</b> abre un chat'),('<b>Email</b> writes to him','<b>Correo</b> le escribe a él'),('<b>EN / JA / VI</b> switches language','<b>EN / JA / VI</b> cambia el idioma'),
 ('<b>Day / Night</b> switches the look','<b>Día / Noche</b> cambia el aspecto'),('<b>Share</b> send the card','<b>Compartir</b> envía la tarjeta'),('<b>Save contact</b> adds to phone','<b>Guardar contacto</b> lo agrega al teléfono'),
 ('<b>QR code</b> scan to open','<b>Código QR</b> escanee para abrir'),('<b>Add to home screen</b> installs like an app','<b>Añadir a pantalla de inicio</b> se instala como una aplicación'),
 ('<b>Book first class</b> opens booking page','<b>Reservar primera clase</b> abre la página de reservas'),('<b>Call</b> rings the gym','<b>Llamar</b> suena en el gimnasio'),('<b>Text</b> starts a text','<b>Mensaje</b> inicia un mensaje de texto'),
 ('<b>Email</b> writes to the gym','<b>Correo</b> le escribe al gimnasio'),('<b>Directions</b> opens the map','<b>Direcciones</b> abre el mapa'),('<b>EN / ES</b> switches language','<b>EN / ES</b> cambia el idioma')]
for en, es in chips: R(en, es)
R('<p class="langnote">English and Spanish on one card.</p>', '<p class="langnote">Inglés y español en una tarjeta.</p>', 1)
R('<p>Alpha Fit Club</p>', '<p>Alpha Fit Club</p>') if False else None
R('aria-label="5 out of 5 stars"', 'aria-label="5 de 5 estrellas"', 1)
R('Google review, 5.0', 'Reseña de Google (en inglés), 5.0', 1)

# ---------- how ----------
R('<p class="kicker">How it works</p>', '<p class="kicker">Cómo funciona</p>', 1)
R('<h2>See it before you pay.</h2>', '<h2>Véala antes de pagar.</h2>', 1)
R('<h3>Fill out our Free Preview form</h3><p>Only your name, business name, phone, email, and confirmation checkbox are required. All other questions are optional.</p>',
  '<h3>Llene nuestro formulario de vista previa gratis</h3><p>Solo se piden su nombre, el nombre del negocio, teléfono, correo y una casilla de confirmación. Las demás preguntas son opcionales.</p>', 1)
R("<h3>Get your free preview</h3><p>We'll create your free digital business card preview using the information you provide and email it to you for review. You can receive up to 3 free previews. You only pay if you approve your card.</p>",
  '<h3>Reciba su vista previa gratis</h3><p>Crearemos la vista previa gratis de su tarjeta de presentación digital con los datos que nos dé y se la enviaremos por correo para que la revise. Puede recibir hasta 3 vistas previas gratis. Solo paga si aprueba su tarjeta.</p>', 1)
R("<h3>Pay when you're happy</h3><p>You only pay when you’re happy with it. Then your card goes live with its own link and QR code.</p>",
  '<h3>Pague cuando esté contento</h3><p>Solo paga cuando esté contento con el resultado. Entonces su tarjeta se publica con su propio enlace y código QR.</p>', 1)
R('<p class="kicker">Languages</p>', '<p class="kicker">Idiomas</p>', 1)
R('<h2>Up to 3 of 25 languages.</h2>', '<h2>Hasta 3 de 25 idiomas.</h2>', 1)
R('<p class="sub-lead">Pick up to 3 languages for your card, like Spanish, Portuguese, Chinese, Japanese and Arabic. Customers switch between them on the card.</p>',
  '<p class="sub-lead">Elija hasta 3 idiomas para su tarjeta, como español, portugués, chino, japonés y árabe. Los clientes cambian entre ellos en la tarjeta.</p>', 1)
R('<span>English</span>\n<span lang="es">', '<span>English</span>\n<span lang="es">', 1)

# ---------- pricing ----------
R('<p class="kicker">Pricing</p>', '<p class="kicker">Precios</p>', 1)
R('<h2>Free setup. Just a small monthly fee.</h2>', '<h2>Instalación gratis. Solo una pequeña cuota mensual.</h2>', 1)
R('<p class="label">Design &amp; setup</p>', '<p class="label">Diseño e instalación</p>', 1)
R('<div class="big">Free</div>', '<div class="big">Gratis</div>', 1)
R('<p class="psub"><b>No setup fee.</b></p>', '<p class="psub"><b>Sin costo de instalación.</b></p>', 1)
for en, es in [('<li>Your logo and brand colors</li>','<li>Su logo y los colores de su marca</li>'),('<li>Call, text, WhatsApp, email, directions and website buttons</li>','<li>Botones de llamada, mensaje, WhatsApp, correo, direcciones y sitio web</li>'),
 ('<li>Hours, services and prices, photos, payment links</li>','<li>Horario, servicios y precios, fotos y enlaces de pago</li>'),('<li>QR code, Share and Save contact</li>','<li>Código QR, Compartir y Guardar contacto</li>'),
 ('<li>Up to 3 of 25 languages</li>','<li>Hasta 3 de 25 idiomas</li>'),('<li>Installs like an app on iPhone and Android, no app store</li>','<li>Se instala como una aplicación en iPhone y Android, sin tienda de aplicaciones</li>'),
 ('<li><b>Up to 3 free previews before you pay</b></li>','<li><b>Hasta 3 vistas previas gratis antes de pagar</b></li>'),
 ('<li>Hosting and security updates</li>','<li>Alojamiento y actualizaciones de seguridad</li>'),('<li>Unlimited changes to your hours, prices, photos and links</li>','<li>Cambios ilimitados en su horario, precios, fotos y enlaces</li>'),
 ('<li>Your QR code never changes, so printed codes keep working</li>','<li>Su código QR nunca cambia, así que los códigos impresos siguen funcionando</li>')]:
    R(en, es, 1)
R('<p class="label">Hosting &amp; updates</p>', '<p class="label">Alojamiento y actualizaciones</p>', 1)
R('<div class="big">$10<small> /month</small></div>', '<div class="big">$10<small> /mes</small></div>', 1)
R('<p class="psub">or <b>$100 per year</b>, 2 months free</p>', '<p class="psub">o <b>$100 al año</b>, 2 meses gratis</p>', 1)
R('<summary>Already approved your preview? Pay here</summary>', '<summary>¿Ya aprobó su vista previa? Pague aquí</summary>', 1)
R('Enter the unlock code we sent you with your preview. Use the same name, business name and phone you gave us. No preview yet? <a href="mailto:pedro_torres@torrestechremote.com">Ask for one first</a>, it’s free.',
  'Escriba el código de desbloqueo que le enviamos con su vista previa. Use el mismo nombre, nombre del negocio y teléfono que nos dio. ¿Aún no tiene vista previa? <a href="mailto:pedro_torres@torrestechremote.com">Pídala primero</a>, es gratis.', 1)
R('<label for="order-code">Unlock code</label>', '<label for="order-code">Código de desbloqueo</label>', 1)
R('placeholder="From your preview"', 'placeholder="De su vista previa"', 1)
R('type="submit">Unlock</button>', 'type="submit">Desbloquear</button>', 1)
R('<p>No code box? <a href="mailto:pedro_torres@torrestechremote.com">Email us</a> for your payment link.</p>', '<p>¿No ve el campo del código? <a href="mailto:pedro_torres@torrestechremote.com">Escríbanos</a> para recibir su enlace de pago.</p>', 1)
R('Your preview is ready to go live. At checkout, use the same name, business name and phone you gave us. Pick a plan:', 'Su vista previa está lista para publicarse. Al pagar, use el mismo nombre, nombre del negocio y teléfono que nos dio. Elija un plan:', 1)
R('>Make it live: $10/month</a>', '>Publicar mi tarjeta: $10/mes</a>', 1)
R('>Make it live: $100/year</a>', '>Publicar mi tarjeta: $100/año</a>', 1)
R('Card accepted online and in person. Cash in person for yearly plans. In-person service in the Ironbound, Newark NJ; online orders available in the US and its territories, and to US citizens abroad paying with a US card or bank account. See the <a href="/tos.html">Terms</a>.',
  'Se acepta tarjeta en línea y en persona. Efectivo en persona para los planes anuales. Servicio en persona en el Ironbound, Newark, NJ; pedidos en línea disponibles en EE. UU. y sus territorios, y para ciudadanos estadounidenses en el extranjero que paguen con una tarjeta o cuenta bancaria de EE. UU. Vea los <a href="/tos.html">Términos</a> (en inglés).', 1)
R('"That code doesn’t match. Check the code we sent with your preview."', '"Ese código no coincide. Revise el código que le enviamos con su vista previa."', 1)
R('"This browser can’t unlock the links. Email us for your payment link."', '"Este navegador no puede desbloquear los enlaces. Escríbanos para recibir su enlace de pago."', 1)

# ---------- teams ----------
R('<p class="kicker">For businesses</p>', '<p class="kicker">Para negocios</p>', 1)
R('<h2>Multiple locations or employees?</h2>', '<h2>¿Varios locales o empleados?</h2>', 1)
R('<p>Select the option that fits your organization, or combine them. Each business is different, so we provide a custom quote based on your number of locations and employees. Setup is free.</p>',
  '<p>Elija la opción que se ajuste a su organización, o combínelas. Cada negocio es distinto, por eso damos un presupuesto a la medida según su número de locales y empleados. La instalación es gratis.</p>', 1)
R('Run a gym or fitness studio? <a href="/digital-business-card-for-gyms/"><b>See the digital business card for gyms</b></a>.', '¿Tiene un gimnasio o un estudio de fitness? <a href="/es/tarjeta-digital-gimnasio/"><b>Vea la tarjeta de presentación digital para gimnasios</b></a>.', 1)
for en, es in [('<p class="label">Option 1</p>','<p class="label">Opción 1</p>'),('<p class="label">Option 2</p>','<p class="label">Opción 2</p>'),('<p class="label">Option 3</p>','<p class="label">Opción 3</p>'),
 ('<h3>Multiple locations</h3>','<h3>Varios locales</h3>'),('<h3>Single location, multiple employees</h3>','<h3>Un local, varios empleados</h3>'),('<h3>Multiple locations and employees</h3>','<h3>Varios locales y empleados</h3>'),
 ('<p>A single card lists every location, each with its own address, directions, phone number and hours. Suited to retail, fitness and multi-site businesses.</p>','<p>Una sola tarjeta muestra cada local, cada uno con su dirección, indicaciones, teléfono y horario. Ideal para comercios, fitness y negocios con varias sedes.</p>'),
 ('<p>Each employee receives an individual card with their name, photo and contact details. One office card lists the entire team.</p>','<p>Cada empleado recibe su propia tarjeta con su nombre, foto y datos de contacto. Una tarjeta de oficina muestra a todo el equipo.</p>'),
 ('<p>Multiple locations with individual employee cards. Each employee can be assigned to the location where they work.</p>','<p>Varios locales con tarjetas individuales de empleados. Cada empleado puede asignarse al local donde trabaja.</p>'),
 ('See an example: Corner Table Café','Ver un ejemplo: Corner Table Café'),('See an example: Harbor Realty','Ver un ejemplo: Harbor Realty'),('See an example: Brightside Dental','Ver un ejemplo: Brightside Dental'),
 ('>Request a quote: multiple locations</a>','>Pedir un presupuesto: varios locales (formulario en inglés)</a>'),('>Request a quote: multiple employees</a>','>Pedir un presupuesto: varios empleados (formulario en inglés)</a>'),('>Request a quote: both</a>','>Pedir un presupuesto: ambos (formulario en inglés)</a>')]:
    R(en, es, 1)
R('Prefer to talk? Call <a href="tel:+12017722106">(201) 772-2106</a> or email <a', '¿Prefiere hablar? Llame al <a href="tel:+12017722106">(201) 772-2106</a> o escriba a <a', 1)

# ---------- meet ----------
R('<p class="kicker">Who makes your card</p>', '<p class="kicker">Quién hace su tarjeta</p>', 1)
R('<h2>Hi, I’m Pedro.</h2>', '<h2>Hola, soy Pedro.</h2>', 1)
R('alt="Pedro Torres, founder of Torres Tech Remote"', 'alt="Pedro Torres, fundador de Torres Tech Remote"', 1)
R('I run Torres Tech Remote from the Ironbound, Newark. I make every card myself, and in the Ironbound I can come by your shop to set it up with you.', 'Dirijo Torres Tech Remote desde el Ironbound, en Newark. Hago cada tarjeta yo mismo, y en el Ironbound puedo pasar por su negocio para prepararla con usted.', 1)
R('I’m Pedro, the owner. Send me your business name and I’ll make you a free preview and send you a link to review. You only pay if you like it.', 'Soy Pedro, el dueño. Envíeme el nombre de su negocio y le haré una vista previa gratis con un enlace para que la revise. Solo paga si le gusta.', 1)
R('<a class="btn btn-ghost" href="mailto:pedro_torres@torrestechremote.com">Email Pedro</a>', '<a class="btn btn-ghost" href="mailto:pedro_torres@torrestechremote.com">Escribir a Pedro</a>', 1)
R('>Or fill in the form</a>', '>O llene el formulario</a>', 1)
R('<p class="contact-hint">Email works from a computer or a phone.</p>', '<p class="contact-hint">El correo funciona desde una computadora o un teléfono.</p>', 1)

# ---------- FAQ ----------
R('<p class="kicker">FAQ</p>', '<p class="kicker">Preguntas frecuentes</p>', 1)
R('<h2>Common questions.</h2>', '<h2>Preguntas comunes.</h2>', 1)
faq = [
('What does it cost?','¿Cuánto cuesta?','Design and setup are free. You pay $10 per month for hosting and updates, or $100 per year (2 months free). Up to 3 free previews before you pay. For several locations or employees, request a custom quote <a href="#teams">here</a>.','El diseño y la instalación son gratis. Usted paga $10 al mes por el alojamiento y las actualizaciones, o $100 al año (2 meses gratis). Hasta 3 vistas previas gratis antes de pagar. Para varios locales o empleados, pida <a href="#teams">aquí</a> un presupuesto a la medida.'),
('Which languages can my card show?','¿Qué idiomas puede mostrar mi tarjeta?','Up to 3 of 25 languages, like Spanish, Portuguese, Chinese, Japanese and Arabic. See the <a href="#languages">full list</a>.','Hasta 3 de 25 idiomas, como español, portugués, chino, japonés y árabe. Vea la <a href="#languages">lista completa</a>.'),
('Do my customers need to download an app?','¿Mis clientes tienen que descargar una aplicación?','No. The card opens from its link or QR code. Customers can also save it to their home screen like an app, no app store. On Android, open it in Chrome and tap <b>Add to home screen</b>, then <b>Install</b>. On iPhone or iPad, open it in Safari, tap <b>Share</b>, then <b>Add to Home Screen</b>. <a href="#install">See the steps</a>.','No. La tarjeta se abre desde su enlace o código QR. Los clientes también pueden guardarla en la pantalla de inicio como una aplicación, sin tienda de aplicaciones. En Android, ábrala en Chrome y toque <b>Añadir a pantalla de inicio</b>, luego <b>Instalar</b>. En iPhone o iPad, ábrala en Safari, toque <b>Compartir</b> y luego <b>Añadir a pantalla de inicio</b>. <a href="#install">Vea los pasos</a>.'),
('Can customers book, order or get a quote from my card?','¿Pueden mis clientes reservar, pedir o cotizar desde mi tarjeta?','Yes. Your card’s main button, like Book now, Order online or Get a quote, opens the booking, ordering or quote page you already use, such as Square, Booksy, OpenTable or DoorDash. Or it can call, text or WhatsApp you. It works for barbers and salons, cafés and restaurants, contractors, pest control and more.','Sí. El botón principal de su tarjeta, como Reservar, Pedir en línea u Obtener presupuesto, abre la página de reservas, pedidos o presupuestos que ya usa, como Square, Booksy, OpenTable o DoorDash. O puede llamarle, escribirle o enviarle un WhatsApp. Sirve para barberías y salones, cafés y restaurantes, contratistas, control de plagas y más.'),
('Can I change my hours or prices later?','¿Puedo cambiar mi horario o mis precios después?','Yes. Hosting includes unlimited changes to your hours, prices, photos and links. Your QR code never changes, so printed codes keep working.','Sí. El alojamiento incluye cambios ilimitados en su horario, precios, fotos y enlaces. Su código QR nunca cambia, así que los códigos impresos siguen funcionando.'),
('How do I pay?','¿Cómo pago?','Card accepted online and in person. Cash in person for yearly plans. After you approve your free preview, pay online with the <a data-open-order="" href="#order">payment links</a>.','Se acepta tarjeta en línea y en persona. Efectivo en persona para los planes anuales. Después de aprobar su vista previa gratis, pague en línea con los <a data-open-order="" href="#order">enlaces de pago</a>.'),
('Can one card cover several locations?','¿Una tarjeta puede cubrir varios locales?','Yes. One card lists every location, each with its own address, directions, phone number and hours. Each location can also have its own QR code, so a customer who scans it at that location lands on that location. See the <a href="#teams">examples</a>.','Sí. Una tarjeta muestra cada local, cada uno con su dirección, indicaciones, teléfono y horario. Cada local también puede tener su propio código QR, así el cliente que lo escanea en ese local llega a ese local. Vea los <a href="#teams">ejemplos</a>.'),
('Can each of my employees have their own card?','¿Cada uno de mis empleados puede tener su propia tarjeta?','Yes. Each employee receives an individual card with their name, photo and contact details. One office card lists the entire team, and each person can be assigned to the location where they work.','Sí. Cada empleado recibe su propia tarjeta con su nombre, foto y datos de contacto. Una tarjeta de oficina muestra a todo el equipo, y cada persona puede asignarse al local donde trabaja.'),
('How much does it cost for several locations or employees?','¿Cuánto cuesta con varios locales o empleados?','Each business is different, so we provide a custom quote based on your number of locations and employees. Setup is free. <a href="https://docs.google.com/forms/d/e/1FAIpQLSenglfDQ0WaNQpeYR2ZBD-Y4AP6W5HduUZSNqFPebuN1tnx-Q/viewform" rel="noopener nofollow" target="_blank">Request a quote</a>.','Cada negocio es distinto, por eso damos un presupuesto a la medida según su número de locales y empleados. La instalación es gratis. <a href="https://docs.google.com/forms/d/e/1FAIpQLSenglfDQ0WaNQpeYR2ZBD-Y4AP6W5HduUZSNqFPebuN1tnx-Q/viewform" rel="noopener nofollow" target="_blank">Pida un presupuesto</a> (formulario en inglés).'),
('What happens when we add or lose an employee?','¿Qué pasa si agregamos o perdemos un empleado?','You can add people at any time and they are billed for the rest of that year. If someone leaves, you can give their place to a new person at no charge. Please tell us by the 1st of the month, and we make the change that week.','Puede agregar personas en cualquier momento y se les cobra por el resto de ese año. Si alguien se va, puede darle su lugar a otra persona sin costo. Avísenos antes del día 1 del mes y hacemos el cambio esa semana.'),
('What if one of my locations is a franchise?','¿Y si uno de mis locales es una franquicia?','A location owned by another business is a separate customer with its own card and its own bill. It can link back to your main card if you both agree.','Un local que pertenece a otro negocio es un cliente aparte, con su propia tarjeta y su propia factura. Puede enlazar de vuelta a su tarjeta principal si ambos están de acuerdo.'),
('Who can order a card?','¿Quién puede pedir una tarjeta?','In-person service in the Ironbound, Newark NJ; online orders available in the US and its territories, and to US citizens abroad paying with a US card or bank account.','Servicio en persona en el Ironbound, Newark, NJ; pedidos en línea disponibles en EE. UU. y sus territorios, y para ciudadanos estadounidenses en el extranjero que paguen con una tarjeta o cuenta bancaria de EE. UU.'),
]
for qe, qs, ae, as_ in faq:
    R(f'<summary>{qe}</summary>\n<div class="faq-answer">{ae}</div>', f'<summary>{qs}</summary>\n<div class="faq-answer">{as_}</div>', 1)

# ---------- final CTA + footer (same text as the Spanish home page) ----------
R('<h2>See your card before you pay.</h2>', '<h2>Vea su tarjeta antes de pagar.</h2>', 1)
R('Call, email or fill in a short form, and we’ll make you a free preview. Up to 3 free previews. You only pay when you’re happy with it.', 'Llame, escriba o llene un formulario corto y le haremos una vista previa gratis. Hasta 3 vistas previas gratis. Solo paga cuando esté contento con el resultado.', 1)
body = ("Hola, me gustaría una vista previa gratis de una tarjeta de presentación digital.\n\nNombre del negocio: \nTeléfono del negocio: \nCorreo del negocio: \nDirección o zona: \nHorario: \n"
        "Servicios (y precios, si quiere que se muestren): \nCómo reservan, piden o cotizan los clientes (enlace de una aplicación, o llamada/mensaje/WhatsApp): \nColores de la marca (si los hay): \nSitio web, Instagram o Facebook (si los hay): \n\nAdjunte su logo y unas fotos si los tiene.")
subj = "Vista previa gratis: tarjeta de presentación digital"
s, n = re.subn(r'href="mailto:pedro_torres@torrestechremote\.com\?subject=[^"]*"', 'href="mailto:pedro_torres@torrestechremote.com?subject=%s&amp;body=%s"' % (urllib.parse.quote(subj, safe=""), urllib.parse.quote(body, safe="")), s); assert n == 1
s, n = re.subn(r'(<a class="btn btn-out" href="mailto:[^"]*">)[^<]*(</a>)', r'\1O escríbanos por correo\2', s); assert n == 1
R('<small>See it live: <a href', '<small>Véalo en vivo: <a href', 1)
R('rel="noopener" target="_blank">demo card</a> · ', 'rel="noopener" target="_blank">tarjeta de demostración</a> · ', 1)
R('>our own card</a>', '>nuestra propia tarjeta</a>', 1)
R('<p>Digital Business Cards · Ironbound, Newark, NJ</p>', '<p>Tarjetas de presentación digitales · Ironbound, Newark, NJ</p>', 1)
R('<a href="/">Home</a>', '<a href="/es/">Inicio</a>', 1)
R('<a href="/digital-business-card-for-gyms/">Cards for gyms</a>', '<a href="/es/tarjeta-digital-gimnasio/">Tarjetas para gimnasios</a>', 1)
R('">Contact</a>', '">Contacto</a>', 1)
R('>Terms</a>', '>Términos</a>', 1); R('>Privacy</a>', '>Privacidad</a>', 1)
R('<h3>Follow</h3>', '<h3>Síganos</h3>', 1)
R('>Review us on Google</a>', '>Reseñe en Google</a>', 1)

# quote buttons go to the free-preview form in this language (same as the gym pages)
s = s.replace('https://docs.google.com/forms/d/e/1FAIpQLSenglfDQ0WaNQpeYR2ZBD-Y4AP6W5HduUZSNqFPebuN1tnx-Q/viewform', '/go/preview-es.html')
s = s.replace(' (formulario en inglés)', '')

# full hreflang set (en, es, pt-PT, x-default) on every language version of the sales page
s = re.sub(r'<link href="[^"]*" hreflang="[^"]*" rel="alternate"/>\n?', '', s)
s = re.sub(r'(<link href="[^"]*" rel="canonical"/>)', lambda m: m.group(1) + '\n' + '<link href="https://torrestechremote.com/digital-business-cards.html" hreflang="en" rel="alternate"/>\n<link href="https://torrestechremote.com/es/tarjetas-de-presentacion-digitales/" hreflang="es" rel="alternate"/>\n<link href="https://torrestechremote.com/pt/cartoes-de-visita-digitais/" hreflang="pt-PT" rel="alternate"/>\n<link href="https://torrestechremote.com/digital-business-cards.html" hreflang="x-default" rel="alternate"/>', s, count=1)

out = root / "es" / "tarjetas-de-presentacion-digitales" / "index.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(s, encoding="utf-8")
print("wrote", out, len(s))
