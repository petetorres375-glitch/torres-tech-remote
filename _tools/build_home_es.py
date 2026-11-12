#!/usr/bin/env python3
"""Builds es/index.html (Spanish home page) from the English index.html. Safe to re-run; only writes es/index.html."""
import re, urllib.parse, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
s = (root / "index.html").read_text(encoding="utf-8")
s = re.sub(r'<link href="[^"]*" hreflang="[^"]*" rel="alternate"/>\n', "", s)  # English page now has its own; each build adds the full set
s = re.sub(r'<nav class="langs".*?</nav>\n', "", s, flags=re.S)  # drop English page\'s switch; each build adds its own
s = re.sub(r'\.langs\{[^\n]*?\.langs b\{[^\n]*?\}\n', "", s)

def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, f"expected {count} of {old[:60]!r}, found {n}"
    s = s.replace(old, new)

# ---- head ----
rep('<html lang="en">', '<html lang="es">')
T = "Torres Tech Remote | Tarjetas de presentación digitales para pequeños negocios en todo EE. UU."
rep("<title>Torres Tech Remote | Digital Business Cards for Small Businesses Across the U.S.</title>", f"<title>{T}</title>")
D = "Tarjetas de presentación digitales para pequeños negocios en todo EE. UU.: un enlace y un código QR para cada local, una tarjeta para cada persona, y nosotros hacemos sus actualizaciones. Instalación gratis, luego $10/mes. Vista previa gratis antes de pagar."
rep('<meta content="Digital business cards for small businesses across the U.S.: one link and one QR code for every location, a card for each person, and we do your updates. Free setup, then $10/month. Free preview before you pay." name="description"/>',
    f'<meta content="{D}" name="description"/>')
rep('<link href="https://torrestechremote.com/" rel="canonical"/>',
    '<link href="https://torrestechremote.com/es/" rel="canonical"/>\n<link href="https://torrestechremote.com/" hreflang="en" rel="alternate"/>\n<link href="https://torrestechremote.com/es/" hreflang="es" rel="alternate"/>\n<link href="https://torrestechremote.com/pt/" hreflang="pt-PT" rel="alternate"/>\n<link href="https://torrestechremote.com/" hreflang="x-default" rel="alternate"/>')
rep('<meta content="https://torrestechremote.com/" property="og:url"/>', '<meta content="https://torrestechremote.com/es/" property="og:url"/>')
OT = "Torres Tech Remote | Tarjetas de presentación digitales para su negocio, cada local y su equipo"
OD = "Para pequeños negocios en todo EE. UU.: un enlace y un código QR para cada local, una tarjeta para cada persona, y nosotros hacemos sus actualizaciones. Instalación gratis, luego $10/mes. Vista previa gratis antes de pagar."
rep('<meta content="Torres Tech Remote | Digital Business Cards for Your Business, Every Location and Team" property="og:title"/>', f'<meta content="{OT}" property="og:title"/>')
rep('<meta content="For small businesses across the U.S.: one link and one QR code for each location, a card for each person, and we do your updates. Free setup, then $10/month. Free preview before you pay." property="og:description"/>', f'<meta content="{OD}" property="og:description"/>')
rep('<meta content="Torres Tech Remote: digital business cards for small businesses across the U.S., for one business, every location, and your whole team" property="og:image:alt"/>',
    '<meta content="Torres Tech Remote: tarjetas de presentación digitales para pequeños negocios en todo EE. UU., para un negocio, cada local y todo su equipo" property="og:image:alt"/>')
rep('<meta content="Torres Tech Remote | Digital Business Cards for Your Business, Every Location and Team" name="twitter:title"/>', f'<meta content="{OT}" name="twitter:title"/>')
rep('<meta content="For small businesses across the U.S.: one link and one QR code for each location, a card for each person, and we do your updates. Free setup, then $10/month. Free preview before you pay." name="twitter:description"/>', f'<meta content="{OD}" name="twitter:description"/>')
# JSON-LD
rep('"url": "https://torrestechremote.com/",\n      "publisher"', '"url": "https://torrestechremote.com/",\n      "inLanguage": ["en", "es", "pt-PT"],\n      "publisher"')
rep('"@id": "https://torrestechremote.com/#webpage",\n      "url": "https://torrestechremote.com/",\n      "name": "Torres Tech Remote: digital business cards",',
    '"@id": "https://torrestechremote.com/es/#webpage",\n      "url": "https://torrestechremote.com/es/",\n      "inLanguage": "es",\n      "name": "Torres Tech Remote: tarjetas de presentación digitales",')

