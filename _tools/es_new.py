"""Spanish for the new one-page home. Used by build_home_es.py.

TRANSLATIONS: exact English text of one text node (or alt/aria-label) -> Spanish.
RAW: (English HTML piece, Spanish HTML piece) swaps done before the text pass (inline links, order changes).
KEEP: visible text that stays as it is (names, numbers, language names).
PAGE(s): page-level changes (html lang, head, links, language switch).
New Spanish is for Pedro to proofread; reused Spanish (es_legacy_pairs.json) was proofread before.
"""
import urllib.parse

KEEP = {"Torres Tech Remote", "Android", "iPhone", "Chrome", "Safari", "ES", "EN", "PT", "Alpha Fit Club", "Keon Torres",
        "English", "Español", "Português", "Português (BR)", "Português (PT)", "Deutsch", "Français", "Italiano",
        "Nederlands", "Polski", "Română", "Svenska", "Türkçe", "Bahasa Indonesia", "Čeština", "Tiếng Việt", "Ελληνικά",
        "Русский", "Українська", "العربية", "עברית", "हिन्दी", "日本語", "한국어", "ไทย", "简体中文",
        "pedro_torres@torrestechremote.com", "WhatsApp", "LINE", "Facebook", "Instagram", "YouTube", "QR", "TTR", "OK"}

