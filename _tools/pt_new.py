"""Portuguese (pt-PT) for the new one-page home. Used by build_home_pt.py. Same layout as es_new.py.
New Portuguese is for Pedro to proofread; reused Portuguese (pt_legacy_pairs.json) was proofread before.
"""
import re
import urllib.parse

KEEP = {"Torres Tech Remote", "Android", "iPhone", "Chrome", "Safari", "ES", "EN", "PT", "Alpha Fit Club", "Keon Torres",
        "English", "Español", "Português", "Português (BR)", "Português (PT)", "Deutsch", "Français", "Italiano",
        "Nederlands", "Polski", "Română", "Svenska", "Türkçe", "Bahasa Indonesia", "Čeština", "Tiếng Việt", "Ελληνικά",
        "Русский", "Українська", "العربية", "עברית", "हिन्दी", "日本語", "한국어", "ไทย", "简体中文",
        "pedro_torres@torrestechremote.com", "WhatsApp", "LINE", "Facebook", "Instagram", "YouTube", "QR", "TTR", "OK"}

TRANSLATIONS = {}
TRANSLATIONS.update({'Put it on a phone in under a minute': 'Coloque-o num telemóvel em menos de um minuto', 'Two quick things your customers can do, on iPhone or Android.': 'Duas coisas rápidas que os seus clientes podem fazer, em iPhone ou Android.', 'Add it to the home screen, so it opens like an app': 'Adicione-o ao ecrã principal, para abrir como uma aplicação', 'Save the contact': 'Guarde o contacto', 'Not sure how? We email you these steps to share with your customers, and we can walk you through them by phone or video call, from anywhere in the U.S.': 'Não tem a certeza de como fazer? Enviamos-lhe estes passos por e-mail para partilhar com os seus clientes, e podemos guiá-lo por telefone ou videochamada, a partir de qualquer ponto dos EUA.'})

