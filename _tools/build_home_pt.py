#!/usr/bin/env python3
"""Builds pt/index.html (Portuguese pt-PT home page) from the English index.html. Safe to re-run; only writes es/index.html."""
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
rep('<html lang="en">', '<html lang="pt-PT">')
T = "Torres Tech Remote | Cartões de visita digitais para pequenos negócios em todos os EUA"
rep("<title>Torres Tech Remote | Digital Business Cards for Small Businesses Across the U.S.</title>", f"<title>{T}</title>")
D = "Cartões de visita digitais para pequenos negócios em todos os EUA: uma ligação e um código QR para cada local, um cartão para cada pessoa, e nós tratamos das suas atualizações. Criação grátis, depois $10/mês. Pré-visualização grátis antes de pagar."
rep('<meta content="Digital business cards for small businesses across the U.S.: one link and one QR code for every location, a card for each person, and we do your updates. Free setup, then $10/month. Free preview before you pay." name="description"/>',
    f'<meta content="{D}" name="description"/>')
rep('<link href="https://torrestechremote.com/" rel="canonical"/>',
    '<link href="https://torrestechremote.com/pt/" rel="canonical"/>\n<link href="https://torrestechremote.com/" hreflang="en" rel="alternate"/>\n<link href="https://torrestechremote.com/es/" hreflang="es" rel="alternate"/>\n<link href="https://torrestechremote.com/pt/" hreflang="pt-PT" rel="alternate"/>\n<link href="https://torrestechremote.com/" hreflang="x-default" rel="alternate"/>')
rep('<meta content="https://torrestechremote.com/" property="og:url"/>', '<meta content="https://torrestechremote.com/pt/" property="og:url"/>')
OT = "Torres Tech Remote | Cartões de visita digitais para o seu negócio, cada local e a sua equipa"
OD = "Para pequenos negócios em todos os EUA: uma ligação e um código QR para cada local, um cartão para cada pessoa, e nós tratamos das suas atualizações. Criação grátis, depois $10/mês. Pré-visualização grátis antes de pagar."
rep('<meta content="Torres Tech Remote | Digital Business Cards for Your Business, Every Location and Team" property="og:title"/>', f'<meta content="{OT}" property="og:title"/>')
rep('<meta content="For small businesses across the U.S.: one link and one QR code for each location, a card for each person, and we do your updates. Free setup, then $10/month. Free preview before you pay." property="og:description"/>', f'<meta content="{OD}" property="og:description"/>')
rep('<meta content="Torres Tech Remote: digital business cards for small businesses across the U.S., for one business, every location, and your whole team" property="og:image:alt"/>',
    '<meta content="Torres Tech Remote: cartões de visita digitais para pequenos negócios em todos os EUA, para um negócio, cada local e toda a sua equipa" property="og:image:alt"/>')
rep('<meta content="Torres Tech Remote | Digital Business Cards for Your Business, Every Location and Team" name="twitter:title"/>', f'<meta content="{OT}" name="twitter:title"/>')
rep('<meta content="For small businesses across the U.S.: one link and one QR code for each location, a card for each person, and we do your updates. Free setup, then $10/month. Free preview before you pay." name="twitter:description"/>', f'<meta content="{OD}" name="twitter:description"/>')
# JSON-LD
rep('"url": "https://torrestechremote.com/",\n      "publisher"', '"url": "https://torrestechremote.com/",\n      "inLanguage": ["en", "es", "pt-PT"],\n      "publisher"')
rep('"@id": "https://torrestechremote.com/#webpage",\n      "url": "https://torrestechremote.com/",\n      "name": "Torres Tech Remote: digital business cards",',
    '"@id": "https://torrestechremote.com/pt/#webpage",\n      "url": "https://torrestechremote.com/pt/",\n      "inLanguage": "pt-PT",\n      "name": "Torres Tech Remote: cartões de visita digitais",')

# language switch (English / Español; Português added when that page exists)
rep('</style>\n</head>', '.langs{display:flex;gap:12px;font-size:14px;align-items:center;margin-right:6px}.langs a{color:var(--muted,#65717e);text-decoration:none}.langs a:hover{text-decoration:underline}.langs b{color:var(--navy,#12192d)}\n</style>\n</head>')
rep('<div class="nav-right">\n', '<div class="nav-right">\n<nav class="langs" aria-label="Idioma"><a href="/" hreflang="en" lang="en">English</a><a href="/es/" hreflang="es" lang="es">Español</a><b aria-current="page">Português</b></nav>\n')