# language switch (English / Español; Português added when that page exists)
rep('</style>\n</head>', '.langs{display:flex;gap:12px;font-size:14px;align-items:center;margin-right:6px}.langs a{color:var(--muted,#65717e);text-decoration:none}.langs a:hover{text-decoration:underline}.langs b{color:var(--navy,#12192d)}\n</style>\n</head>')
rep('<div class="nav-right">\n', '<div class="nav-right">\n<nav class="langs" aria-label="Idioma"><a href="/" hreflang="en" lang="en">English</a><b aria-current="page">Español</b><a href="/pt/" hreflang="pt-PT" lang="pt-PT">Português</a></nav>\n')

# ---- absolute asset paths (page now lives in /es/) ----
s = s.replace('src="img/', 'src="/img/').replace('src="comptia-a-certification.7.png"', 'src="/comptia-a-certification.7.png"')
rep('href="tos.html"', 'href="/tos.html"'); rep('href="privacy.html"', 'href="/privacy.html"')
rep('<a class="brand" href="/">', '<a class="brand" href="/es/">', 2)

# free-preview buttons always open the Spanish form on this page
s = s.replace('href="/go/preview.html"', 'href="/go/preview-es.html"')

# ---- header ----
rep('rel="noopener" target="_blank">Demo card</a>', 'rel="noopener" target="_blank">Tarjeta de demostración</a>')
rep('<a class="navlink" href="/digital-business-cards.html#pricing">Pricing</a>', '<a class="navlink" href="/digital-business-cards.html#pricing">Precios</a>')
rep('<a class="navlink" href="/digital-business-cards.html#faq">FAQ</a>', '<a class="navlink" href="/digital-business-cards.html#faq">Preguntas frecuentes</a>')
rep('target="_blank">Free preview</a>', 'target="_blank">Vista previa gratis</a>')
rep('href="tel:+12017722106">Call</a>', 'href="tel:+12017722106">Llamar</a>')

# ---- hero ----
rep('Digital Business Cards · Newark, NJ', 'Tarjetas de presentación digitales · Newark, NJ')
rep('<h1>A business card your customers <em>keep on their phone.</em></h1>', '<h1>Una tarjeta de presentación que sus clientes <em>guardan en el teléfono.</em></h1>')
rep("One link and one QR code for your shop. Customers call, text, WhatsApp or email you in one tap and save you to their contacts. Your card opens in your customer's own phone language, and they can tap to switch. We design it, host it and keep it up to date. You never touch an app.",
    "Un enlace y un código QR para su negocio. Sus clientes le llaman, le escriben, le envían un WhatsApp o un correo con un solo toque, y le guardan en sus contactos. Su tarjeta se abre en el idioma del teléfono de cada cliente, y ellos pueden tocar para cambiarlo. Nosotros la diseñamos, la alojamos y la mantenemos al día. Usted nunca toca una aplicación.")
rep('>Call (201) 772-2106</a>', '>Llamar al (201) 772-2106</a>', 2)
rep('Hi%20Pedro%2C%20I%27d%20like%20a%20free%20preview%20for%20my%20business%3A%20', urllib.parse.quote("Hola Pedro, me gustaría una vista previa gratis para mi negocio: ", safe=""), 2)
rep('>Text Pedro</a>', '>Escribir a Pedro</a>', 2)
rep('>Request your free preview</a>', '>Pida su vista previa gratis</a>', 3)
rep('Call and Text open on your phone. Email works from a computer or a phone.</p>\n<p class="contact-hint">Free preview.', 'Llamar y Escribir se abren en su teléfono. El correo funciona desde una computadora o un teléfono.</p>\n<p class="contact-hint">Free preview.')
rep('Call and Text open on your phone. Email works from a computer or a phone.', 'Llamar y Escribir se abren en su teléfono. El correo funciona desde una computadora o un teléfono.')
rep('Free preview. No payment or credit card required. Just your name, business name, phone, and email to get started.', 'Vista previa gratis. Sin pago ni tarjeta de crédito. Solo su nombre, el nombre del negocio, teléfono y correo para empezar.', 2)
rep('alt="Pedro Torres, owner of Torres Tech Remote"', 'alt="Pedro Torres, dueño de Torres Tech Remote"')
rep('>Email Pedro</a> · ', '>Escribir a Pedro por correo</a> · ')
rep('target="_blank">See the demo card</a>', 'target="_blank">Ver la tarjeta de demostración</a>')
# remove the old trilingual tagline block
s, n = re.subn(r'<div class="tri">.*?</div>\n', '', s, flags=re.S); assert n == 1

# ---- phones ----
rep('alt="Torres Tech Remote\'s own digital business card on a phone: TTR logo, See a demo card button, call, text, WhatsApp, email and website buttons, Share, Save contact, Show QR code, and opening hours"',
    'alt="La tarjeta de presentación digital de Torres Tech Remote en un teléfono: logo de TTR, botón para ver una tarjeta de demostración, botones de llamada, mensaje, WhatsApp, correo y sitio web, Compartir, Guardar contacto, Mostrar código QR y horario"')