TRANSLATIONS = {}
TRANSLATIONS.update({
"Video: on an iPhone, open the card in Safari, tap Add to home screen on the card, tap Share, tap Add to Home Screen, tap Add, and the card's icon appears on the home screen": "Video: en un iPhone, abra la tarjeta en Safari, toque Añadir a pantalla de inicio en la tarjeta, toque Compartir, toque Añadir a pantalla de inicio, toque Añadir, y el ícono de la tarjeta aparece en la pantalla de inicio",
"Social links": "Redes sociales", "Torres Tech Remote social links": "Redes sociales de Torres Tech Remote",
"Google review": "Reseña de Google",
"Alpha Fit Club digital card": "Tarjeta digital de Alpha Fit Club", "Keon Torres digital card": "Tarjeta digital de Keon Torres",
"A digital business card QR code": "Código QR de una tarjeta de presentación digital",
"Alpha Fit Club card screenshots": "Capturas de la tarjeta de Alpha Fit Club", "Keon Torres card screenshots": "Capturas de la tarjeta de Keon Torres",
"Previous Alpha Fit Club screenshot": "Captura anterior de Alpha Fit Club", "Next Alpha Fit Club screenshot": "Captura siguiente de Alpha Fit Club",
"Choose a Alpha Fit Club screenshot": "Elegir una captura de Alpha Fit Club",
"Previous Keon Torres screenshot": "Captura anterior de Keon Torres", "Next Keon Torres screenshot": "Captura siguiente de Keon Torres",
"Step 1": "Paso 1", "Step 2": "Paso 2", "Step 3": "Paso 3",
"Email Pedro": "Correo a Pedro",
"Install": "Instalar", "Share": "Compartir", "Add": "Añadir", "Save contact": "Guardar contacto", "Import": "Importar",
"(some phones say": "(algunos teléfonos dicen", "Save": "Guardar",
"Newark, NJ location": "Local de Newark, NJ",
"Night · English": "Noche · Inglés", "Day · English": "Día · Inglés", "Night · Spanish": "Noche · Español", "Day · Spanish": "Día · Español",
"Night · Japanese": "Noche · Japonés", "Day · Japanese": "Día · Japonés", "Night · Vietnamese": "Noche · Vietnamita", "Day · Vietnamese": "Día · Vietnamita",
"Book first class": "Reservar primera clase", "opens booking page": "abre la página de reservas",
"Call": "Llamar", "Text": "Mensaje", "starts a text": "inicia un mensaje de texto", "Email": "Correo", "Directions": "Direcciones",
"switches language": "cambia el idioma", "Day / Night": "Día / Noche", "QR code": "Código QR", "opens a chat": "abre un chat",
"No setup fee.": "Sin costo de instalación.",
"Option 1": "Opción 1", "Option 2": "Opción 2", "Option 3": "Opción 3",
"Multiple locations": "Varios locales", "Single location, multiple employees": "Un local, varios empleados",
"Request a quote: multiple locations": "Pedir un presupuesto: varios locales",
"Request a quote: multiple employees": "Pedir un presupuesto: varios empleados",
"Request a quote: both": "Pedir un presupuesto: ambos",
"Español:": "English:",
"Su tarjeta de presentación en el teléfono de sus clientes. Instalación gratis, vista previa gratis.": "Your business card on your customers' phones. Free setup, free preview.",
"Pricing": "Precios",
"FAQ": "Preguntas frecuentes",
"Languages": "Idiomas",
"Design & setup": "Diseño e instalación",
"Hosting & updates": "Alojamiento y actualizaciones",
"Show all": "Ver todas",
"What's on your card": "Qué lleva su tarjeta",
"How it works": "Cómo funciona",
"Digital business cards · Newark, NJ · online across the U.S.": "Tarjetas de presentación digitales · Newark, NJ · en línea en todo EE. UU.",
"Get my free preview →": "Quiero mi vista previa gratis →",
"Facebook (opens in a new tab)": "Facebook (se abre en una pestaña nueva)",
"Instagram (opens in a new tab)": "Instagram (se abre en una pestaña nueva)",
"YouTube (opens in a new tab)": "YouTube (se abre en una pestaña nueva)",
"Google review (opens in a new tab)": "Reseña de Google (se abre en una pestaña nueva)",
"Free preview.": "Vista previa gratis.",
"No payment or credit card required. Just your name, business name, phone and email.": "Sin pago ni tarjeta de crédito. Solo su nombre, el nombre del negocio, teléfono y correo.",
"Free setup": "Instalación gratis",
"or $100/year": "o $100/año",
"Up to 3 free previews": "Hasta 3 vistas previas gratis",
"pay only if you approve": "solo paga si aprueba",
"no setup fee": "sin costo de instalación",
"$10/month": "$10/mes",
"YOUR CARD, YOUR BRAND": "SU TARJETA, SU MARCA",
"Real cards": "Tarjetas reales",
"Open the Alpha Fit Club card": "Abrir la tarjeta de Alpha Fit Club",
"Open the Torres Tech Remote card": "Abrir la tarjeta de Torres Tech Remote",
"Open the Keon Torres card": "Abrir la tarjeta de Keon Torres",
"Torres Tech Remote's own digital business card": "La tarjeta de presentación digital de Torres Tech Remote",
"$10/month or $100/year": "$10/mes o $100/año",
"In-person service in the Ironbound, Newark NJ ·": "Servicio en persona en el Ironbound, Newark, NJ ·",
"Now on Facebook": "Ahora en Facebook",
"Tap any card above to try the real thing.": "Toque cualquiera de las tarjetas de arriba para probar la real.",
"Alpha Fit Club brand shown on the card": "La marca de Alpha Fit Club en la tarjeta",
"One-tap buttons on a digital card": "Botones de un toque en una tarjeta digital",
"Business hours and service pricing on a card": "Horario y precios de servicios en una tarjeta",
"Photo gallery on the Alpha Fit Club card": "Galería de fotos en la tarjeta de Alpha Fit Club",
"Your photos": "Sus fotos",
"Show your place, your work or your team in a photo gallery customers can swipe.": "Muestre su local, su trabajo o su equipo en una galería de fotos que los clientes pueden deslizar.",
"Torres Tech Remote card with Facebook, Instagram, YouTube, video and Leave a review buttons": "Tarjeta de Torres Tech Remote con botones de Facebook, Instagram, YouTube, videos y Reseñe en Google",
"Your socials and reviews": "Sus redes y reseñas",
"Facebook, Instagram, YouTube, your videos, your website and a Leave a review button, so customers can follow you.": "Facebook, Instagram, YouTube, sus videos, su sitio web y un botón para dejar una reseña, para que los clientes puedan seguirle.",
"English and Spanish versions of the Alpha Fit Club card": "Versiones en inglés y español de la tarjeta de Alpha Fit Club",
"Alpha Fit Club November events promotion on the card": "Promoción de eventos de noviembre de Alpha Fit Club en la tarjeta",
"Alpha Fit Club promotional poster on the card": "Cartel promocional de Alpha Fit Club en la tarjeta",
"Easy to share, and it lasts": "Fácil de compartir, y dura",
"QR code, Share and Save contact. Your QR code never changes, so printed codes keep working.": "Código QR, Compartir y Guardar contacto. Su código QR nunca cambia, así que los códigos impresos siguen funcionando.",
"Works like an app": "Funciona como una aplicación",
"Customers save your card to their phone in a few taps. It gets its own icon, opens full screen like an app, and still opens without internet. No app store and no download. Pick your phone to watch how:": "Los clientes guardan su tarjeta en el teléfono en unos toques. Tiene su propio ícono, se abre a pantalla completa como una aplicación y abre incluso sin internet. Sin tienda de aplicaciones y sin descargar nada. Elija su teléfono para ver cómo:",
"Open the card in": "Abra la tarjeta en",
"Tap": "Toque",
"Add to home screen": "Añadir a pantalla de inicio",
"on the card.": "en la tarjeta.",
"(iPhone or iPad).": "(iPhone o iPad).",
"(the square with an arrow).": "(el cuadrado con una flecha).",
"Add to Home Screen": "Añadir a pantalla de inicio",
", then": ", y luego",
"Saved in their contacts": "Guardado en sus contactos",
"“Save contact” adds your business to their contacts with your logo, phone, email, address and website, so they can find you and call you later. Pick your phone to watch how:": "“Guardar contacto” agrega su negocio a los contactos del cliente con su logo, teléfono, correo, dirección y sitio web, para que puedan encontrarle y llamarle después. Elija su teléfono para ver cómo:",
"It downloads. Tap": "Se descarga. Toque",
"Open": "Abrir",
"The contact opens. Tap": "Se abre el contacto. Toque",
"at the top left.": "arriba a la izquierda.",
"These are screenshots. On the real card, every button works when you tap it.": "Son capturas de pantalla. En la tarjeta real, cada botón funciona al tocarlo.",
"Show all Alpha Fit Club card screenshots": "Ver todas las capturas de la tarjeta de Alpha Fit Club",
"Show all Keon Torres card screenshots": "Ver todas las capturas de la tarjeta de Keon Torres",
"rings the gym": "suena en el gimnasio",
"writes to the gym": "le escribe al gimnasio",
"opens the map": "abre el mapa",
"switches the look": "cambia el aspecto",
"send the card": "envía la tarjeta",
"adds to phone": "lo agrega al teléfono",
"scan to open": "escanee para abrir",
"Message on LINE": "Mensaje por LINE",
"writes to him": "le escribe a él",
"installs like an app": "se instala como una aplicación",
"“Great product. Great service. Best digital business card out there! I’ve had several and this is the most interactive I’ve had. Pete’s very accommodating and works with you on all the details till it’s just right. So happy to do business with Torres Tech Remote!”": "“Great product. Great service. Best digital business card out there! I’ve had several and this is the most interactive I’ve had. Pete’s very accommodating and works with you on all the details till it’s just right. So happy to do business with Torres Tech Remote!”",
"Free preview form with required name and business name fields": "Formulario de vista previa gratis con los campos obligatorios de nombre y nombre del negocio",
"Fill out our Free Preview form": "Llene nuestro formulario de vista previa gratis",
"Only your name, business name, phone, email and a confirmation checkbox are required. All other questions are optional.": "Solo se piden su nombre, el nombre del negocio, teléfono, correo y una casilla de confirmación. Las demás preguntas son opcionales.",
"A watermarked digital business card preview for Navalha Barber Co.": "Vista previa con marca de agua de una tarjeta digital de Navalha Barber Co.",
"Get your free preview": "Reciba su vista previa gratis",
"We create your free digital business card preview from the information you give us and email it to you for review. You can receive up to 3 free previews. You only pay if you approve your card.": "Crearemos la vista previa gratis de su tarjeta de presentación digital con los datos que nos dé y se la enviaremos por correo para que la revise. Puede recibir hasta 3 vistas previas gratis. Solo paga si aprueba su tarjeta.",
"The live Navalha Barber Co. digital card with contact buttons and hours": "La tarjeta digital en vivo de Navalha Barber Co. con botones de contacto y horario",
"Pick up to 3 languages for your card, like Spanish, Portuguese, Chinese, Japanese and Arabic. Customers switch between them on the card.": "Elija hasta 3 idiomas para su tarjeta, como español, portugués, chino, japonés y árabe. Los clientes cambian entre ellos en la tarjeta.",
"Who makes your card": "Quién hace su tarjeta",
"Send me your business name and I’ll make you a free preview and send you a link to review. You only pay if you like it.": "Envíeme el nombre de su negocio y le haré una vista previa gratis con un enlace para que la revise. Solo paga si le gusta.",
"Fill in the form →": "Llene el formulario →",
"Certified IT technician. I set up and look after your card myself.": "Técnico de TI certificado. Yo mismo preparo y cuido su tarjeta.",
"Your logo and brand colors": "Su logo y los colores de su marca",
"Call, text, WhatsApp, email, directions and website buttons": "Botones de llamada, mensaje, WhatsApp, correo, direcciones y sitio web",
"Hours, services and prices, photos, payment links": "Horario, servicios y precios, fotos y enlaces de pago",
"QR code, Share and Save contact": "Código QR, Compartir y Guardar contacto",
"Up to 3 of 25 languages": "Hasta 3 de 25 idiomas",
"Installs like an app on iPhone and Android, no app store": "Se instala como una aplicación en iPhone y Android, sin tienda de aplicaciones",
"Up to 3 free previews before you pay": "Hasta 3 vistas previas gratis antes de pagar",
"or": "o",
"$100 per year": "$100 al año",
", 2 months free": ", 2 meses gratis",
"Hosting and security updates": "Alojamiento y actualizaciones de seguridad",
"Unlimited changes to your hours, prices, photos and links": "Cambios ilimitados en su horario, precios, fotos y enlaces",
"Your QR code never changes, so printed codes keep working": "Su código QR nunca cambia, así que los códigos impresos siguen funcionando",
"For businesses": "Para negocios",
"Select the option that fits your organization, or combine them. Each business is different, so we provide a custom quote based on your number of locations and employees. Setup is free.": "Elija la opción que se ajuste a su organización, o combínelas. Cada negocio es distinto, por eso damos un presupuesto a la medida según su número de locales y empleados. La instalación es gratis.",
"Run a gym or fitness studio?": "¿Tiene un gimnasio o un estudio de fitness?",
"See the digital business card for gyms": "Vea la tarjeta de presentación digital para gimnasios",
"A single card lists every location, each with its own address, directions, phone number and hours. Suited to retail, fitness and multi-site businesses.": "Una sola tarjeta muestra cada local, cada uno con su dirección, indicaciones, teléfono y horario. Ideal para comercios, fitness y negocios con varias sedes.",
"See an example: Corner Table Café": "Ver un ejemplo: Corner Table Café",
"Each employee receives an individual card with their name, photo and contact details. One office card lists the entire team.": "Cada empleado recibe su propia tarjeta con su nombre, foto y datos de contacto. Una tarjeta de oficina muestra a todo el equipo.",
"See an example: Harbor Realty": "Ver un ejemplo: Harbor Realty",
"Multiple locations and employees": "Varios locales y empleados",
"Multiple locations with individual employee cards. Each employee can be assigned to the location where they work.": "Varios locales con tarjetas individuales de empleados. Cada empleado puede asignarse al local donde trabaja.",
"See an example: Brightside Dental": "Ver un ejemplo: Brightside Dental",
"Request your free preview →": "Pida su vista previa gratis →",
"Free preview. No payment or credit card required. Just your name, business name, phone and email to get started.": "Vista previa gratis. Sin pago ni tarjeta de crédito. Solo su nombre, el nombre del negocio, teléfono y correo para empezar.",
"See it live:": "Véalo en vivo:",
})