# ---- absolute asset paths (page now lives in /es/) ----
s = s.replace('src="img/', 'src="/img/').replace('src="comptia-a-certification.7.png"', 'src="/comptia-a-certification.7.png"')
rep('href="tos.html"', 'href="/tos.html"'); rep('href="privacy.html"', 'href="/privacy.html"')
rep('<a class="brand" href="/">', '<a class="brand" href="/pt/">', 2)

# free-preview buttons always open the Portuguese form on this page
s = s.replace('href="/go/preview.html"', 'href="/go/preview-pt.html"')

# ---- header ----
rep('rel="noopener" target="_blank">Demo card</a>', 'rel="noopener" target="_blank">Cartão de demonstração</a>')
rep('<a class="navlink" href="/digital-business-cards.html#pricing">Pricing</a>', '<a class="navlink" href="/digital-business-cards.html#pricing">Preços</a>')
rep('<a class="navlink" href="/digital-business-cards.html#faq">FAQ</a>', '<a class="navlink" href="/digital-business-cards.html#faq">Perguntas frequentes</a>')
rep('target="_blank">Free preview</a>', 'target="_blank">Pré-visualização grátis</a>')
rep('href="tel:+12017722106">Call</a>', 'href="tel:+12017722106">Ligar</a>')

# ---- hero ----
rep('Digital Business Cards · Newark, NJ', 'Cartões de visita digitais · Newark, NJ')
rep('<h1>A business card your customers <em>keep on their phone.</em></h1>', '<h1>Um cartão de visita que os seus clientes <em>guardam no telemóvel.</em></h1>')
rep("One link and one QR code for your shop. Customers call, text, WhatsApp or email you in one tap and save you to their contacts. Your card opens in your customer's own phone language, and they can tap to switch. We design it, host it and keep it up to date. You never touch an app.",
    "Uma ligação e um código QR para o seu negócio. Os seus clientes ligam, enviam mensagem, WhatsApp ou e-mail com um só toque e guardam-no nos contactos. O seu cartão abre-se no idioma do telemóvel de cada cliente, e eles podem tocar para mudar. Nós desenhamo-lo, alojamo-lo e mantemo-lo atualizado. Nunca precisa de mexer numa aplicação.")
rep('>Call (201) 772-2106</a>', '>Ligar para (201) 772-2106</a>', 2)
rep('Hi%20Pedro%2C%20I%27d%20like%20a%20free%20preview%20for%20my%20business%3A%20', urllib.parse.quote("Olá Pedro, gostaria de uma pré-visualização grátis para o meu negócio: ", safe=""), 2)
rep('>Text Pedro</a>', '>Enviar mensagem ao Pedro</a>', 2)
rep('>Request your free preview</a>', '>Peça a sua pré-visualização grátis</a>', 3)
rep('Call and Text open on your phone. Email works from a computer or a phone.</p>\n<p class="contact-hint">Free preview.', 'Ligar e Mensagem abrem no seu telemóvel. O e-mail funciona num computador ou num telemóvel.</p>\n<p class="contact-hint">Free preview.')
rep('Call and Text open on your phone. Email works from a computer or a phone.', 'Ligar e Mensagem abrem no seu telemóvel. O e-mail funciona num computador ou num telemóvel.')
rep('Free preview. No payment or credit card required. Just your name, business name, phone, and email to get started.', 'Pré-visualização grátis. Sem pagamento nem cartão de crédito. Só o seu nome, o nome do negócio, telefone e e-mail para começar.', 2)
rep('alt="Pedro Torres, owner of Torres Tech Remote"', 'alt="Pedro Torres, dono da Torres Tech Remote"')
rep('>Email Pedro</a> · ', '>Enviar e-mail ao Pedro</a> · ')
rep('target="_blank">See the demo card</a>', 'target="_blank">Ver o cartão de demonstração</a>')
# remove the old trilingual tagline block
s, n = re.subn(r'<div class="tri">.*?</div>\n', '', s, flags=re.S); assert n == 1

# ---- phones ----
rep('alt="Torres Tech Remote\'s own digital business card on a phone: TTR logo, See a demo card button, call, text, WhatsApp, email and website buttons, Share, Save contact, Show QR code, and opening hours"',
    'alt="O cartão de visita digital da Torres Tech Remote num telemóvel: logótipo da TTR, botão para ver um cartão de demonstração, botões de chamada, mensagem, WhatsApp, e-mail e site, Partilhar, Guardar contacto, Mostrar código QR e horário"')