rep('<b>Our own card</b>', '<b>Nuestra propia tarjeta</b>')
rep('alt="Demo digital business card for a barbershop on a phone: logo, Book now button, call, text, WhatsApp, email, directions and website buttons, Save contact, Show QR code, and opening hours"',
    'alt="Tarjeta de presentación digital de demostración de una barbería en un teléfono: logo, botón de reservar, botones de llamada, mensaje, WhatsApp, correo, direcciones y sitio web, Guardar contacto, Mostrar código QR y horario"')
rep('<b>Demo card</b> for a made-up barbershop', '<b>Tarjeta de demostración</b> de una barbería inventada')

# ---- trust bar ----
rep('<b>Free setup</b>', '<b>Instalación gratis</b>')
rep('<span>$10/month or $100/year</span>', '<span>$10/mes o $100/año</span>')
rep('<span>Up to 3 free previews</span>', '<span>Hasta 3 vistas previas gratis</span>')
rep('In-person service in the Ironbound, Newark NJ.', 'Servicio en persona en el Ironbound, Newark, NJ.')
rep('</svg>Now on Facebook</a>', '</svg>Ahora en Facebook</a>')

# ---- offers ----
rep('<p class="kicker">Choose what fits</p>', '<p class="kicker">Elija lo que le conviene</p>')
rep('<h2>One card, or a card for every location and employee.</h2>', '<h2>Una tarjeta, o una tarjeta para cada local y cada empleado.</h2>')
rep('<p>Setup is free. See your card before you pay, with up to 3 free previews.</p>', '<p>La instalación es gratis. Vea su tarjeta antes de pagar, con hasta 3 vistas previas gratis.</p>')
rep('<p class="label">One business</p>', '<p class="label">Un negocio</p>')
rep('<h3>One card for your business</h3>', '<h3>Una tarjeta para su negocio</h3>')
rep('Your logo and brand colors, call, text, WhatsApp, email, directions and website buttons, hours, services and prices, payment links, and a QR code that never changes. Free setup, then $10/month or $100/year.',
    'Su logo y los colores de su marca, botones de llamada, mensaje, WhatsApp, correo, direcciones y sitio web, horarios, servicios y precios, enlaces de pago y un código QR que nunca cambia. Instalación gratis, luego $10/mes o $100/año.')
rep('>See how it works and pricing</a>', '>Vea cómo funciona y los precios</a>')
rep('<p class="label">Locations and teams</p>', '<p class="label">Locales y equipos</p>')
rep('<h3>Multiple locations or employees</h3>', '<h3>Varios locales o empleados</h3>')
rep('A single card can list every location with its own address, phone and hours, and each employee can have an individual card with their name, photo and contact details. Each business is different, so we provide a custom quote. Setup is free.',
    'Una sola tarjeta puede mostrar cada local con su propia dirección, teléfono y horario, y cada empleado puede tener su tarjeta con su nombre, foto y datos de contacto. Cada negocio es distinto, por eso damos un presupuesto a la medida. La instalación es gratis.')
rep('>Request a quote</a>', '>Pedir un presupuesto (formulario en inglés)</a>')
rep('>See examples</a>', '>Ver ejemplos</a>')
rep('Run a gym or fitness studio? <a href="/digital-business-card-for-gyms/"><b>See the digital business card for gyms</b></a>.',
    '¿Tiene un gimnasio o un estudio de fitness? <a href="/es/tarjeta-digital-gimnasio/"><b>Vea la tarjeta de presentación digital para gimnasios</b></a>.')
rep('Prefer to talk? Call <a href="tel:+12017722106">(201) 772-2106</a> or email <a', '¿Prefiere hablar? Llame al <a href="tel:+12017722106">(201) 772-2106</a> o escriba a <a')

# ---- meet ----
rep('<p class="kicker">About Torres Tech Remote</p>', '<p class="kicker">Sobre Torres Tech Remote</p>')
rep('<h2>Hi, I’m Pedro.</h2>', '<h2>Hola, soy Pedro.</h2>')
rep('alt="Pedro Torres, founder of Torres Tech Remote"', 'alt="Pedro Torres, fundador de Torres Tech Remote"')
rep('I run Torres Tech Remote from the Ironbound, Newark. I make every card myself, and in the Ironbound I can come by your shop to set it up with you.',
    'Dirijo Torres Tech Remote desde el Ironbound, en Newark. Hago cada tarjeta yo mismo, y en el Ironbound puedo pasar por su negocio para prepararla con usted.')