RAW = [
    ('<li>Open the <b>Chrome</b> browser and type in your card’s link.</li><li>Scroll down and tap <b>Add to home screen</b> on the card.</li><li>Tap <b>Install</b>. The card’s icon is added to your home screen and to your app list.</li>',
     '<li>Abra el navegador <b>Chrome</b> y escriba el enlace de su tarjeta.</li><li>Baje y toque <b>Añadir a pantalla de inicio</b> en la tarjeta.</li><li>Toque <b>Instalar</b>. El ícono de la tarjeta se agrega a su pantalla de inicio y a su lista de aplicaciones.</li>'),
    ('<li>Open <b>Chrome</b> and type in your card’s link.</li><li>Scroll down and tap <b>Add to home screen</b> on the card.</li><li>Tap <b>Install</b>.</li>',
     '<li>Abra <b>Chrome</b> y escriba el enlace de su tarjeta.</li><li>Baje y toque <b>Añadir a pantalla de inicio</b> en la tarjeta.</li><li>Toque <b>Instalar</b>.</li>'),
    ('<li>Open your card.</li><li>Tap the <b>Save contact</b> button.</li><li>Download the file: tap <b>Download</b> in the box that shows the file name (like <b>torres-tech-remote.vcf</b>) and where it will be saved.</li><li>Open the downloaded file.</li><li>On the next screen, tap <b>Import</b> and choose where to save it.</li><li>The contact is now in your contacts list.</li>',
     '<li>Abra su tarjeta.</li><li>Toque el botón <b>Guardar contacto</b>.</li><li>Descargue el archivo: toque <b>Descargar</b> en el cuadro que muestra el nombre del archivo (por ejemplo, <b>torres-tech-remote.vcf</b>) y dónde se guardará.</li><li>Abra el archivo descargado.</li><li>En la pantalla siguiente, toque <b>Importar</b> y elija dónde guardarlo.</li><li>El contacto ya está en su lista de contactos.</li>'),
    ('<li>Open <b>Safari</b> and type in your card’s link.</li><li>Scroll down and tap <b>Add to home screen</b> on the card.</li><li>Tap <b>Share</b> (the square with an arrow).</li><li>Tap <b>Add to Home Screen</b>, then <b>Add</b>.</li>',
     '<li>Abra <b>Safari</b> y escriba el enlace de su tarjeta.</li><li>Baje y toque <b>Añadir a pantalla de inicio</b> en la tarjeta.</li><li>Toque <b>Compartir</b> (el cuadrado con una flecha).</li><li>Toque <b>Añadir a pantalla de inicio</b> y luego <b>Añadir</b>.</li>'),
    ('<li>Open <b>Safari</b> and type in your card’s link.</li><li>Scroll down and tap <b>Save contact</b> on the card.</li><li>The contact opens. Tap <b>✓</b> at the top left.</li>',
     '<li>Abra <b>Safari</b> y escriba el enlace de su tarjeta.</li><li>Baje y toque <b>Guardar contacto</b> en la tarjeta.</li><li>Se abre el contacto. Toque <b>✓</b> arriba a la izquierda.</li>'),
]