rep('<b>Our own card</b>', '<b>O nosso próprio cartão</b>')
rep('alt="Demo digital business card for a barbershop on a phone: logo, Book now button, call, text, WhatsApp, email, directions and website buttons, Save contact, Show QR code, and opening hours"',
    'alt="Cartão de visita digital de demonstração de uma barbearia num telemóvel: logótipo, botão de reservar, botões de chamada, mensagem, WhatsApp, e-mail, direções e site, Guardar contacto, Mostrar código QR e horário"')
rep('<b>Demo card</b> for a made-up barbershop', '<b>Cartão de demonstração</b> de uma barbearia inventada')

# ---- trust bar ----
rep('<b>Free setup</b>', '<b>Criação grátis</b>')
rep('<span>$10/month or $100/year</span>', '<span>$10/mês ou $100/ano</span>')
rep('<span>Up to 3 free previews</span>', '<span>Até 3 pré-visualizações grátis</span>')
rep('In-person service in the Ironbound, Newark NJ.', 'Serviço presencial no Ironbound, Newark, NJ.')
rep('</svg>Now on Facebook</a>', '</svg>Agora no Facebook</a>')

# ---- offers ----
rep('<p class="kicker">Choose what fits</p>', '<p class="kicker">Escolha o que lhe convém</p>')
rep('<h2>One card, or a card for every location and employee.</h2>', '<h2>Um cartão, ou um cartão para cada local e cada funcionário.</h2>')
rep('<p>Setup is free. See your card before you pay, with up to 3 free previews.</p>', '<p>A criação é grátis. Veja o seu cartão antes de pagar, com até 3 pré-visualizações grátis.</p>')
rep('<p class="label">One business</p>', '<p class="label">Um negócio</p>')
rep('<h3>One card for your business</h3>', '<h3>Um cartão para o seu negócio</h3>')
rep('Your logo and brand colors, call, text, WhatsApp, email, directions and website buttons, hours, services and prices, payment links, and a QR code that never changes. Free setup, then $10/month or $100/year.',
    'O seu logótipo e as cores da sua marca, botões de chamada, mensagem, WhatsApp, e-mail, direções e site, horários, serviços e preços, ligações de pagamento e um código QR que nunca muda. Criação grátis, depois $10/mês ou $100/ano.')
rep('>See how it works and pricing</a>', '>Veja como funciona e os preços</a>')
rep('<p class="label">Locations and teams</p>', '<p class="label">Locais e equipas</p>')
rep('<h3>Multiple locations or employees</h3>', '<h3>Vários locais ou funcionários</h3>')
rep('A single card can list every location with its own address, phone and hours, and each employee can have an individual card with their name, photo and contact details. Each business is different, so we provide a custom quote. Setup is free.',
    'Um só cartão pode mostrar cada local com a sua própria morada, telefone e horário, e cada funcionário pode ter o seu cartão com nome, foto e dados de contacto. Cada negócio é diferente, por isso fazemos um orçamento à medida. A criação é grátis.')
rep('>Request a quote</a>', '>Pedir um orçamento (formulário em inglês)</a>')
rep('>See examples</a>', '>Ver exemplos</a>')
rep('Run a gym or fitness studio? <a href="/digital-business-card-for-gyms/"><b>See the digital business card for gyms</b></a>.',
    'Tem um ginásio ou um estúdio de fitness? <a href="/pt/cartao-digital-ginasio/"><b>Veja o cartão de visita digital para ginásios</b></a>.')
rep('Prefer to talk? Call <a href="tel:+12017722106">(201) 772-2106</a> or email <a', 'Prefere falar? Ligue para <a href="tel:+12017722106">(201) 772-2106</a> ou escreva para <a')

# ---- meet ----
rep('<p class="kicker">About Torres Tech Remote</p>', '<p class="kicker">Sobre a Torres Tech Remote</p>')
rep('<h2>Hi, I’m Pedro.</h2>', '<h2>Olá, sou o Pedro.</h2>')
rep('alt="Pedro Torres, founder of Torres Tech Remote"', 'alt="Pedro Torres, fundador da Torres Tech Remote"')
rep('I run Torres Tech Remote from the Ironbound, Newark. I make every card myself, and in the Ironbound I can come by your shop to set it up with you.',
    'Giro a Torres Tech Remote a partir do Ironbound, em Newark. Faço cada cartão eu mesmo, e no Ironbound posso passar pelo seu negócio para o preparar consigo.')