RAW = [
    ('<li>Open the <b>Chrome</b> browser and type in your card’s link.</li><li>Scroll down and tap <b>Add to home screen</b> on the card.</li><li>Tap <b>Install</b>. The card’s icon is added to your home screen and to your app list.</li>',
     '<li>Abra o navegador <b>Chrome</b> e escreva a ligação do seu cartão.</li><li>Desloque para baixo e toque em <b>Adicionar ao ecrã principal</b> no cartão.</li><li>Toque em <b>Instalar</b>. O ícone do cartão é adicionado ao ecrã principal e à lista de aplicações.</li>'),
    ('<li>Open <b>Chrome</b> and type in your card’s link.</li><li>Scroll down and tap <b>Add to home screen</b> on the card.</li><li>Tap <b>Install</b>.</li>',
     '<li>Abra o <b>Chrome</b> e escreva a ligação do seu cartão.</li><li>Desloque para baixo e toque em <b>Adicionar ao ecrã principal</b> no cartão.</li><li>Toque em <b>Instalar</b>.</li>'),
    ('<li>Open your card.</li><li>Tap the <b>Save contact</b> button.</li><li>Download the file: tap <b>Download</b> in the box that shows the file name (like <b>torres-tech-remote.vcf</b>) and where it will be saved.</li><li>Open the downloaded file.</li><li>On the next screen, tap <b>Import</b> and choose where to save it.</li><li>The contact is now in your contacts list.</li>',
     '<li>Abra o seu cartão.</li><li>Toque no botão <b>Guardar contacto</b>.</li><li>Transfira o ficheiro: toque em <b>Transferir</b> na caixa que mostra o nome do ficheiro (por exemplo, <b>torres-tech-remote.vcf</b>) e onde será guardado.</li><li>Abra o ficheiro transferido.</li><li>No ecrã seguinte, toque em <b>Importar</b> e escolha onde o guardar.</li><li>O contacto já está na sua lista de contactos.</li>'),
    ('<li>Open <b>Safari</b> and type in your card’s link.</li><li>Scroll down and tap <b>Add to home screen</b> on the card.</li><li>Tap <b>Share</b> (the square with an arrow).</li><li>Tap <b>Add to Home Screen</b>, then <b>Add</b>.</li>',
     '<li>Abra o <b>Safari</b> e escreva a ligação do seu cartão.</li><li>Desloque para baixo e toque em <b>Adicionar ao ecrã principal</b> no cartão.</li><li>Toque em <b>Partilhar</b> (o quadrado com uma seta).</li><li>Toque em <b>Adicionar ao ecrã principal</b> e depois em <b>Adicionar</b>.</li>'),
    ('<li>Open <b>Safari</b> and type in your card’s link.</li><li>Scroll down and tap <b>Save contact</b> on the card.</li><li>The contact opens. Tap <b>✓</b> at the top left.</li>',
     '<li>Abra o <b>Safari</b> e escreva a ligação do seu cartão.</li><li>Desloque para baixo e toque em <b>Guardar contacto</b> no cartão.</li><li>O contacto abre. Toque em <b>✓</b> no canto superior esquerdo.</li>'),
]
TRANSLATIONS.update({
"Video: on an iPhone, open the card in Safari, tap Add to home screen on the card, tap Share, tap Add to Home Screen, tap Add, and the card's icon appears on the home screen": "Vídeo: num iPhone, abra o cartão no Safari, toque em Adicionar ao ecrã principal no cartão, toque em Partilhar, toque em Adicionar ao ecrã principal, toque em Adicionar, e o ícone do cartão aparece no ecrã principal",
"Pricing": "Preços", "FAQ": "Perguntas frequentes", "Languages": "Idiomas",
"Design & setup": "Conceção e criação", "Hosting & updates": "Alojamento e atualizações",
"Show all": "Ver todas",
"Email Pedro": "E-mail ao Pedro",
"Install": "Instalar", "Share": "Partilhar", "Add": "Adicionar", "Save contact": "Guardar contacto", "Import": "Importar",
"(some phones say": "(alguns telemóveis dizem", "Save": "Guardar",
"Newark, NJ location": "Local em Newark, NJ",
"Night · English": "Noite · Inglês", "Day · English": "Dia · Inglês", "Night · Spanish": "Noite · Espanhol", "Day · Spanish": "Dia · Espanhol",
"Night · Japanese": "Noite · Japonês", "Day · Japanese": "Dia · Japonês", "Night · Vietnamese": "Noite · Vietnamita", "Day · Vietnamese": "Dia · Vietnamita",
"Book first class": "Reservar primeira aula", "opens booking page": "abre a página de reservas",
"Call": "Ligar", "Text": "Mensagem", "starts a text": "inicia uma mensagem de texto", "Email": "E-mail", "Directions": "Direções",
"switches language": "muda o idioma", "Day / Night": "Dia / Noite", "QR code": "Código QR", "opens a chat": "abre uma conversa",
"No setup fee.": "Sem custo de criação.",
"Option 1": "Opção 1", "Option 2": "Opção 2", "Option 3": "Opção 3",
"Multiple locations": "Vários locais", "Single location, multiple employees": "Um local, vários funcionários",
"Request a quote: multiple locations": "Pedir um orçamento: vários locais",
"Request a quote: multiple employees": "Pedir um orçamento: vários funcionários",
"Request a quote: both": "Pedir um orçamento: ambos",
"Español:": "English:",
"Português:": "Español:",
"Su tarjeta de presentación en el teléfono de sus clientes. Instalación gratis, vista previa gratis.": "Your business card on your customers' phones. Free setup, free preview.",
"Seu cartão de visita no celular dos seus clientes. Criação grátis, prévia grátis.": "Su tarjeta de presentación en el teléfono de sus clientes. Instalación gratis, vista previa gratis.",
"Social links": "Redes sociais", "Torres Tech Remote social links": "Redes sociais da Torres Tech Remote",
"Google review": "Avaliação no Google",
"Alpha Fit Club digital card": "Cartão digital da Alpha Fit Club", "Keon Torres digital card": "Cartão digital do Keon Torres",
"A digital business card QR code": "Código QR de um cartão de visita digital",
"Alpha Fit Club card screenshots": "Capturas do cartão da Alpha Fit Club", "Keon Torres card screenshots": "Capturas do cartão do Keon Torres",
"Previous Alpha Fit Club screenshot": "Captura anterior da Alpha Fit Club", "Next Alpha Fit Club screenshot": "Captura seguinte da Alpha Fit Club",
"Choose a Alpha Fit Club screenshot": "Escolher uma captura da Alpha Fit Club",
"Previous Keon Torres screenshot": "Captura anterior do Keon Torres", "Next Keon Torres screenshot": "Captura seguinte do Keon Torres",
"Step 1": "Passo 1", "Step 2": "Passo 2", "Step 3": "Passo 3",
"What's on your card": "O que leva o seu cartão",
"How it works": "Como funciona",
"Digital business cards · Newark, NJ · online across the U.S.": "Cartões de visita digitais · Newark, NJ · online em todos os EUA",
"Get my free preview →": "Quero a minha pré-visualização grátis →",
"Facebook (opens in a new tab)": "Facebook (abre num novo separador)",
"Instagram (opens in a new tab)": "Instagram (abre num novo separador)",
"YouTube (opens in a new tab)": "YouTube (abre num novo separador)",
"Google review (opens in a new tab)": "Avaliação no Google (abre num novo separador)",
"Free preview.": "Pré-visualização grátis.",
"No payment or credit card required. Just your name, business name, phone and email.": "Sem pagamento nem cartão de crédito. Só o seu nome, o nome do negócio, telefone e e-mail.",
"Free setup": "Criação grátis",
"or $100/year": "ou $100/ano",
"Up to 3 free previews": "Até 3 pré-visualizações grátis",
"pay only if you approve": "só paga se aprovar",
"no setup fee": "sem custo de criação",
"$10/month": "$10/mês",
"YOUR CARD, YOUR BRAND": "O SEU CARTÃO, A SUA MARCA",
"Real cards": "Cartões reais",
"Open the Alpha Fit Club card": "Abrir o cartão da Alpha Fit Club",
"Open the Torres Tech Remote card": "Abrir o cartão da Torres Tech Remote",
"Open the Keon Torres card": "Abrir o cartão do Keon Torres",
"Torres Tech Remote's own digital business card": "O cartão de visita digital da Torres Tech Remote",
"$10/month or $100/year": "$10/mês ou $100/ano",
"In-person service in the Ironbound, Newark NJ ·": "Serviço presencial no Ironbound, Newark, NJ ·",
"Now on Facebook": "Agora no Facebook",
"Tap any card above to try the real thing.": "Toque em qualquer um dos cartões acima para experimentar o verdadeiro.",
"Alpha Fit Club brand shown on the card": "A marca da Alpha Fit Club no cartão",
"One-tap buttons on a digital card": "Botões de um toque num cartão digital",
"Business hours and service pricing on a card": "Horário e preços de serviços num cartão",
"Photo gallery on the Alpha Fit Club card": "Galeria de fotos no cartão da Alpha Fit Club",
"Your photos": "As suas fotos",
"Show your place, your work or your team in a photo gallery customers can swipe.": "Mostre o seu espaço, o seu trabalho ou a sua equipa numa galeria de fotos que os clientes podem deslizar.",
"Torres Tech Remote card with Facebook, Instagram, YouTube, video and Leave a review buttons": "Cartão da Torres Tech Remote com botões de Facebook, Instagram, YouTube, vídeos e Deixar uma avaliação",
"Your socials and reviews": "As suas redes e avaliações",
"Facebook, Instagram, YouTube, your videos, your website and a Leave a review button, so customers can follow you.": "Facebook, Instagram, YouTube, os seus vídeos, o seu site e um botão para deixar uma avaliação, para que os clientes o possam seguir.",
"English and Spanish versions of the Alpha Fit Club card": "Versões em inglês e espanhol do cartão da Alpha Fit Club",
"Alpha Fit Club November events promotion on the card": "Promoção dos eventos de novembro da Alpha Fit Club no cartão",
"Alpha Fit Club promotional poster on the card": "Cartaz promocional da Alpha Fit Club no cartão",
"Easy to share, and it lasts": "Fácil de partilhar, e dura",
"QR code, Share and Save contact. Your QR code never changes, so printed codes keep working.": "Código QR, Partilhar e Guardar contacto. O seu código QR nunca muda, por isso os códigos impressos continuam a funcionar.",
"Works like an app": "Funciona como uma aplicação",
"Customers save your card to their phone in a few taps. It gets its own icon, opens full screen like an app, and still opens without internet. No app store and no download. Pick your phone to watch how:": "Os clientes guardam o seu cartão no telemóvel com alguns toques. Tem o seu próprio ícone, abre em ecrã inteiro como uma aplicação e abre mesmo sem internet. Sem loja de aplicações e sem transferir nada. Escolha o seu telemóvel para ver como:",
"Open the card in": "Abra o cartão no",
"Tap": "Toque em",
"Add to home screen": "Adicionar ao ecrã principal",
"on the card.": "no cartão.",
"(iPhone or iPad).": "(iPhone ou iPad).",
"(the square with an arrow).": "(o quadrado com uma seta).",
"Add to Home Screen": "Adicionar ao ecrã principal",
", then": ", e depois em",
"Saved in their contacts": "Guardado nos contactos",
"“Save contact” adds your business to their contacts with your logo, phone, email, address and website, so they can find you and call you later. Pick your phone to watch how:": "“Guardar contacto” adiciona o seu negócio aos contactos do cliente com o seu logótipo, telefone, e-mail, morada e site, para que o possam encontrar e ligar-lhe mais tarde. Escolha o seu telemóvel para ver como:",
"It downloads. Tap": "É transferido. Toque em",
"Open": "Abrir",
"The contact opens. Tap": "O contacto abre. Toque em",
"at the top left.": "no canto superior esquerdo.",
"These are screenshots. On the real card, every button works when you tap it.": "São capturas de ecrã. No cartão real, cada botão funciona ao tocar.",
"Show all Alpha Fit Club card screenshots": "Ver todas as capturas do cartão da Alpha Fit Club",
"Show all Keon Torres card screenshots": "Ver todas as capturas do cartão do Keon Torres",
"rings the gym": "toca no ginásio",
"writes to the gym": "escreve ao ginásio",
"opens the map": "abre o mapa",
"switches the look": "muda o aspeto",
"send the card": "envia o cartão",
"adds to phone": "adiciona ao telemóvel",
"scan to open": "leia para abrir",
"Message on LINE": "Mensagem por LINE",
"writes to him": "escreve-lhe",
"installs like an app": "instala-se como uma aplicação",
"“Great product. Great service. Best digital business card out there! I’ve had several and this is the most interactive I’ve had. Pete’s very accommodating and works with you on all the details till it’s just right. So happy to do business with Torres Tech Remote!”": "“Great product. Great service. Best digital business card out there! I’ve had several and this is the most interactive I’ve had. Pete’s very accommodating and works with you on all the details till it’s just right. So happy to do business with Torres Tech Remote!”",
"Free preview form with required name and business name fields": "Formulário de pré-visualização grátis com os campos obrigatórios de nome e nome do negócio",
"Fill out our Free Preview form": "Preencha o nosso formulário de pré-visualização grátis",
"Only your name, business name, phone, email and a confirmation checkbox are required. All other questions are optional.": "Só são pedidos o seu nome, o nome do negócio, telefone, e-mail e uma caixa de confirmação. As restantes perguntas são opcionais.",
"A watermarked digital business card preview for Navalha Barber Co.": "Pré-visualização com marca de água de um cartão digital da Navalha Barber Co.",
"Get your free preview": "Receba a sua pré-visualização grátis",
"We create your free digital business card preview from the information you give us and email it to you for review. You can receive up to 3 free previews. You only pay if you approve your card.": "Criamos a pré-visualização grátis do seu cartão de visita digital com os dados que nos der e enviamo-la por e-mail para a rever. Pode receber até 3 pré-visualizações grátis. Só paga se aprovar o seu cartão.",
"The live Navalha Barber Co. digital card with contact buttons and hours": "O cartão digital em direto da Navalha Barber Co. com botões de contacto e horário",
"Pick up to 3 languages for your card, like Spanish, Portuguese, Chinese, Japanese and Arabic. Customers switch between them on the card.": "Escolha até 3 idiomas para o seu cartão, como espanhol, português, chinês, japonês e árabe. Os clientes mudam entre eles no cartão.",
"Who makes your card": "Quem faz o seu cartão",
"Send me your business name and I’ll make you a free preview and send you a link to review. You only pay if you like it.": "Envie-me o nome do seu negócio e faço-lhe uma pré-visualização grátis com uma ligação para a rever. Só paga se gostar.",
"Fill in the form →": "Preencha o formulário →",
"Certified IT technician. I set up and look after your card myself.": "Técnico de TI certificado. Eu próprio preparo e cuido do seu cartão.",
"Your logo and brand colors": "O seu logótipo e as cores da sua marca",
"Call, text, WhatsApp, email, directions and website buttons": "Botões de chamada, mensagem, WhatsApp, e-mail, direções e site",
"Hours, services and prices, photos, payment links": "Horário, serviços e preços, fotos e ligações de pagamento",
"QR code, Share and Save contact": "Código QR, Partilhar e Guardar contacto",
"Up to 3 of 25 languages": "Até 3 de 25 idiomas",
"Installs like an app on iPhone and Android, no app store": "Instala-se como uma aplicação no iPhone e no Android, sem loja de aplicações",
"Up to 3 free previews before you pay": "Até 3 pré-visualizações grátis antes de pagar",
"or": "ou",
"$100 per year": "$100 por ano",
", 2 months free": ", 2 meses grátis",
"Hosting and security updates": "Alojamento e atualizações de segurança",
"Unlimited changes to your hours, prices, photos and links": "Alterações ilimitadas ao seu horário, preços, fotos e ligações",
"Your QR code never changes, so printed codes keep working": "O seu código QR nunca muda, por isso os códigos impressos continuam a funcionar",
"For businesses": "Para negócios",
"Select the option that fits your organization, or combine them. Each business is different, so we provide a custom quote based on your number of locations and employees. Setup is free.": "Escolha a opção que se adequa à sua organização, ou combine-as. Cada negócio é diferente, por isso damos um orçamento à medida com base no número de locais e funcionários. A criação é grátis.",
"Run a gym or fitness studio?": "Tem um ginásio ou um estúdio de fitness?",
"See the digital business card for gyms": "Veja o cartão de visita digital para ginásios",
"A single card lists every location, each with its own address, directions, phone number and hours. Suited to retail, fitness and multi-site businesses.": "Um só cartão mostra cada local, cada um com a sua morada, direções, telefone e horário. Ideal para comércio, fitness e negócios com várias sedes.",
"See an example: Corner Table Café": "Ver um exemplo: Corner Table Café",
"Each employee receives an individual card with their name, photo and contact details. One office card lists the entire team.": "Cada funcionário recebe o seu próprio cartão com o nome, foto e dados de contacto. Um cartão do escritório mostra toda a equipa.",
"See an example: Harbor Realty": "Ver um exemplo: Harbor Realty",
"Multiple locations and employees": "Vários locais e funcionários",
"Multiple locations with individual employee cards. Each employee can be assigned to the location where they work.": "Vários locais com cartões individuais de funcionários. Cada funcionário pode ser atribuído ao local onde trabalha.",
"See an example: Brightside Dental": "Ver um exemplo: Brightside Dental",
"Request your free preview →": "Peça a sua pré-visualização grátis →",
"Free preview. No payment or credit card required. Just your name, business name, phone and email to get started.": "Pré-visualização grátis. Sem pagamento nem cartão de crédito. Só o seu nome, o nome do negócio, telefone e e-mail para começar.",
"See it live:": "Veja-o em direto:",
})


