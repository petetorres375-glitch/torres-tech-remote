#!/usr/bin/env python3
"""Builds pt/cartoes-de-visita-digitais/index.html (Portuguese pt-PT sales page) from digital-business-cards.html.
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

URL = "https://torrestechremote.com/pt/cartoes-de-visita-digitais/"
EN = "https://torrestechremote.com/digital-business-cards.html"

# ---------- head ----------
R('<html lang="en">', '<html lang="pt-PT">', 1)
R("<title>Digital Business Cards for Small Businesses Across the U.S. | Torres Tech Remote</title>", "<title>Cartões de visita digitais para pequenos negócios em todos os EUA | Torres Tech Remote</title>", 1)
R('content="Digital business cards for one business, every location, and your whole team. One link and one QR code; customers call, text, email or save you in one tap, in up to 3 of 25 languages. Free setup, then $10/month. Free preview before you pay."',
  'content="Cartões de visita digitais para um negócio, cada local e toda a sua equipa. Uma ligação e um código QR; os clientes ligam, enviam mensagem, enviam e-mail ou guardam-no com um só toque, em até 3 de 25 idiomas. Criação grátis, depois $10/mês. Pré-visualização grátis antes de pagar."', 1)
R(f'<link href="{EN}" rel="canonical"/>',
  f'<link href="{URL}" rel="canonical"/>\n<link href="{EN}" hreflang="en" rel="alternate"/>\n<link href="{URL}" hreflang="pt-PT" rel="alternate"/>\n<link href="{EN}" hreflang="x-default" rel="alternate"/>', 1)
R(f'<meta content="{EN}" property="og:url"/>', f'<meta content="{URL}" property="og:url"/>', 1)
OT = "Cartões de visita digitais para o seu negócio, cada local e a sua equipa"
R('content="Digital Business Cards for Your Business, Every Location, and Your Team"', f'content="{OT}"', 2)
OD = "Para pequenos negócios em todos os EUA: uma ligação e um código QR para cada local, um cartão para cada pessoa, e nós tratamos das suas atualizações. Criação grátis, depois $10/mês. Pré-visualização grátis antes de pagar."
R('content="For small businesses across the U.S.: one link and one QR code for each location, a card for each person, and we do your updates. Free setup, then $10/month. Free preview before you pay."', f'content="{OD}"', 2)
R('content="Torres Tech Remote: digital business cards for small businesses across the U.S., for one business, every location, and your whole team"',
  'content="Torres Tech Remote: cartões de visita digitais para pequenos negócios em todos os EUA, para um negócio, cada local e toda a sua equipa"', 1)
# JSON-LD
R(f'"@id": "{EN}#webpage",\n      "url": "{EN}",\n      "name": "Digital Business Cards for Small Businesses Across the U.S.",',
  f'"@id": "{URL}#webpage",\n      "url": "{URL}",\n      "inLanguage": "pt-PT",\n      "name": "Cartões de visita digitais para pequenos negócios em todos os EUA",', 1)
R(f'"breadcrumb": {{ "@id": "{EN}#breadcrumb" }}', f'"breadcrumb": {{ "@id": "{URL}#breadcrumb" }}', 1)
R(f'"@id": "{EN}#breadcrumb",', f'"@id": "{URL}#breadcrumb",', 1)
R(f'"position": 2, "name": "Digital Business Cards", "item": "{EN}"', f'"position": 2, "name": "Cartões de visita digitais", "item": "{URL}"', 1)
R('"description": "One link and one QR code for your business, every location, and your team. Customers call, text or email you in one tap, save you to their contacts, and read it in up to 3 of 25 languages. We design it, host it and keep it up to date.",',
  '"description": "Uma ligação e um código QR para o seu negócio, cada local e a sua equipa. Os clientes ligam, enviam mensagem ou e-mail com um só toque, guardam-no nos contactos e leem-no em até 3 de 25 idiomas. Nós desenhamo-lo, alojamo-lo e mantemo-lo atualizado.",', 1)
# the Service block keeps pointing at the English #service id (shared entity); only its name is localized elsewhere

# language switch (class langsw: the page already uses .langs for the language grid)
R('</style>\n</head>', '.langsw{display:flex;gap:12px;font-size:14px;align-items:center;margin-right:6px}.langsw a{color:var(--muted,#65717e);text-decoration:none}.langsw a:hover{text-decoration:underline}.langsw b{color:var(--navy,#12192d)}\n</style>\n</head>', 1)
R('<div class="nav-right">\n', '<div class="nav-right">\n<nav class="langsw" aria-label="Idioma"><a href="/digital-business-cards.html" hreflang="en" lang="en">English</a><a href="/es/tarjetas-de-presentacion-digitales/" hreflang="es" lang="es">Español</a><b aria-current="page">Português</b></nav>\n', 1)

# ---------- absolute paths ----------
s = s.replace('src="img/', 'src="/img/').replace('poster="video/', 'poster="/video/').replace('src="video/', 'src="/video/')
R('`video/${clip}-', '`/video/${clip}-', 1)
R('href="tos.html"', 'href="/tos.html"'); R('href="privacy.html"', 'href="/privacy.html"')
R('<a class="brand" href="/">', '<a class="brand" href="/pt/">', 2)
# always Spanish steps + videos on this page, whatever the phone language is
R('.find((l) => ["en", "es", "pt", "pt-PT"].includes(l))) || "en";', '.find((l) => ["en", "es", "pt", "pt-PT"].includes(l))) || "en";\n    const pageLang = "pt-PT"; // this page is the Portuguese (Portugal) page', 1)
s2 = s.replace("const lang = ((navigator.languages", "const phoneLang = ((navigator.languages", 1)
assert s2 != s; s = s2
R("    if (STEPS[lang]) {", "    const lang = pageLang;\n    if (STEPS[lang]) {", 1)

# free preview buttons -> Spanish form
s = s.replace('href="/go/preview.html"', 'href="/go/preview-pt.html"')

# ---------- header + hero ----------
R('rel="noopener" target="_blank">Demo card</a>', 'rel="noopener" target="_blank">Cartão de demonstração</a>', 1)
R('<a class="navlink" href="#faq">FAQ</a>', '<a class="navlink" href="#faq">Perguntas frequentes</a>', 1)
R('target="_blank">Free preview</a>', 'target="_blank">Pré-visualização grátis</a>', 1)
R('href="tel:+12017722106">Call</a>', 'href="tel:+12017722106">Ligar</a>', 1)
R('Digital Business Cards · Newark, NJ', 'Cartões de visita digitais · Newark, NJ', 1)
R('<h1>A business card your customers <em>keep on their phone.</em></h1>', '<h1>Um cartão de visita que os seus clientes <em>guardam no telemóvel.</em></h1>', 1)
R("One link and one QR code for your shop. Customers call, text, WhatsApp or email you in one tap and save you to their contacts. Your card opens in your customer's own phone language, and they can tap to switch. We design it, host it and keep it up to date. You never touch an app.",
  "Uma ligação e um código QR para o seu negócio. Os seus clientes ligam, enviam mensagem, WhatsApp ou e-mail com um só toque e guardam-no nos contactos. O seu cartão abre-se no idioma do telemóvel de cada cliente, e eles podem tocar para mudar. Nós desenhamo-lo, alojamo-lo e mantemo-lo atualizado. Nunca precisa de mexer numa aplicação.", 1)
R('>Call (201) 772-2106</a>', '>Ligar para (201) 772-2106</a>', 2)
R('Hi%20Pedro%2C%20I%27d%20like%20a%20free%20preview%20for%20my%20business%3A%20', urllib.parse.quote("Olá Pedro, gostaria de uma pré-visualização grátis para o meu negócio: ", safe=""), 2)
R('>Text Pedro</a>', '>Enviar mensagem ao Pedro</a>', 2)
R('>Request your free preview</a>', '>Peça a sua pré-visualização grátis</a>', 2)
R('Call and Text open on your phone. Email works from a computer or a phone.', 'Ligar e Mensagem abrem no seu telemóvel. O e-mail funciona num computador ou num telemóvel.', 2)
R('Free preview. No payment or credit card required. Just your name, business name, phone, and email to get started.', 'Pré-visualização grátis. Sem pagamento nem cartão de crédito. Só o seu nome, o nome do negócio, telefone e e-mail para começar.', 2)
R('alt="Pedro Torres, owner of Torres Tech Remote"', 'alt="Pedro Torres, dono da Torres Tech Remote"', 1)
R('>Email Pedro</a> · ', '>Enviar e-mail ao Pedro</a> · ', 1)
R('target="_blank">See the demo card</a>', 'target="_blank">Ver o cartão de demonstração</a>', 1)
s, n = re.subn(r'<div class="tri">.*?</div>\n', '', s, flags=re.S); assert n == 1
R('alt="Torres Tech Remote\'s own digital business card on a phone: TTR logo, See a demo card button, call, text, WhatsApp, email and website buttons, Share, Save contact, Show QR code, and opening hours"',
  'alt="O cartão de visita digital da Torres Tech Remote num telemóvel: logótipo da TTR, botão para ver um cartão de demonstração, botões de chamada, mensagem, WhatsApp, e-mail e site, Partilhar, Guardar contacto, Mostrar código QR e horário"', 1)
R('<b>Our own card</b>', '<b>O nosso próprio cartão</b>', 1)
R('alt="Demo digital business card for a barbershop on a phone: logo, Book now button, call, text, WhatsApp, email, directions and website buttons, Save contact, Show QR code, and opening hours"',
  'alt="Cartão de visita digital de demonstração de uma barbearia num telemóvel: logótipo, botão de reservar, botões de chamada, mensagem, WhatsApp, e-mail, direções e site, Guardar contacto, Mostrar código QR e horário"', 1)
R('<b>Demo card</b> for a made-up barbershop', '<b>Cartão de demonstração</b> de uma barbearia inventada', 1)
R('aria-label="Service and pricing details"', 'aria-label="Serviço e preços"', 1)
R('<b>Free setup</b>', '<b>Criação grátis</b>', 1)
R('<span>$10/month or $100/year</span>', '<span>$10/mês ou $100/ano</span>', 1)
R('<span>Up to 3 free previews</span>', '<span>Até 3 pré-visualizações grátis</span>', 1)
R('In-person service in the Ironbound, Newark NJ.', 'Serviço presencial no Ironbound, Newark, NJ.', 1)
R('</svg>Now on Facebook</a>', '</svg>Agora no Facebook</a>', 1)

# ---------- features ----------
R("<p class=\"kicker\">What's on your card</p>", '<p class="kicker">O que leva o seu cartão</p>', 1)
R('<h2>Everything a customer needs, one tap away.</h2>', '<h2>Tudo o que um cliente precisa, a um toque.</h2>', 1)
R('<p>Tap either card above to try the real thing.</p>', '<p>Toque em qualquer um dos cartões acima para experimentar o verdadeiro.</p>', 1)
R('<h3>Your brand</h3><p>Your logo and brand colors.</p>', '<h3>O seu logótipo</h3><p>O seu logótipo e as cores da sua marca.</p>', 1)
R('<h3>One-tap buttons</h3><p>Call, text, WhatsApp, email, directions and website buttons.</p>', '<h3>Botões de um toque</h3><p>Botões de chamada, mensagem, WhatsApp, e-mail, direções e site.</p>', 1)
R('<h3>Your business details</h3><p>Hours, services and prices, photos, payment links.</p>', '<h3>Os dados do seu negócio</h3><p>Horário, serviços e preços, fotos e ligações de pagamento.</p>', 1)
R('<h3>Opens in their language</h3><p>Their phone is set to Spanish? They see Spanish, and can tap to switch to your other languages. You pick up to 3 of 25.</p>',
  '<h3>Abre no idioma deles</h3><p>O telemóvel está em inglês? Veem inglês e podem tocar para mudar para os outros idiomas do seu negócio. Escolhe até 3 de 25.</p>', 1)
R('<h3>A spot for your offer</h3><p>Having a sale? Email me and I change it for you. It can turn itself off when your offer ends.</p>',
  '<h3>Um espaço para a sua oferta</h3><p>Tem uma promoção? Escreva-me e eu altero-a por si. Pode desligar-se sozinha quando a oferta terminar.</p>', 1)
R('<h3>Easy to share</h3><p>QR code, Share and Save contact. <a href="#save-contact">See how</a>.</p>', '<h3>Fácil de partilhar</h3><p>Código QR, Partilhar e Guardar contacto. <a href="#save-contact">Veja como</a>.</p>', 1)
R('<h3>Like an app</h3><p>Installs like an app on iPhone and Android, no app store. <a href="#install">See how</a>.</p>', '<h3>Como uma aplicação</h3><p>Instala-se como uma aplicação no iPhone e no Android, sem loja de aplicações. <a href="#install">Veja como</a>.</p>', 1)
R('<h3>A QR code that lasts</h3><p>Your QR code never changes, so printed codes keep working.</p>', '<h3>Um código QR que dura</h3><p>O seu código QR nunca muda, por isso os códigos impressos continuam a funcionar.</p>', 1)
R('<p class="kicker">Works like an app</p>', '<p class="kicker">Funciona como uma aplicação</p>', 1)
R('<h3>Your card on their home screen.</h3>', '<h3>O seu cartão no ecrã principal deles.</h3>', 1)
R('<p>Customers save your card to their phone in a few taps. It gets its own icon, opens full screen like an app, and still opens without internet. No app store and no download. Pick your phone to watch how:</p>',
  '<p>Os clientes guardam o seu cartão no telemóvel com alguns toques. Tem o seu próprio ícone, abre em ecrã inteiro como uma aplicação e abre mesmo sem internet. Sem loja de aplicações e sem descarregar nada. Escolha o seu telemóvel para ver como:</p>', 1)
R('aria-label="Pick your phone"', 'aria-label="Escolha o seu telemóvel"', 2)
R('<p class="kicker">Saved in their contacts</p>', '<p class="kicker">Guardado nos contactos</p>', 1)
R('<h3>In their contacts in seconds.</h3>', '<h3>Nos contactos em segundos.</h3>', 1)
R('<p>“Save contact” adds your business to their contacts with your logo, phone, email, address and website, so they can find you and call you later. Pick your phone to watch how:</p>',
  '<p>"Guardar contacto" adiciona o seu negócio aos contactos do cliente com o seu logótipo, telefone, e-mail, morada e site, para que o possam encontrar e ligar-lhe mais tarde. Escolha o seu telemóvel para ver como:</p>', 1)
# video aria-labels (screen readers)
R("Video: on an Android phone, open the card in Chrome, tap Add to home screen, tap Install, and the card's icon appears on the home screen", "Vídeo: num telemóvel Android, abra o cartão no Chrome, toque em Adicionar ao ecrã principal, toque em Instalar, e o ícone do cartão aparece no ecrã principal", 1)
R("Video: on an iPhone, open the card in Safari, tap Share, tap Add to Home Screen, tap Add, and the card's icon appears on the home screen", "Vídeo: num iPhone, abra o cartão no Safari, toque em Partilhar, toque em Adicionar ao ecrã principal, toque em Adicionar, e o ícone do cartão aparece no ecrã principal", 1)
R("Video: on an Android phone, tap Save contact on the card, it downloads, tap Open, then tap Import, and the business is in the phone's contacts", "Vídeo: num telemóvel Android, toque em Guardar contacto no cartão, é transferido, toque em Abrir, depois toque em Importar, e o negócio fica nos contactos do telemóvel", 1)
R("Video: on an iPhone, tap Save contact on the card, the contact opens, tap the check mark at the top left, and the business is in the phone's contacts", "Vídeo: num iPhone, toque em Guardar contacto no cartão, o contacto abre, toque na marca de verificação no canto superior esquerdo, e o negócio fica nos contactos do telemóvel", 1)
# static (pre-JS) steps are replaced by the page script with the Spanish steps; make the static fallback Spanish too
for en, es in [('<li>Open the card in <b>Chrome</b>.</li>','<li>Abra o cartão no <b>Chrome</b>.</li>'),('<li>Tap <b>Add to home screen</b> on the card.</li>','<li>Toque em <b>Adicionar ao ecrã principal</b> no cartão.</li>'),('<li>Tap <b>Install</b>.</li>','<li>Toque em <b>Instalar</b>.</li>'),
    ('<li>Open the card in <b>Safari</b> (iPhone or iPad).</li>','<li>Abra o cartão no <b>Safari</b> (iPhone ou iPad).</li>'),('<li>Tap <b>Share</b> (the square with an arrow).</li>','<li>Toque em <b>Partilhar</b> (o quadrado com uma seta).</li>'),
    ('<li>Tap <b>Add to Home Screen</b>, then <b>Add</b>.</li>','<li>Toque em <b>Adicionar ao ecrã principal</b> e depois em <b>Adicionar</b>.</li>'),('<li>Tap <b>Save contact</b> on the card.</li>','<li>Toque em <b>Guardar contacto</b> no cartão.</li>'),
    ('<li>It downloads. Tap <b>Open</b>.</li>','<li>É transferido. Toque em <b>Abrir</b>.</li>'),('<li>Tap <b>Import</b> (some phones say <b>Save</b>).</li>','<li>Toque em <b>Importar</b> (alguns telemóveis dizem <b>Guardar</b>).</li>'),
    ('<li>The contact opens. Tap <b>✓</b> at the top left.</li>','<li>O contacto abre. Toque em <b>&#10003;</b> no canto superior esquerdo.</li>')]:
    R(en, es)

# ---------- clients ----------
R('<p class="kicker">Real cards</p>', '<p class="kicker">Cartões reais</p>', 1)
R('<h2>Featured clients.</h2>', '<h2>Clientes em destaque.</h2>', 1)
R('<p>These are screenshots. On the real card, every button works when you tap it.</p>', '<p>São capturas de ecrã. No cartão real, cada botão funciona ao tocar.</p>', 1)
R('<p>English &amp; Acting Coach / Instructor<br/>Vietnam &amp; Japan</p>', '<p>Professor e treinador de inglês e representação<br/>Vietname e Japão</p>', 1)
R('Tap to see more', 'Toque para ver mais', 2)
for en, es in [('Night · English','Noite · Inglês'),('Day · English','Dia · Inglês'),('Night · Japanese','Noite · Japonês'),('Day · Japanese','Dia · Japonês'),('Night · Vietnamese','Noite · Vietnamita'),('Day · Vietnamese','Dia · Vietnamita'),('Night · Spanish','Noite · Espanhol'),('Day · Spanish','Dia · Espanhol')]:
    R(en, es)
for nm in ['Keon Torres','Alpha Fit Club']:
    R(f'aria-label="Show all {nm} card screenshots"', f'aria-label="Ver todas as capturas do cartão de {nm}"')
    R(f'aria-label="{nm} card screenshots"', f'aria-label="Capturas do cartão de {nm}"')
    R(f'aria-label="Previous {nm} screenshot"', f'aria-label="Captura anterior de {nm}"')
    R(f'aria-label="Next {nm} screenshot"', f'aria-label="Captura seguinte de {nm}"')
R('aria-label="Choose a Keon Torres screenshot"', 'aria-label="Escolher uma captura de Keon Torres"', 1)
R('aria-label="Choose an Alpha Fit Club screenshot"', 'aria-label="Escolher uma captura de Alpha Fit Club"', 1)
R('alt="Keon Torres card, ', 'alt="Cartão de Keon Torres, '); R('alt="Alpha Fit Club card, ', 'alt="Cartão de Alpha Fit Club, ')
R('>Close</button>', '>Fechar</button>', 2)
R('<p class="langnote">Three languages on one card: English, Japanese and Vietnamese.</p>', '<p class="langnote">Três idiomas num só cartão: inglês, japonês e vietnamita.</p>', 1)
chips = [('<b>Message on LINE</b> opens a chat','<b>Mensagem por LINE</b> abre uma conversa'),('<b>Email</b> writes to him','<b>E-mail</b> escreve-lhe a ele'),('<b>EN / JA / VI</b> switches language','<b>EN / JA / VI</b> muda o idioma'),
 ('<b>Day / Night</b> switches the look','<b>Dia / Noite</b> muda o aspeto'),('<b>Share</b> send the card','<b>Partilhar</b> envia o cartão'),('<b>Save contact</b> adds to phone','<b>Guardar contacto</b> adiciona ao telemóvel'),
 ('<b>QR code</b> scan to open','<b>Código QR</b> digitalize para abrir'),('<b>Add to home screen</b> installs like an app','<b>Adicionar ao ecrã principal</b> instala-se como uma aplicação'),
 ('<b>Book first class</b> opens booking page','<b>Reservar primeira aula</b> abre a página de reservas'),('<b>Call</b> rings the gym','<b>Ligar</b> toca no ginásio'),('<b>Text</b> starts a text','<b>Mensagem</b> inicia uma mensagem de texto'),
 ('<b>Email</b> writes to the gym','<b>E-mail</b> escreve ao ginásio'),('<b>Directions</b> opens the map','<b>Direções</b> abre o mapa'),('<b>EN / ES</b> switches language','<b>EN / ES</b> muda o idioma')]
for en, es in chips: R(en, es)
R('<p class="langnote">English and Spanish on one card.</p>', '<p class="langnote">Inglês e espanhol num só cartão.</p>', 1)
R('<p>Alpha Fit Club</p>', '<p>Alpha Fit Club</p>') if False else None
R('aria-label="5 out of 5 stars"', 'aria-label="5 em 5 estrelas"', 1)
R('Google review, 5.0', 'Avaliação do Google (em inglês), 5.0', 1)

# ---------- how ----------
R('<p class="kicker">How it works</p>', '<p class="kicker">Como funciona</p>', 1)
R('<h2>See it before you pay.</h2>', '<h2>Veja antes de pagar.</h2>', 1)
R('<h3>Fill out our Free Preview form</h3><p>Only your name, business name, phone, email, and confirmation checkbox are required. All other questions are optional.</p>',
  '<h3>Preencha o nosso formulário de pré-visualização grátis</h3><p>Só são pedidos o seu nome, o nome do negócio, telefone, e-mail e uma caixa de confirmação. As restantes perguntas são opcionais.</p>', 1)
R("<h3>Get your free preview</h3><p>We'll create your free digital business card preview using the information you provide and email it to you for review. You can receive up to 3 free previews. You only pay if you approve your card.</p>",
  '<h3>Receba a sua pré-visualização grátis</h3><p>Criaremos a pré-visualização grátis do seu cartão de visita digital com os dados que nos der e enviá-la-emos por e-mail para a rever. Pode receber até 3 pré-visualizações grátis. Só paga se aprovar o seu cartão.</p>', 1)
R("<h3>Pay when you're happy</h3><p>You only pay when you’re happy with it. Then your card goes live with its own link and QR code.</p>",
  '<h3>Pague quando estiver satisfeito</h3><p>Só paga quando estiver satisfeito com o resultado. Depois o seu cartão fica publicado com a sua própria ligação e código QR.</p>', 1)
R('<p class="kicker">Languages</p>', '<p class="kicker">Idiomas</p>', 1)
R('<h2>Up to 3 of 25 languages.</h2>', '<h2>Até 3 de 25 idiomas.</h2>', 1)
R('<p class="sub-lead">Pick up to 3 languages for your card, like Spanish, Portuguese, Chinese, Japanese and Arabic. Customers switch between them on the card.</p>',
  '<p class="sub-lead">Escolha até 3 idiomas para o seu cartão, como espanhol, português, chinês, japonês e árabe. Os clientes alternam entre eles no cartão.</p>', 1)
R('<span>English</span>\n<span lang="es">', '<span>English</span>\n<span lang="es">', 1)

# ---------- pricing ----------
R('<p class="kicker">Pricing</p>', '<p class="kicker">Preços</p>', 1)
R('<h2>Free setup. Just a small monthly fee.</h2>', '<h2>Criação grátis. Só uma pequena mensalidade.</h2>', 1)
R('<p class="label">Design &amp; setup</p>', '<p class="label">Design e criação</p>', 1)
R('<div class="big">Free</div>', '<div class="big">Grátis</div>', 1)
R('<p class="psub"><b>No setup fee.</b></p>', '<p class="psub"><b>Sem custos de criação.</b></p>', 1)
for en, es in [('<li>Your logo and brand colors</li>','<li>O seu logótipo e as cores da sua marca</li>'),('<li>Call, text, WhatsApp, email, directions and website buttons</li>','<li>Botões de chamada, mensagem, WhatsApp, e-mail, direções e site</li>'),
 ('<li>Hours, services and prices, photos, payment links</li>','<li>Horário, serviços e preços, fotos e ligações de pagamento</li>'),('<li>QR code, Share and Save contact</li>','<li>Código QR, Partilhar e Guardar contacto</li>'),
 ('<li>Up to 3 of 25 languages</li>','<li>Até 3 de 25 idiomas</li>'),('<li>Installs like an app on iPhone and Android, no app store</li>','<li>Instala-se como uma aplicação no iPhone e no Android, sem loja de aplicações</li>'),
 ('<li><b>Up to 3 free previews before you pay</b></li>','<li><b>Até 3 pré-visualizações grátis antes de pagar</b></li>'),
 ('<li>Hosting and security updates</li>','<li>Alojamento e atualizações de segurança</li>'),('<li>Unlimited changes to your hours, prices, photos and links</li>','<li>Alterações ilimitadas ao seu horário, preços, fotos e ligações</li>'),
 ('<li>Your QR code never changes, so printed codes keep working</li>','<li>O seu código QR nunca muda, por isso os códigos impressos continuam a funcionar</li>')]:
    R(en, es, 1)
R('<p class="label">Hosting &amp; updates</p>', '<p class="label">Alojamento e atualizações</p>', 1)
R('<div class="big">$10<small> /month</small></div>', '<div class="big">$10<small> /mês</small></div>', 1)
R('<p class="psub">or <b>$100 per year</b>, 2 months free</p>', '<p class="psub">ou <b>$100 por ano</b>, 2 meses grátis</p>', 1)
R('<summary>Already approved your preview? Pay here</summary>', '<summary>Já aprovou a sua pré-visualização? Pague aqui</summary>', 1)
R('Enter the unlock code we sent you with your preview. Use the same name, business name and phone you gave us. No preview yet? <a href="mailto:pedro_torres@torrestechremote.com">Ask for one first</a>, it’s free.',
  'Introduza o código de desbloqueio que lhe enviámos com a sua pré-visualização. Use o mesmo nome, nome do negócio e telefone que nos deu. Ainda não tem pré-visualização? <a href="mailto:pedro_torres@torrestechremote.com">Peça uma primeiro</a>, é grátis.', 1)
R('<label for="order-code">Unlock code</label>', '<label for="order-code">Código de desbloqueio</label>', 1)
R('placeholder="From your preview"', 'placeholder="Da sua pré-visualização"', 1)
R('type="submit">Unlock</button>', 'type="submit">Desbloquear</button>', 1)
R('<p>No code box? <a href="mailto:pedro_torres@torrestechremote.com">Email us</a> for your payment link.</p>', '<p>Não vê o campo do código? <a href="mailto:pedro_torres@torrestechremote.com">Escreva-nos</a> para receber a sua ligação de pagamento.</p>', 1)
R('Your preview is ready to go live. At checkout, use the same name, business name and phone you gave us. Pick a plan:', 'A sua pré-visualização está pronta para ser publicada. Ao pagar, use o mesmo nome, nome do negócio e telefone que nos deu. Escolha um plano:', 1)
R('>Make it live: $10/month</a>', '>Publicar o meu cartão: $10/mês</a>', 1)
R('>Make it live: $100/year</a>', '>Publicar o meu cartão: $100/ano</a>', 1)
R('Card accepted online and in person. Cash in person for yearly plans. In-person service in the Ironbound, Newark NJ; online orders available in the US and its territories, and to US citizens abroad paying with a US card or bank account. See the <a href="/tos.html">Terms</a>.',
  'Aceitamos cartão online e em pessoa. Numerário em pessoa para os planos anuais. Serviço presencial no Ironbound, Newark, NJ; encomendas online disponíveis nos EUA e nos seus territórios, e para cidadãos norte-americanos no estrangeiro que paguem com um cartão ou conta bancária dos EUA. Veja os <a href="/tos.html">Termos</a> (em inglês).', 1)
R('"That code doesn’t match. Check the code we sent with your preview."', '"Esse código não corresponde. Verifique o código que lhe enviámos com a sua pré-visualização."', 1)
R('"This browser can’t unlock the links. Email us for your payment link."', '"Este navegador não consegue desbloquear as ligações. Escreva-nos para receber a sua ligação de pagamento."', 1)

# ---------- teams ----------
R('<p class="kicker">For businesses</p>', '<p class="kicker">Para negócios</p>', 1)
R('<h2>Multiple locations or employees?</h2>', '<h2>Vários locais ou funcionários?</h2>', 1)
R('<p>Select the option that fits your organization, or combine them. Each business is different, so we provide a custom quote based on your number of locations and employees. Setup is free.</p>',
  '<p>Escolha a opção que se adapta à sua organização, ou combine-as. Cada negócio é diferente, por isso fazemos um orçamento à medida consoante o número de locais e funcionários. A criação é grátis.</p>', 1)
R('Run a gym or fitness studio? <a href="/digital-business-card-for-gyms/"><b>See the digital business card for gyms</b></a>.', 'Tem um ginásio ou um estúdio de fitness? <a href="/pt/cartao-digital-ginasio/"><b>Veja o cartão de visita digital para ginásios</b></a>.', 1)
for en, es in [('<p class="label">Option 1</p>','<p class="label">Opção 1</p>'),('<p class="label">Option 2</p>','<p class="label">Opção 2</p>'),('<p class="label">Option 3</p>','<p class="label">Opção 3</p>'),
 ('<h3>Multiple locations</h3>','<h3>Vários locais</h3>'),('<h3>Single location, multiple employees</h3>','<h3>Um local, vários funcionários</h3>'),('<h3>Multiple locations and employees</h3>','<h3>Vários locais e funcionários</h3>'),
 ('<p>A single card lists every location, each with its own address, directions, phone number and hours. Suited to retail, fitness and multi-site businesses.</p>','<p>Um só cartão mostra cada local, cada um com a sua morada, direções, telefone e horário. Ideal para comércio, fitness e negócios com várias unidades.</p>'),
 ('<p>Each employee receives an individual card with their name, photo and contact details. One office card lists the entire team.</p>','<p>Cada funcionário recebe o seu próprio cartão com nome, foto e dados de contacto. Um cartão de escritório mostra toda a equipa.</p>'),
 ('<p>Multiple locations with individual employee cards. Each employee can be assigned to the location where they work.</p>','<p>Vários locais com cartões individuais de funcionários. Cada funcionário pode ser atribuído ao local onde trabalha.</p>'),
 ('See an example: Corner Table Café','Ver um exemplo: Corner Table Café'),('See an example: Harbor Realty','Ver um exemplo: Harbor Realty'),('See an example: Brightside Dental','Ver um exemplo: Brightside Dental'),
 ('>Request a quote: multiple locations</a>','>Pedir um orçamento: vários locais</a>'),('>Request a quote: multiple employees</a>','>Pedir um orçamento: vários funcionários</a>'),('>Request a quote: both</a>','>Pedir um orçamento: ambos</a>')]:
    R(en, es, 1)
R('Prefer to talk? Call <a href="tel:+12017722106">(201) 772-2106</a> or email <a', 'Prefere falar? Ligue para <a href="tel:+12017722106">(201) 772-2106</a> ou escreva para <a', 1)

# ---------- meet ----------
R('<p class="kicker">Who makes your card</p>', '<p class="kicker">Quem faz o seu cartão</p>', 1)
R('<h2>Hi, I’m Pedro.</h2>', '<h2>Olá, sou o Pedro.</h2>', 1)
R('alt="Pedro Torres, founder of Torres Tech Remote"', 'alt="Pedro Torres, fundador da Torres Tech Remote"', 1)
R('I run Torres Tech Remote from the Ironbound, Newark. I make every card myself, and in the Ironbound I can come by your shop to set it up with you.', 'Giro a Torres Tech Remote a partir do Ironbound, em Newark. Faço cada cartão eu mesmo, e no Ironbound posso passar pelo seu negócio para o preparar consigo.', 1)
R('I’m Pedro, the owner. Send me your business name and I’ll make you a free preview and send you a link to review. You only pay if you like it.', 'Sou o Pedro, o dono. Envie-me o nome do seu negócio e farei uma pré-visualização grátis com uma ligação para a rever. Só paga se gostar.', 1)
R('<a class="btn btn-ghost" href="mailto:pedro_torres@torrestechremote.com">Email Pedro</a>', '<a class="btn btn-ghost" href="mailto:pedro_torres@torrestechremote.com">Enviar e-mail ao Pedro</a>', 1)
R('>Or fill in the form</a>', '>Ou preencha o formulário</a>', 1)
R('<p class="contact-hint">Email works from a computer or a phone.</p>', '<p class="contact-hint">O e-mail funciona num computador ou num telemóvel.</p>', 1)

# ---------- FAQ ----------
R('<p class="kicker">FAQ</p>', '<p class="kicker">Perguntas frequentes</p>', 1)
R('<h2>Common questions.</h2>', '<h2>Perguntas comuns.</h2>', 1)
faq = [
('What does it cost?','Quanto custa?','Design and setup are free. You pay $10 per month for hosting and updates, or $100 per year (2 months free). Up to 3 free previews before you pay. For several locations or employees, request a custom quote <a href="#teams">here</a>.','O design e a criação são grátis. Paga $10 por mês pelo alojamento e atualizações, ou $100 por ano (2 meses grátis). Até 3 pré-visualizações grátis antes de pagar. Para vários locais ou funcionários, peça <a href="#teams">aqui</a> um orçamento à medida.'),
('Which languages can my card show?','Que idiomas pode mostrar o meu cartão?','Up to 3 of 25 languages, like Spanish, Portuguese, Chinese, Japanese and Arabic. See the <a href="#languages">full list</a>.','Até 3 de 25 idiomas, como espanhol, português, chinês, japonês e árabe. Veja a <a href="#languages">lista completa</a>.'),
('Do my customers need to download an app?','Os meus clientes têm de descarregar uma aplicação?','No. The card opens from its link or QR code. Customers can also save it to their home screen like an app, no app store. On Android, open it in Chrome and tap <b>Add to home screen</b>, then <b>Install</b>. On iPhone or iPad, open it in Safari, tap <b>Share</b>, then <b>Add to Home Screen</b>. <a href="#install">See the steps</a>.','Não. O cartão abre a partir da sua ligação ou código QR. Os clientes também o podem guardar no ecrã principal como uma aplicação, sem loja de aplicações. No Android, abra-o no Chrome e toque em <b>Adicionar ao ecrã principal</b>, depois em <b>Instalar</b>. No iPhone ou iPad, abra-o no Safari, toque em <b>Partilhar</b> e depois em <b>Adicionar ao ecrã principal</b>. <a href="#install">Veja os passos</a>.'),
('Can customers book, order or get a quote from my card?','Os clientes podem reservar, encomendar ou pedir orçamento a partir do meu cartão?','Yes. Your card’s main button, like Book now, Order online or Get a quote, opens the booking, ordering or quote page you already use, such as Square, Booksy, OpenTable or DoorDash. Or it can call, text or WhatsApp you. It works for barbers and salons, cafés and restaurants, contractors, pest control and more.','Sim. O botão principal do seu cartão, como Reservar, Encomendar online ou Pedir orçamento, abre a página de reservas, encomendas ou orçamentos que já usa, como Square, Booksy, OpenTable ou DoorDash. Ou pode ligar-lhe, enviar-lhe mensagem ou WhatsApp. Serve para barbeiros e salões, cafés e restaurantes, empreiteiros, controlo de pragas e mais.'),
('Can I change my hours or prices later?','Posso alterar o meu horário ou preços mais tarde?','Yes. Hosting includes unlimited changes to your hours, prices, photos and links. Your QR code never changes, so printed codes keep working.','Sim. O alojamento inclui alterações ilimitadas ao seu horário, preços, fotos e ligações. O seu código QR nunca muda, por isso os códigos impressos continuam a funcionar.'),
('How do I pay?','Como pago?','Card accepted online and in person. Cash in person for yearly plans. After you approve your free preview, pay online with the <a data-open-order="" href="#order">payment links</a>.','Aceitamos cartão online e em pessoa. Numerário em pessoa para os planos anuais. Depois de aprovar a sua pré-visualização grátis, pague online com as <a data-open-order="" href="#order">ligações de pagamento</a>.'),
('Can one card cover several locations?','Um cartão pode cobrir vários locais?','Yes. One card lists every location, each with its own address, directions, phone number and hours. Each location can also have its own QR code, so a customer who scans it at that location lands on that location. See the <a href="#teams">examples</a>.','Sim. Um cartão mostra cada local, cada um com a sua morada, direções, telefone e horário. Cada local pode também ter o seu próprio código QR, assim o cliente que o digitaliza nesse local chega a esse local. Veja os <a href="#teams">exemplos</a>.'),
('Can each of my employees have their own card?','Cada um dos meus funcionários pode ter o seu próprio cartão?','Yes. Each employee receives an individual card with their name, photo and contact details. One office card lists the entire team, and each person can be assigned to the location where they work.','Sim. Cada funcionário recebe o seu próprio cartão com nome, foto e dados de contacto. Um cartão de escritório mostra toda a equipa, e cada pessoa pode ser atribuída ao local onde trabalha.'),
('How much does it cost for several locations or employees?','Quanto custa com vários locais ou funcionários?','Each business is different, so we provide a custom quote based on your number of locations and employees. Setup is free. <a href="https://docs.google.com/forms/d/e/1FAIpQLSenglfDQ0WaNQpeYR2ZBD-Y4AP6W5HduUZSNqFPebuN1tnx-Q/viewform" rel="noopener nofollow" target="_blank">Request a quote</a>.','Cada negócio é diferente, por isso fazemos um orçamento à medida consoante o número de locais e funcionários. A criação é grátis. <a href="https://docs.google.com/forms/d/e/1FAIpQLSenglfDQ0WaNQpeYR2ZBD-Y4AP6W5HduUZSNqFPebuN1tnx-Q/viewform" rel="noopener nofollow" target="_blank">Peça um orçamento</a>.'),
('What happens when we add or lose an employee?','O que acontece se adicionarmos ou perdermos um funcionário?','You can add people at any time and they are billed for the rest of that year. If someone leaves, you can give their place to a new person at no charge. Please tell us by the 1st of the month, and we make the change that week.','Pode adicionar pessoas a qualquer momento e são cobradas pelo resto desse ano. Se alguém sair, pode dar o seu lugar a outra pessoa sem custos. Avise-nos até ao dia 1 do mês e fazemos a alteração nessa semana.'),
('What if one of my locations is a franchise?','E se um dos meus locais for uma franquia?','A location owned by another business is a separate customer with its own card and its own bill. It can link back to your main card if you both agree.','Um local que pertence a outro negócio é um cliente à parte, com o seu próprio cartão e a sua própria fatura. Pode ligar de volta ao seu cartão principal se ambos estiverem de acordo.'),
('Who can order a card?','Quem pode encomendar um cartão?','In-person service in the Ironbound, Newark NJ; online orders available in the US and its territories, and to US citizens abroad paying with a US card or bank account.','Serviço presencial no Ironbound, Newark, NJ; encomendas online disponíveis nos EUA e nos seus territórios, e para cidadãos norte-americanos no estrangeiro que paguem com um cartão ou conta bancária dos EUA.'),
]
for qe, qs, ae, as_ in faq:
    R(f'<summary>{qe}</summary>\n<div class="faq-answer">{ae}</div>', f'<summary>{qs}</summary>\n<div class="faq-answer">{as_}</div>', 1)

# ---------- final CTA + footer (same text as the Spanish home page) ----------
R('<h2>See your card before you pay.</h2>', '<h2>Veja o seu cartão antes de pagar.</h2>', 1)
R('Call, email or fill in a short form, and we’ll make you a free preview. Up to 3 free previews. You only pay when you’re happy with it.', 'Ligue, escreva ou preencha um formulário curto e faremos uma pré-visualização grátis. Até 3 pré-visualizações grátis. Só paga quando estiver satisfeito com o resultado.', 1)
body = ("Olá, gostaria de uma pré-visualização grátis de um cartão de visita digital.\n\nNome do negócio: \nTelefone do negócio: \nE-mail do negócio: \nMorada ou zona: \nHorário: \n"
        "Serviços (e preços, se quiser que sejam mostrados): \nComo os clientes reservam, encomendam ou pedem orçamento (ligação de uma aplicação, ou chamada/mensagem/WhatsApp): \nCores da marca (se tiver): \nSite, Instagram ou Facebook (se tiver): \n\nAnexe o seu logótipo e algumas fotos, se os tiver.")
subj = "Pré-visualização grátis: cartão de visita digital"
s, n = re.subn(r'href="mailto:pedro_torres@torrestechremote\.com\?subject=[^"]*"', 'href="mailto:pedro_torres@torrestechremote.com?subject=%s&amp;body=%s"' % (urllib.parse.quote(subj, safe=""), urllib.parse.quote(body, safe="")), s); assert n == 1
s, n = re.subn(r'(<a class="btn btn-out" href="mailto:[^"]*">)[^<]*(</a>)', r'\1Ou escreva-nos por e-mail\2', s); assert n == 1
R('<small>See it live: <a href', '<small>Veja-o ao vivo: <a href', 1)
R('rel="noopener" target="_blank">demo card</a> · ', 'rel="noopener" target="_blank">cartão de demonstração</a> · ', 1)
R('>our own card</a>', '>o nosso próprio cartão</a>', 1)
R('<p>Digital Business Cards · Ironbound, Newark, NJ</p>', '<p>Cartões de visita digitais · Ironbound, Newark, NJ</p>', 1)
R('<a href="/">Home</a>', '<a href="/pt/">Início</a>', 1)
R('<a href="/digital-business-card-for-gyms/">Cards for gyms</a>', '<a href="/pt/cartao-digital-ginasio/">Cartões para ginásios</a>', 1)
R('">Contact</a>', '">Contacto</a>', 1)
R('>Terms</a>', '>Termos</a>', 1); R('>Privacy</a>', '>Privacidade</a>', 1)
R('<h3>Follow</h3>', '<h3>Siga-nos</h3>', 1)
R('>Review us on Google</a>', '>Avalie-nos no Google</a>', 1)

# quote buttons go to the free-preview form in this language (same as the gym pages)
s = s.replace('https://docs.google.com/forms/d/e/1FAIpQLSenglfDQ0WaNQpeYR2ZBD-Y4AP6W5HduUZSNqFPebuN1tnx-Q/viewform', '/go/preview-pt.html')
s = s.replace(' (formulário em inglês)', '')

# full hreflang set (en, es, pt-PT, x-default) on every language version of the sales page
s = re.sub(r'<link href="[^"]*" hreflang="[^"]*" rel="alternate"/>\n?', '', s)
s = re.sub(r'(<link href="[^"]*" rel="canonical"/>)', lambda m: m.group(1) + '\n' + '<link href="https://torrestechremote.com/digital-business-cards.html" hreflang="en" rel="alternate"/>\n<link href="https://torrestechremote.com/es/tarjetas-de-presentacion-digitales/" hreflang="es" rel="alternate"/>\n<link href="https://torrestechremote.com/pt/cartoes-de-visita-digitais/" hreflang="pt-PT" rel="alternate"/>\n<link href="https://torrestechremote.com/digital-business-cards.html" hreflang="x-default" rel="alternate"/>', s, count=1)

out = root / "pt" / "cartoes-de-visita-digitais" / "index.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(s, encoding="utf-8")
print("wrote", out, len(s))