rep('I’m Pedro, the owner. Send me your business name and I’ll make you a free preview and send you a link to review. You only pay if you like it.',
    'Soy Pedro, el dueño. Envíeme el nombre de su negocio y le haré una vista previa gratis con un enlace para que la revise. Solo paga si le gusta.')
rep('<a class="btn btn-ghost" href="mailto:pedro_torres@torrestechremote.com">Email Pedro</a>', '<a class="btn btn-ghost" href="mailto:pedro_torres@torrestechremote.com">Escribir a Pedro</a>')
rep('>Or fill in the form</a>', '>O llene el formulario</a>')
rep('<p class="contact-hint">Email works from a computer or a phone.</p>', '<p class="contact-hint">El correo funciona desde una computadora o un teléfono.</p>')
rep('alt="CompTIA A+ Certified"', 'alt="Técnico de TI certificado CompTIA A+"')
rep('<b>CompTIA A+ Certified</b>', '<b>Técnico de TI certificado CompTIA A+</b>')
rep('IT Technician — Hardware &amp; Software Support. Industry-recognized certification covering troubleshooting, networking, and system configuration.',
    'Soporte de hardware y software. Certificación reconocida en la industria que cubre solución de problemas, redes y configuración de sistemas.')

# ---- final ----
rep('<h2>See your card before you pay.</h2>', '<h2>Vea su tarjeta antes de pagar.</h2>')
rep('Call, email or fill in a short form, and we’ll make you a free preview. Up to 3 free previews. You only pay when you’re happy with it.',
    'Llame, escriba o llene un formulario corto y le haremos una vista previa gratis. Hasta 3 vistas previas gratis. Solo paga cuando esté contento con el resultado.')
rep('>Or email us</a>', '>O escríbanos por correo</a>') if '>Or email us</a>' in s else None
# the mailto button text
s, n = re.subn(r'(<a class="btn btn-out" href="mailto:[^"]*">)[^<]*(</a>)', r'\1O escríbanos por correo\2', s); assert n >= 1
body = ("Hola, me gustaría una vista previa gratis de una tarjeta de presentación digital.\n\nNombre del negocio: \nTeléfono del negocio: \nCorreo del negocio: \nDirección o zona: \nHorario: \n"
        "Servicios (y precios, si quiere que se muestren): \nCómo reservan, piden o cotizan los clientes (enlace de una aplicación, o llamada/mensaje/WhatsApp): \nColores de la marca (si los hay): \nSitio web, Instagram o Facebook (si los hay): \n\nAdjunte su logo y unas fotos si los tiene.")
subj = "Vista previa gratis: tarjeta de presentación digital"
s, n = re.subn(r'href="mailto:pedro_torres@torrestechremote\.com\?subject=[^"]*"',
               'href="mailto:pedro_torres@torrestechremote.com?subject=%s&amp;body=%s"' % (urllib.parse.quote(subj, safe=""), urllib.parse.quote(body, safe="")), s); assert n == 1
rep('<small>See it live: <a href', '<small>Véalo en vivo: <a href')
rep('rel="noopener" target="_blank">demo card</a> · ', 'rel="noopener" target="_blank">tarjeta de demostración</a> · ')
rep('>our own card</a>', '>nuestra propia tarjeta</a>')

# ---- footer ----
rep('<p>Digital Business Cards · Ironbound, Newark, NJ</p>', '<p>Tarjetas de presentación digitales · Ironbound, Newark, NJ</p>')
rep('<a href="/">Home</a>', '<a href="/es/">Inicio</a>')
rep('<a href="/digital-business-cards.html">Digital business cards</a>', '<a href="/digital-business-cards.html">Tarjetas de presentación digitales</a>')
rep('<a href="/digital-business-card-for-gyms/">Cards for gyms</a>', '<a href="/es/tarjeta-digital-gimnasio/">Tarjetas para gimnasios</a>')
rep('">Contact</a>', '">Contacto</a>')
rep('>Terms</a>', '>Términos</a>'); rep('>Privacy</a>', '>Privacidad</a>')
rep('<h3>Follow</h3>', '<h3>Síganos</h3>')
rep('>Review us on Google</a>', '>Reseñe en Google</a>')

# links to the sales page -> Spanish sales page
s = s.replace('href="/digital-business-cards.html', 'href="/es/tarjetas-de-presentacion-digitales/')

# quote buttons go to the free-preview form in this language (same as the gym pages)
s = s.replace('https://docs.google.com/forms/d/e/1FAIpQLSenglfDQ0WaNQpeYR2ZBD-Y4AP6W5HduUZSNqFPebuN1tnx-Q/viewform', '/go/preview-es.html')
s = s.replace(' (formulario en inglés)', '')

out = root / "es" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(s, encoding="utf-8")
print("wrote", out, len(s))