def PAGE(s):
    s = re.sub(r'<link href="[^"]*" hreflang="[^"]*" rel="alternate"/>\n', "", s)
    s = s.replace('<link href="https://torrestechremote.com/pt/" rel="canonical"/>\n',
        '<link href="https://torrestechremote.com/pt/" rel="canonical"/>\n'
        '<link href="https://torrestechremote.com/" hreflang="en" rel="alternate"/>\n'
        '<link href="https://torrestechremote.com/es/" hreflang="es" rel="alternate"/>\n'
        '<link href="https://torrestechremote.com/pt/" hreflang="pt-PT" rel="alternate"/>\n'
        '<link href="https://torrestechremote.com/" hreflang="x-default" rel="alternate"/>\n', 1)
    s = s.replace('<b aria-current="page">EN</b> · <a hreflang="es" lang="es" href="/es/">ES</a> · <a hreflang="pt-PT" lang="pt-PT" href="/pt/">PT</a>',
                  '<a hreflang="en" lang="en" href="/">EN</a> · <a hreflang="es" lang="es" href="/es/">ES</a> · <b aria-current="page">PT</b>')
    s = s.replace('<a href="/" aria-current="page">English</a><a hreflang="es" lang="es" href="/es/">Español</a><a hreflang="pt-PT" lang="pt-PT" href="/pt/">Português</a>',
                  '<a hreflang="en" lang="en" href="/">English</a><a hreflang="es" lang="es" href="/es/">Español</a><a href="/pt/" aria-current="page">Português</a>')
    s = s.replace('/pt/', '/pt/').replace('/es/', '/es/')
    s = s.replace('href="/digital-business-card-for-gyms/"', 'href="/pt/cartao-digital-ginasio/"')
    s = s.replace('href="/go/preview.html"', 'href="/go/preview-pt.html"')
    s = s.replace('https://docs.google.com/forms/d/e/1FAIpQLSenglfDQ0WaNQpeYR2ZBD-Y4AP6W5HduUZSNqFPebuN1tnx-Q/viewform', '/go/preview-pt.html')
    sms = urllib.parse.quote("Olá Pedro, gostaria de uma pré-visualização grátis para o meu negócio: ", safe="")
    s = re.sub(r'href="sms:\+12017722106\?&amp;body=[^"]*"', 'href="sms:+12017722106?&amp;body=%s"' % sms, s)
    body = ("Olá, gostaria de uma pré-visualização grátis de um cartão de visita digital.\n\nNome do negócio: \nTelefone do negócio: \nE-mail do negócio: \nMorada ou zona: \nHorário: \n"
            "Serviços (e preços, se quiser que sejam mostrados): \nComo os clientes reservam, encomendam ou pedem orçamento (ligação de uma aplicação, ou chamada/mensagem/WhatsApp): \nCores da marca (se houver): \nSite, Instagram ou Facebook (se houver): \n\nAnexe o seu logótipo e algumas fotos, se as tiver.")
    subj = "Pré-visualização grátis: cartão de visita digital"
    s = re.sub(r'href="mailto:pedro_torres@torrestechremote\.com\?subject=[^"]*"',
               'href="mailto:pedro_torres@torrestechremote.com?subject=%s&amp;body=%s"' % (urllib.parse.quote(subj, safe=""), urllib.parse.quote(body, safe="")), s)
    OT = "Cartões de visita digitais para o seu negócio, cada local e a sua equipa"
    OD = "Para pequenos negócios em todos os EUA: uma ligação e um código QR para cada local, um cartão para cada pessoa, e nós tratamos das suas atualizações. Criação grátis, depois $10/mês. Pré-visualização grátis antes de pagar."
    s = s.replace('content="Digital Business Cards for Your Business, Every Location, and Your Team"', 'content="%s"' % OT)
    s = s.replace('content="For small businesses across the U.S.: one link and one QR code for each location, a card for each person, and we do your updates. Free setup, then $10/month. Free preview before you pay."', 'content="%s"' % OD)
    s = s.replace('"@id": "https://torrestechremote.com/#webpage",\n      "url": "https://torrestechremote.com/",\n      "name": "Digital Business Cards for Small Businesses Across the U.S.",',
                  '"@id": "https://torrestechremote.com/pt/#webpage",\n      "url": "https://torrestechremote.com/pt/",\n      "inLanguage": "pt-PT",\n      "name": "Cartões de visita digitais para pequenos negócios em todos os EUA",')
    s = s.replace('"serviceType": "Digital business card design and hosting"', '"serviceType": "Conceção e alojamento de cartões de visita digitais"')
    s = s.replace('"name": "Design & setup"', '"name": "Conceção e criação"').replace('"description": "Free"', '"description": "Grátis"')
    s = s.replace('"name": "Hosting & updates, monthly"', '"name": "Alojamento e atualizações, mensal"').replace('"name": "Hosting & updates, yearly"', '"name": "Alojamento e atualizações, anual"')
    for a, b in (("Night · English", "Noite · Inglês"), ("Day · English", "Dia · Inglês"), ("Night · Spanish", "Noite · Espanhol"), ("Day · Spanish", "Dia · Espanhol"),
                 ("Night · Japanese", "Noite · Japonês"), ("Day · Japanese", "Dia · Japonês"), ("Night · Vietnamese", "Noite · Vietnamita"), ("Day · Vietnamese", "Dia · Vietnamita")):
        s = s.replace(", " + a + '"', ", " + b + '"')
    s = s.replace("<b>Técnico de TI certificado CompTIA A+</b>", "<b>Certificado CompTIA A+</b>")
    s = s.replace('<span lang="es">Your business card', '<span lang="en">Your business card')
    s = s.replace('<span lang="pt-BR">Su tarjeta', '<span lang="es">Su tarjeta')
    s = s.replace('<a href="#card">O que leva o seu cartão</a>', '<a href="#card">O seu cartão</a>')
    s = s.replace('<a href="#faq">Perguntas frequentes</a>', '<a href="#faq">Perguntas</a>')
    s = s.replace('"Checking…"', '"A verificar…"')
    s = s.replace('"That code doesn’t match. Check the code we sent with your preview."', '"Esse código não corresponde. Verifique o código que lhe enviámos com a sua pré-visualização."')
    s = s.replace('"This browser can’t unlock the links. Email us for your payment link."', '"Este navegador não consegue desbloquear as ligações. Escreva-nos para receber a sua ligação de pagamento."')
    return s