import re


def PAGE(s):
    # language links / hreflang
    s = re.sub(r'<link href="[^"]*" hreflang="[^"]*" rel="alternate"/>\n', "", s)
    s = s.replace('<link href="https://torrestechremote.com/es/" rel="canonical"/>\n',
        '<link href="https://torrestechremote.com/es/" rel="canonical"/>\n'
        '<link href="https://torrestechremote.com/" hreflang="en" rel="alternate"/>\n'
        '<link href="https://torrestechremote.com/es/" hreflang="es" rel="alternate"/>\n'
        '<link href="https://torrestechremote.com/pt/" hreflang="pt-PT" rel="alternate"/>\n'
        '<link href="https://torrestechremote.com/" hreflang="x-default" rel="alternate"/>\n', 1)
    s = s.replace('<b aria-current="page">EN</b> · <a hreflang="es" lang="es" href="/es/">ES</a>',
                  '<a hreflang="en" lang="en" href="/">EN</a> · <b aria-current="page">ES</b>')
    s = s.replace('<a href="/" aria-current="page">English</a><a hreflang="es" lang="es" href="/es/">Español</a>',
                  '<a hreflang="en" lang="en" href="/">English</a><a href="/es/" aria-current="page">Español</a>')
    s = s.replace('/pt/', '/pt/')
    s = s.replace('/es/', '/es/')
    s = s.replace('href="/digital-business-card-for-gyms/"', 'href="/es/tarjeta-digital-gimnasio/"')
    # forms and contact messages in Spanish
    s = s.replace('href="/go/preview.html"', 'href="/go/preview-es.html"')
    s = s.replace('https://docs.google.com/forms/d/e/1FAIpQLSenglfDQ0WaNQpeYR2ZBD-Y4AP6W5HduUZSNqFPebuN1tnx-Q/viewform', '/go/preview-es.html')
    sms = urllib.parse.quote("Hola Pedro, me gustaría una vista previa gratis para mi negocio: ", safe="")
    s = re.sub(r'href="sms:\+12017722106\?&amp;body=[^"]*"', 'href="sms:+12017722106?&amp;body=%s"' % sms, s)
    body = ("Hola, me gustaría una vista previa gratis de una tarjeta de presentación digital.\n\nNombre del negocio: \nTeléfono del negocio: \nCorreo del negocio: \nDirección o zona: \nHorario: \n"
            "Servicios (y precios, si quiere que se muestren): \nCómo reservan, piden o cotizan los clientes (enlace de una aplicación, o llamada/mensaje/WhatsApp): \nColores de la marca (si los hay): \nSitio web, Instagram o Facebook (si los hay): \n\nAdjunte su logo y unas fotos si los tiene.")
    subj = "Vista previa gratis: tarjeta de presentación digital"
    s = re.sub(r'href="mailto:pedro_torres@torrestechremote\.com\?subject=[^"]*"',
               'href="mailto:pedro_torres@torrestechremote.com?subject=%s&amp;body=%s"' % (urllib.parse.quote(subj, safe=""), urllib.parse.quote(body, safe="")), s)
    # social / review labels in the footer language heading etc. handled by TRANSLATIONS
    # open graph / twitter
    OT = "Tarjetas de presentación digitales para su negocio, cada local y su equipo"
    OD = "Para pequeños negocios en todo EE. UU.: un enlace y un código QR para cada local, una tarjeta para cada persona, y nosotros hacemos sus actualizaciones. Instalación gratis, luego $10/mes. Vista previa gratis antes de pagar."
    s = s.replace('content="Digital Business Cards for Your Business, Every Location, and Your Team"', 'content="%s"' % OT)
    s = s.replace('content="For small businesses across the U.S.: one link and one QR code for each location, a card for each person, and we do your updates. Free setup, then $10/month. Free preview before you pay."', 'content="%s"' % OD)
    # JSON-LD
    s = s.replace('"@id": "https://torrestechremote.com/#webpage",\n      "url": "https://torrestechremote.com/",\n      "name": "Digital Business Cards for Small Businesses Across the U.S.",',
                  '"@id": "https://torrestechremote.com/es/#webpage",\n      "url": "https://torrestechremote.com/es/",\n      "inLanguage": "es",\n      "name": "Tarjetas de presentación digitales para pequeños negocios en todo EE. UU.",')
    s = s.replace('"serviceType": "Digital business card design and hosting"', '"serviceType": "Diseño y alojamiento de tarjetas de presentación digitales"')
    s = s.replace('"name": "Design & setup"', '"name": "Diseño e instalación"').replace('"description": "Free"', '"description": "Gratis"')
    s = s.replace('"name": "Hosting & updates, monthly"', '"name": "Alojamiento y actualizaciones, mensual"').replace('"name": "Hosting & updates, yearly"', '"name": "Alojamiento y actualizaciones, anual"')
    for a, b in (("Night · English", "Noche · Inglés"), ("Day · English", "Día · Inglés"), ("Night · Spanish", "Noche · Español"), ("Day · Spanish", "Día · Español"),
                 ("Night · Japanese", "Noche · Japonés"), ("Day · Japanese", "Día · Japonés"), ("Night · Vietnamese", "Noche · Vietnamita"), ("Day · Vietnamese", "Día · Vietnamita")):
        s = s.replace(", " + a + '"', ", " + b + '"')
    s = s.replace('<span lang="es">Your business card', '<span lang="en">Your business card')
    s = s.replace("<b>Técnico de TI certificado CompTIA A+</b>", "<b>Certificado CompTIA A+</b>")
    s = s.replace('<a href="#card">Qué lleva su tarjeta</a>', '<a href="#card">Su tarjeta</a>')
    s = s.replace('<a href="#faq">Preguntas frecuentes</a>', '<a href="#faq">Preguntas</a>')
    # unlock box messages
    s = s.replace('"Checking…"', '"Comprobando…"')
    s = s.replace('"That code doesn’t match. Check the code we sent with your preview."', '"Ese código no coincide. Revise el código que le enviamos con su vista previa."')
    s = s.replace('"This browser can’t unlock the links. Email us for your payment link."', '"Este navegador no puede desbloquear los enlaces. Escríbanos para recibir su enlace de pago."')
    return s