rep('I’m Pedro, the owner. Send me your business name and I’ll make you a free preview and send you a link to review. You only pay if you like it.',
    'Sou o Pedro, o dono. Envie-me o nome do seu negócio e farei uma pré-visualização grátis com uma ligação para a rever. Só paga se gostar.')
rep('<a class="btn btn-ghost" href="mailto:pedro_torres@torrestechremote.com">Email Pedro</a>', '<a class="btn btn-ghost" href="mailto:pedro_torres@torrestechremote.com">Enviar e-mail ao Pedro</a>')
rep('>Or fill in the form</a>', '>Ou preencha o formulário</a>')
rep('<p class="contact-hint">Email works from a computer or a phone.</p>', '<p class="contact-hint">O e-mail funciona num computador ou num telemóvel.</p>')
rep('alt="CompTIA A+ Certified"', 'alt="Técnico de TI certificado CompTIA A+"')
rep('<b>CompTIA A+ Certified</b>', '<b>Técnico de TI certificado CompTIA A+</b>')
rep('IT Technician — Hardware &amp; Software Support. Industry-recognized certification covering troubleshooting, networking, and system configuration.',
    'Suporte de hardware e software. Certificação reconhecida na indústria que cobre resolução de problemas, redes e configuração de sistemas.')

# ---- final ----
rep('<h2>See your card before you pay.</h2>', '<h2>Veja o seu cartão antes de pagar.</h2>')
rep('Call, email or fill in a short form, and we’ll make you a free preview. Up to 3 free previews. You only pay when you’re happy with it.',
    'Ligue, escreva ou preencha um formulário curto e faremos uma pré-visualização grátis. Até 3 pré-visualizações grátis. Só paga quando estiver satisfeito com o resultado.')
rep('>Or email us</a>', '>Ou escreva-nos por e-mail</a>') if '>Or email us</a>' in s else None
# the mailto button text
s, n = re.subn(r'(<a class="btn btn-out" href="mailto:[^"]*">)[^<]*(</a>)', r'\1Ou escreva-nos por e-mail\2', s); assert n >= 1
body = ("Olá, gostaria de uma pré-visualização grátis de um cartão de visita digital.\n\nNome do negócio: \nTelefone do negócio: \nE-mail do negócio: \nMorada ou zona: \nHorário: \n"
        "Serviços (e preços, se quiser que sejam mostrados): \nComo os clientes reservam, encomendam ou pedem orçamento (ligação de uma aplicação, ou chamada/mensagem/WhatsApp): \nCores da marca (se tiver): \nSite, Instagram ou Facebook (se tiver): \n\nAnexe o seu logótipo e algumas fotos, se os tiver.")
subj = "Pré-visualização grátis: cartão de visita digital"
s, n = re.subn(r'href="mailto:pedro_torres@torrestechremote\.com\?subject=[^"]*"',
               'href="mailto:pedro_torres@torrestechremote.com?subject=%s&amp;body=%s"' % (urllib.parse.quote(subj, safe=""), urllib.parse.quote(body, safe="")), s); assert n == 1
rep('<small>See it live: <a href', '<small>Veja-o ao vivo: <a href')
rep('rel="noopener" target="_blank">demo card</a> · ', 'rel="noopener" target="_blank">cartão de demonstração</a> · ')
rep('>our own card</a>', '>o nosso próprio cartão</a>')

# ---- footer ----
rep('<p>Digital Business Cards · Ironbound, Newark, NJ</p>', '<p>Cartões de visita digitais · Ironbound, Newark, NJ</p>')
rep('<a href="/">Home</a>', '<a href="/pt/">Início</a>')
rep('<a href="/digital-business-cards.html">Digital business cards</a>', '<a href="/digital-business-cards.html">Cartões de visita digitais</a>')
rep('<a href="/digital-business-card-for-gyms/">Cards for gyms</a>', '<a href="/pt/cartao-digital-ginasio/">Cartões para ginásios</a>')
rep('">Contact</a>', '">Contacto</a>')
rep('>Terms</a>', '>Termos</a>'); rep('>Privacy</a>', '>Privacidade</a>')
rep('<h3>Follow</h3>', '<h3>Siga-nos</h3>')
rep('>Review us on Google</a>', '>Avalie-nos no Google</a>')

out = root / "pt" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(s, encoding="utf-8")
print("wrote", out, len(s))
