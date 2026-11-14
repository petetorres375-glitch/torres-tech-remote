#!/usr/bin/env python3
"""Builds the English one-page home (new orange look) from the pieces in this repo.

  python3 _tools/build_home_en.py            -> writes index-new.html (local preview only)
  python3 _tools/build_home_en.py --live     -> writes index.html (the real home page)

Shared files: home.css (look), home.js (behaviour), _tools/order-locks.js (encrypted pay links),
_tools/order-unlock-en.js (the unlock-code box). Edit those, then rebuild.
"""
import pathlib, sys

root = pathlib.Path(__file__).resolve().parent.parent
locks = (root / "_tools/order-locks.js").read_text(encoding="utf-8")
unlock = (root / "_tools/order-unlock-en.js").read_text(encoding="utf-8")

ANDROID = '<svg aria-hidden="true" fill="#3ddc84" viewBox="0 0 24 24"><path d="M17.6 9.48l1.84-3.18a.38.38 0 0 0-.66-.38l-1.86 3.22a11.4 11.4 0 0 0-9.84 0L5.22 5.92a.38.38 0 0 0-.66.38L6.4 9.48A10.8 10.8 0 0 0 1 18h22a10.8 10.8 0 0 0-5.4-8.52zM7 15.25a1.25 1.25 0 1 1 0-2.5 1.25 1.25 0 0 1 0 2.5zm10 0a1.25 1.25 0 1 1 0-2.5 1.25 1.25 0 0 1 0 2.5z"/></svg>'
IOS = '<svg aria-hidden="true" fill="currentColor" viewBox="0 0 24 24"><path d="M16.37 12.6c-.02-2.3 1.88-3.4 1.96-3.46a4.2 4.2 0 0 0-3.3-1.8c-1.4-.14-2.74.83-3.45.83-.72 0-1.8-.81-2.97-.79A4.4 4.4 0 0 0 4.9 9.64c-1.6 2.77-.41 6.86 1.14 9.1.76 1.1 1.66 2.33 2.84 2.29 1.14-.05 1.57-.74 2.95-.74 1.37 0 1.76.74 2.97.71 1.23-.02 2-1.11 2.75-2.22a9.7 9.7 0 0 0 1.25-2.57 3.97 3.97 0 0 1-2.43-3.61zM14.1 5.86A4 4 0 0 0 15.04 3a4.1 4.1 0 0 0-2.67 1.38 3.8 3.8 0 0 0-.96 2.77 3.4 3.4 0 0 0 2.69-1.29z"/></svg>'
IOS_DARK = IOS.replace('fill="currentColor"', 'fill="#141a2b"')

SOCIAL = '''<a aria-label="Facebook (opens in a new tab)" class="social-link" href="https://www.facebook.com/profile.php?id=61595452617390" rel="noopener noreferrer" target="_blank" title="Facebook"><svg aria-hidden="true" focusable="false" viewBox="0 0 24 24"><path d="M14 21v-8h3l.5-4H14V7c0-1 .3-2 2-2h2V1.5A23 23 0 0 0 15 1c-3 0-5 2-5 5v3H7v4h3v8z"/></svg></a><a aria-label="Instagram (opens in a new tab)" class="social-link" href="https://www.instagram.com/torrestechremote/" rel="noopener noreferrer" target="_blank" title="Instagram"><svg aria-hidden="true" focusable="false" viewBox="0 0 24 24"><rect height="18" rx="5" width="18" x="3" y="3"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/></svg></a><a aria-label="YouTube (opens in a new tab)" class="social-link" href="https://www.youtube.com/@torrestechremote" rel="noopener noreferrer" target="_blank" title="YouTube"><svg aria-hidden="true" focusable="false" viewBox="0 0 24 24"><rect height="14" rx="4" width="20" x="2" y="5"/><path d="m10 9 5 3-5 3z"/></svg></a><a aria-label="Google review (opens in a new tab)" class="social-link" href="https://g.page/r/CcmkhrdSiKwmEBM/review" rel="noopener noreferrer" target="_blank" title="Google review"><svg aria-hidden="true" focusable="false" viewBox="0 0 24 24"><path d="M20.5 12.2c0 5-3.4 8.3-8.4 8.3a8.5 8.5 0 1 1 6-14.5l-2.5 2.5a5 5 0 1 0 1.2 5.2H12v-3.3h8.3c.1.6.2 1.1.2 1.8z"/></svg></a>'''

QUOTE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSenglfDQ0WaNQpeYR2ZBD-Y4AP6W5HduUZSNqFPebuN1tnx-Q/viewform"
SMS = "sms:+12017722106?&amp;body=Hi%20Pedro%2C%20I%27d%20like%20a%20free%20preview%20for%20my%20business%3A%20"
MAILTO = "mailto:pedro_torres@torrestechremote.com?subject=Free%20preview%3A%20digital%20business%20card&amp;body=Hi%2C%20I%27d%20like%20a%20free%20preview%20of%20a%20digital%20business%20card.%0A%0ABusiness%20name%3A%20%0ABusiness%20phone%3A%20%0ABusiness%20email%3A%20%0AAddress%20or%20area%3A%20%0AHours%3A%20%0AServices%20%28and%20prices%2C%20if%20you%20want%20them%20shown%29%3A%20%0AHow%20customers%20book%2C%20order%20or%20get%20a%20quote%20%28app%20link%2C%20or%20call%2Ftext%2FWhatsApp%29%3A%20%0ABrand%20colors%20%28if%20any%29%3A%20%0AWebsite%2C%20Instagram%20or%20Facebook%20%28if%20any%29%3A%20%0A%0APlease%20attach%20your%20logo%20and%20a%20few%20photos%20if%20you%20have%20them."
PREVIEW = "/go/preview.html"

LANGS = [("", "English"), ("es", "Español"), ("pt-BR", "Português (BR)"), ("pt-PT", "Português (PT)"), ("ar", "العربية"),
         ("cs", "Čeština"), ("de", "Deutsch"), ("el", "Ελληνικά"), ("fr", "Français"), ("he", "עברית"), ("hi", "हिन्दी"),
         ("id", "Bahasa Indonesia"), ("it", "Italiano"), ("ja", "日本語"), ("ko", "한국어"), ("nl", "Nederlands"),
         ("pl", "Polski"), ("ro", "Română"), ("ru", "Русский"), ("sv", "Svenska"), ("th", "ไทย"), ("tr", "Türkçe"),
         ("uk", "Українська"), ("vi", "Tiếng Việt"), ("zh", "简体中文")]
lang_html = "".join(
    f'<span{(" lang=%s" % chr(34) + l + chr(34)) if l else ""}{(" dir=%s" % chr(34) + "rtl" + chr(34)) if l in ("ar", "he") else ""}>{n}</span>'
    for l, n in LANGS)


def fig(src, alt, cap, w=260, h=793):
    return f'<figure><img alt="{alt}" loading="lazy" src="/img/{src}" height="{h}" width="{w}"/><figcaption>{cap}</figcaption></figure>'


def carousel(name, first, h, shots):
    figs = "".join(fig(f, f"{name} card, {c}", c, 260, h) for f, c in shots)
    return f'''<div class="client-carousel" data-client-carousel>
<button class="shot-launch" type="button" aria-label="Show all {name} card screenshots">
<img src="/img/{first}" alt="{name} card, {shots[0][1]}" loading="lazy" height="{h}" width="260"/>
<span class="tap-hint">Tap to see more</span>
</button>
<div class="shots" aria-label="{name} card screenshots">{figs}</div>
<div class="carousel-tools">
<button class="carousel-arrow" type="button" data-prev aria-label="Previous {name} screenshot">&#8592;</button>
<div class="carousel-dots" aria-label="Choose a {name} screenshot"></div>
<button class="carousel-arrow" type="button" data-next aria-label="Next {name} screenshot">&#8594;</button>
<button class="carousel-close" type="button" data-close>Close</button>
</div>
</div>'''


def os_block(clip_id, kicker, title, text, android_video, android_steps, ios_video, ios_steps, clip):
    return f'''<div class="install reveal" id="{clip_id}">
<div>
<p class="eyebrow">{kicker}</p>
<h3>{title}</h3>
<p class="txt">{text} Pick your phone to watch how:</p>
<div aria-label="Pick your phone" class="os-pick" role="group"><button aria-pressed="false" data-pick="android" type="button">{ANDROID}Android</button><button aria-pressed="false" data-pick="ios" type="button">{IOS}iPhone</button></div>
</div>
<div class="os-grid">
<div class="os" data-os="android">
<h4>{ANDROID}Android</h4>
<div class="os-video"><video aria-label="{android_video}" height="1168" loop="" muted="" playsinline="" poster="/video/{clip}-android.webp" preload="none" src="/video/{clip}-android.mp4" width="540"></video></div>
<ol>{android_steps}</ol>
</div>
<div class="os" data-os="ios">
<h4>{IOS_DARK}iPhone</h4>
<div class="os-video"><video aria-label="{ios_video}" height="1168" loop="" muted="" playsinline="" poster="/video/{clip}-ios.webp" preload="none" src="/video/{clip}-ios.mp4" width="540"></video></div>
<ol>{ios_steps}</ol>
</div>
</div>
</div>'''


install = os_block(
    "install", "Works like an app", "Your card on their home screen.",
    "Customers save your card to their phone in a few taps. It gets its own icon, opens full screen like an app, and still opens without internet. No app store and no download.",
    "Video: on an Android phone, open the card in Chrome, tap Add to home screen, tap Install, and the card's icon appears on the home screen",
    "<li>Open the <b>Chrome</b> browser and type in your card’s link.</li><li>Scroll down and tap <b>Add to home screen</b> on the card.</li><li>Tap <b>Install</b>. The card’s icon is added to your home screen and to your app list.</li>",
    "Video: on an iPhone, open the card in Safari, tap Add to home screen on the card, tap Share, tap Add to Home Screen, tap Add, and the card's icon appears on the home screen",
    "<li>Open <b>Safari</b> and type in your card’s link.</li><li>Scroll down and tap <b>Add to home screen</b> on the card.</li><li>Tap <b>Share</b> (the square with an arrow).</li><li>Tap <b>Add to Home Screen</b>, then <b>Add</b>.</li>",
    "install")
contact = os_block(
    "save-contact", "Saved in their contacts", "In their contacts in seconds.",
    "“Save contact” adds your business to their contacts with your logo, phone, email, address and website, so they can find you and call you later.",
    "Video: on an Android phone, tap Save contact on the card, it downloads, tap Open, then tap Import, and the business is in the phone's contacts",
    "<li>Open your card.</li><li>Tap the <b>Save contact</b> button.</li><li>Download the file: tap <b>Download</b> in the box that shows the file name (like <b>torres-tech-remote.vcf</b>) and where it will be saved.</li><li>Open the downloaded file.</li><li>On the next screen, tap <b>Import</b> and choose where to save it.</li><li>The contact is now in your contacts list.</li>",
    "Video: on an iPhone, tap Save contact on the card, the contact opens, tap the check mark at the top left, and the business is in the phone's contacts",
    "<li>Open <b>Safari</b> and type in your card’s link.</li><li>Scroll down and tap <b>Save contact</b> on the card.</li><li>The contact opens. Tap <b>✓</b> at the top left.</li>",
    "contact")

def _grab(block):
    import re as _re
    return block

_ios_inst = "<li>Open <b>Safari</b> and type in your card’s link.</li><li>Scroll down and tap <b>Add to home screen</b> on the card.</li><li>Tap <b>Share</b> (the square with an arrow).</li><li>Tap <b>Add to Home Screen</b>, then <b>Add</b>.</li>"
_and_inst = "<li>Open the <b>Chrome</b> browser and type in your card’s link.</li><li>Scroll down and tap <b>Add to home screen</b> on the card.</li><li>Tap <b>Install</b>. The card’s icon is added to your home screen and to your app list.</li>"
_ios_con = "<li>Open <b>Safari</b> and type in your card’s link.</li><li>Scroll down and tap <b>Save contact</b> on the card.</li><li>The contact opens. Tap <b>✓</b> at the top left.</li>"
_and_con = "<li>Open your card.</li><li>Tap the <b>Save contact</b> button.</li><li>Download the file: tap <b>Download</b> in the box that shows the file name (like <b>torres-tech-remote.vcf</b>) and where it will be saved.</li><li>Open the downloaded file.</li><li>On the next screen, tap <b>Import</b> and choose where to save it.</li><li>The contact is now in your contacts list.</li>"
assert _ios_inst in install and _and_inst in install and _ios_con in contact and _and_con in contact
phone = f'''<div class="gsec phone-sec reveal" id="install"><div class="center"><h2>Put it on a phone in under a minute</h2><p class="sub">Two quick things your customers can do, on iPhone or Android.</p>
<div class="gcards gphones">
<div class="gcard gphone"><h3>iPhone</h3><h4>Add it to the home screen, so it opens like an app</h4><ol class="gsteps">{_ios_inst}</ol><h4 id="save-contact">Save the contact</h4><ol class="gsteps">{_ios_con}</ol></div>
<div class="gcard gphone"><h3>Android</h3><h4>Add it to the home screen, so it opens like an app</h4><ol class="gsteps">{_and_inst}</ol><h4>Save the contact</h4><ol class="gsteps">{_and_con}</ol></div>
</div>
<p class="ghelp">Not sure how? We email you these steps to share with your customers, and we can walk you through them by phone or video call, from anywhere in the U.S.</p></div></div>'''

ICONS = {
    "brand": '<circle cx="12" cy="12" r="9"/><circle cx="8.5" cy="10" r="1.2"/><circle cx="15.5" cy="10" r="1.2"/><path d="M8 15c1.2 1.4 2.6 2 4 2s2.8-.6 4-2"/>',
}

keon = carousel("Keon Torres", "feat-keon-night.webp", 793, [
    ("feat-keon-night.webp", "Night · English"), ("feat-keon-day.webp", "Day · English"),
    ("feat-keon-ja.webp", "Night · Japanese"), ("feat-keon-ja-day.webp", "Day · Japanese"),
    ("feat-keon-vi.webp", "Night · Vietnamese"), ("feat-keon-vi-day.webp", "Day · Vietnamese")])
alpha = carousel("Alpha Fit Club", "feat-alpha-night.webp", 1133, [
    ("feat-alpha-night.webp", "Night · English"), ("feat-alpha-day.webp", "Day · English"),
    ("feat-alpha-es.webp", "Night · Spanish"), ("feat-alpha-es-day.webp", "Day · Spanish")])

FAQ = [
    ("What does it cost?", 'Design and setup are free. You pay $10 per month for hosting and updates, or $100 per year (2 months free). Up to 3 free previews before you pay. For several locations or employees, request a custom quote <a href="#teams">here</a>.'),
    ("Which languages can my card show?", 'Up to 3 of 25 languages, like Spanish, Portuguese, Chinese, Japanese and Arabic. See the <a href="#languages">full list</a>.'),
    ("Do my customers need to download an app?", 'No. The card opens from its link or QR code. Customers can also save it to their home screen like an app, no app store. On Android, open it in Chrome and tap <b>Add to home screen</b>, then <b>Install</b>. On iPhone or iPad, open it in Safari, tap <b>Share</b>, then <b>Add to Home Screen</b>. <a href="#install">See the steps</a>.'),
    ("Can customers book, order or get a quote from my card?", 'Yes. Your card’s main button, like Book now, Order online or Get a quote, opens the booking, ordering or quote page you already use, such as Square, Booksy, OpenTable or DoorDash. Or it can call, text or WhatsApp you. It works for barbers and salons, cafés and restaurants, contractors, pest control and more.'),
    ("Can I change my hours or prices later?", 'Yes. Hosting includes unlimited changes to your hours, prices, photos and links. Your QR code never changes, so printed codes keep working.'),
    ("How do I pay?", 'Card accepted online and in person. Cash in person for yearly plans. After you approve your free preview, pay online with the <a data-open-order="" href="#order">payment links</a>.'),
    ("Can one card cover several locations?", 'Yes. One card lists every location, each with its own address, directions, phone number and hours. Each location can also have its own QR code, so a customer who scans it at that location lands on that location. See the <a href="#teams">examples</a>.'),
    ("Can each of my employees have their own card?", 'Yes. Each employee receives an individual card with their name, photo and contact details. One office card lists the entire team, and each person can be assigned to the location where they work.'),
    ("How much does it cost for several locations or employees?", f'Each business is different, so we provide a custom quote based on your number of locations and employees. Setup is free. The business pays for all the cards. <a href="{QUOTE_FORM}" rel="noopener nofollow" target="_blank">Request a quote</a>.'),
    ("What happens when we add or lose an employee?", 'You can add people at any time and they are billed for the rest of that year. If someone leaves, you can give their place to a new person at no charge. Please tell us by the 1st of the month, and we make the change that week.'),
    ("What if one of my locations is a franchise?", 'A location owned by another business is a separate customer with its own card and its own bill. It can link back to your main card if you both agree.'),
    ("Who can order a card?", 'In-person service in the Ironbound, Newark NJ; online orders available in the US and its territories, and to US citizens abroad paying with a US card or bank account.'),
]
faq_html = "".join(f'<details><summary>{q}</summary><div class="faq-answer">{a}</div></details>' for q, a in FAQ)

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>Digital Business Cards for Small Businesses Across the U.S. | Torres Tech Remote</title>
<meta content="Digital business cards for one business, every location, and your whole team. One link and one QR code; customers call, text, email or save you in one tap, in up to 3 of 25 languages. Free setup, then $10/month. Free preview before you pay." name="description"/>
<link href="https://torrestechremote.com/" rel="canonical"/>
<link href="https://torrestechremote.com/" hreflang="en" rel="alternate"/>
<link href="https://torrestechremote.com/es/" hreflang="es" rel="alternate"/>
<link href="https://torrestechremote.com/pt/" hreflang="pt-PT" rel="alternate"/>
<link href="https://torrestechremote.com/" hreflang="x-default" rel="alternate"/>
<link href="/favicon/ttr-16.png" rel="icon" sizes="16x16" type="image/png"/>
<link href="/favicon/ttr-32.png" rel="icon" sizes="32x32" type="image/png"/>
<link href="/favicon/ttr-192.png" rel="icon" sizes="192x192" type="image/png"/>
<link href="/favicon/ttr.ico" rel="shortcut icon"/>
<link href="/favicon/ttr-180.png" rel="apple-touch-icon" sizes="180x180"/>
<meta content="website" property="og:type"/>
<meta content="https://torrestechremote.com/" property="og:url"/>
<meta content="Digital Business Cards for Your Business, Every Location, and Your Team" property="og:title"/>
<meta content="For small businesses across the U.S.: one link and one QR code for each location, a card for each person, and we do your updates. Free setup, then $10/month. Free preview before you pay." property="og:description"/>
<meta content="https://torrestechremote.com/og-business-cards.jpg" property="og:image"/>
<meta content="1200" property="og:image:width"/>
<meta content="630" property="og:image:height"/>
<meta content="Torres Tech Remote: digital business cards for small businesses across the U.S., for one business, every location, and your whole team" property="og:image:alt"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="Digital Business Cards for Your Business, Every Location, and Your Team" name="twitter:title"/>
<meta content="For small businesses across the U.S.: one link and one QR code for each location, a card for each person, and we do your updates. Free setup, then $10/month. Free preview before you pay." name="twitter:description"/>
<meta content="https://torrestechremote.com/og-business-cards.jpg" name="twitter:image"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/>
<link href="/home.css" rel="stylesheet"/>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://torrestechremote.com/#organization",
      "name": "Torres Tech Remote",
      "url": "https://torrestechremote.com/",
      "logo": "https://torrestechremote.com/favicon/ttr-512.png",
      "email": "support@torrestechremote.com",
      "telephone": "+12017722106",
      "sameAs": [
        "https://www.facebook.com/profile.php?id=61595452617390",
        "https://www.instagram.com/torrestechremote/",
        "https://www.youtube.com/@torrestechremote"
      ],
      "founder": { "@type": "Person", "name": "Pedro Torres" }
    },
    {
      "@type": "WebSite",
      "@id": "https://torrestechremote.com/#website",
      "name": "Torres Tech Remote",
      "url": "https://torrestechremote.com/",
      "publisher": { "@id": "https://torrestechremote.com/#organization" }
    },
    {
      "@type": "WebPage",
      "@id": "https://torrestechremote.com/#webpage",
      "url": "https://torrestechremote.com/",
      "name": "Digital Business Cards for Small Businesses Across the U.S.",
      "isPartOf": { "@id": "https://torrestechremote.com/#website" },
      "about": { "@id": "https://torrestechremote.com/#service" },
      "publisher": { "@id": "https://torrestechremote.com/#organization" }
    },
    {
      "@type": "Service",
      "@id": "https://torrestechremote.com/#service",
      "name": "Digital Business Cards",
      "serviceType": "Digital business card design and hosting",
      "description": "One link and one QR code for your business, every location, and your team. Customers call, text or email you in one tap, save you to their contacts, and read it in up to 3 of 25 languages. We design it, host it and keep it up to date.",
      "url": "https://torrestechremote.com/",
      "provider": { "@id": "https://torrestechremote.com/#organization" },
      "areaServed": [
        { "@type": "Country", "name": "United States" },
        { "@type": "Place", "name": "Ironbound, Newark, NJ" }
      ],
      "offers": [
        { "@type": "Offer", "name": "Design & setup", "price": "0", "priceCurrency": "USD", "description": "Free" },
        { "@type": "Offer", "name": "Hosting & updates, monthly", "price": "10", "priceCurrency": "USD",
          "priceSpecification": { "@type": "UnitPriceSpecification", "price": "10", "priceCurrency": "USD", "unitCode": "MON" } },
        { "@type": "Offer", "name": "Hosting & updates, yearly", "price": "100", "priceCurrency": "USD",
          "priceSpecification": { "@type": "UnitPriceSpecification", "price": "100", "priceCurrency": "USD", "unitCode": "ANN" } }
      ]
    }
  ]
}
</script>
</head>
'''

BODY = f'''<body id="top" class="no-js">
<script>document.body.classList.remove("no-js")</script>
<nav class="top"><div class="wrap nav">
<a class="brand" href="/"><img alt="TTR" src="/img/ttr-monogram.webp" width="61" height="40"/> Torres Tech Remote</a>
<div class="links"><a href="#card">What's on your card</a><a href="#clients">Real cards</a><a href="#how">How it works</a><a href="#pricing">Pricing</a><a href="#faq">FAQ</a></div>
<div class="nav-r"><span class="lang"><b aria-current="page">EN</b> · <a hreflang="es" lang="es" href="/es/">ES</a> · <a hreflang="pt-PT" lang="pt-PT" href="/pt/">PT</a></span><a class="btn btn-p btn-sm" href="{PREVIEW}" rel="noopener nofollow" target="_blank">Free preview</a></div>
</div></nav>
<main>
<header class="hero"><div class="wrap hero-g">
<div>
<span class="pill"><i></i> Digital business cards · Newark, NJ · online across the U.S.</span>
<h1>A business card your customers <em>keep on their phone.</em></h1>
<p class="lead">One link and one QR code for your shop. Customers call, text, WhatsApp or email you in one tap and save you to their contacts. Your card opens in your customer's own phone language, and they can tap to switch. We design it, host it and keep it up to date. You never touch an app.</p>
<div class="cta">
<a class="btn btn-p" href="{PREVIEW}" rel="noopener nofollow" target="_blank">Get my free preview →</a>
<a class="btn btn-s" href="https://cards.torrestechremote.com/navalha-barber-co/" rel="noopener" target="_blank">See the demo card</a>
</div>
<div class="cta-2">
<a class="btn btn-s btn-sm" href="tel:+12017722106">Call (201) 772-2106</a>
<a class="btn btn-s btn-sm" href="{SMS}">Text Pedro</a>
</div>
<p class="fine">Call and Text open on your phone. Email works from a computer or a phone.</p>
<div class="hero-contact-social"><a aria-label="Email Pedro" class="email-pedro" href="mailto:pedro_torres@torrestechremote.com"><img alt="Pedro Torres" height="38" width="38" src="/img/pedro-official-160.webp"/>Email Pedro</a><div aria-label="Social links" class="social-row">{SOCIAL}</div></div>
<p class="fine"><b>Free preview.</b> No payment or credit card required. Just your name, business name, phone and email.</p>
<div class="hero-chips">
<div class="chip">Free setup<small>no setup fee</small></div>
<div class="chip">$10/month<small>or $100/year</small></div>
<div class="chip">Up to 3 free previews<small>pay only if you approve</small></div>
</div>
<p class="langs-line"><b>Español:</b> <span lang="es">Su tarjeta de presentación en el teléfono de sus clientes. Instalación gratis, vista previa gratis.</span><br/><b>Português:</b> <span lang="pt-BR">Seu cartão de visita no celular dos seus clientes. Criação grátis, prévia grátis.</span></p>
</div>
<div class="stage"><div class="showcase-head"><span class="showcase-dot"></span> YOUR CARD, YOUR BRAND</div>
<div class="showcase-cards">
<a class="showcase-card sc-left" href="https://cards.torrestechremote.com/alpha-fit-club-newark/" rel="noopener" target="_blank" aria-label="Open the Alpha Fit Club card"><img alt="Alpha Fit Club digital card" height="2047" width="469" fetchpriority="high" src="/img/home/hero-alpha.webp"/></a>
<a class="showcase-card sc-center" href="https://cards.torrestechremote.com/torres-tech-remote/" rel="noopener" target="_blank" aria-label="Open the Torres Tech Remote card"><img alt="Torres Tech Remote's own digital business card" height="1688" width="780" fetchpriority="high" src="/img/business-card-ttr-day.webp"/></a>
<a class="showcase-card sc-right" href="https://cards.torrestechremote.com/keon-torres/" rel="noopener" target="_blank" aria-label="Open the Keon Torres card"><img alt="Keon Torres digital card" height="2048" width="671" fetchpriority="high" src="/img/home/hero-keon.webp"/></a>
</div>
<div class="showcase-caption">Real cards</div></div>
</div></header>
<div class="strip"><div class="wrap">
<b>Free setup <span class="dot">•</span> $10/month or $100/year <span class="dot">•</span> Up to 3 free previews</b>
<small>In-person service in the Ironbound, Newark NJ · <a href="https://www.facebook.com/profile.php?id=61595452617390" rel="noopener" target="_blank"><u>Now on Facebook</u></a></small>
</div></div>

<section id="card"><div class="wrap center reveal">
<div class="eyebrow">What's on your card</div>
<h2>Everything a customer needs, one tap away.</h2>
<p class="sub">Tap any card above to try the real thing.</p>
<div class="grid3 grid4">
<div class="fc"><div class="feature-photo"><img alt="Alpha Fit Club brand shown on the card" loading="lazy" height="700" width="840" src="/img/home/feat-brand.webp"/></div><h3>Your brand</h3><p>Your logo and brand colors.</p></div>
<div class="fc"><div class="feature-photo"><img alt="One-tap buttons on a digital card" loading="lazy" height="580" width="840" src="/img/home/feat-buttons.webp"/></div><h3>One-tap buttons</h3><p>Call, text, WhatsApp, email, directions and website buttons.</p></div>
<div class="fc"><div class="feature-photo"><img alt="Business hours and service pricing on a card" loading="lazy" height="1500" width="840" src="/img/home/feat-details.webp"/></div><h3>Your business details</h3><p>Hours, services and prices, photos, payment links.</p></div>
<div class="fc"><div class="feature-photo"><img alt="Photo gallery on the Alpha Fit Club card" loading="lazy" height="690" width="780" src="/img/home/feat-photos.webp"/></div><h3>Your photos</h3><p>Show your place, your work or your team in a photo gallery customers can swipe.</p></div>
<div class="fc"><div class="feature-photo feature-photo-fit"><img alt="Torres Tech Remote card with Facebook, Instagram, YouTube, video and Leave a review buttons" loading="lazy" height="610" width="780" src="/img/home/feat-socials.webp"/></div><h3>Your socials and reviews</h3><p>Facebook, Instagram, YouTube, your videos, your website and a Leave a review button, so customers can follow you.</p></div>
<div class="fc"><div class="feature-photo"><img alt="English and Spanish versions of the Alpha Fit Club card" loading="lazy" height="1180" width="1720" src="/img/home/feat-languages.webp"/></div><h3>Opens in their language</h3><p>Their phone is set to Spanish? They see Spanish, and can tap to switch to your other languages. You pick up to 3 of 25.</p></div>
<div class="fc"><div class="feature-photo feature-photo-double"><img alt="Alpha Fit Club November events promotion on the card" loading="lazy" height="1100" width="840" src="/img/home/feat-offer-events.webp"/><img alt="Alpha Fit Club promotional poster on the card" loading="lazy" height="1160" width="840" src="/img/home/feat-offer-poster.webp"/></div><h3>A spot for your offer</h3><p>Having a sale? Email me and I change it for you. It can turn itself off when your offer ends.</p></div>
<div class="fc"><div class="feature-photo"><img alt="A digital business card QR code" loading="lazy" height="710" width="840" src="/img/home/feat-share.webp"/></div><h3>Easy to share, and it lasts</h3><p>QR code, Share and Save contact. Your QR code never changes, so printed codes keep working.</p></div>
</div>
{phone}
</div></section>

<section class="soft" id="clients"><div class="wrap center reveal">
<div class="eyebrow">Real cards</div>
<h2>Featured clients.</h2>
<p class="sub">These are screenshots. On the real card, every button works when you tap it.</p>
<div class="clients">
<div class="client">
<h3>Alpha Fit Club</h3>
<p>Newark, NJ location</p>
{alpha}
<p class="langnote">English and Spanish on one card.</p>
<ul class="chips"><li><b>Book first class</b> opens booking page</li><li><b>Call</b> rings the gym</li><li><b>Text</b> starts a text</li><li><b>Email</b> writes to the gym</li><li><b>Directions</b> opens the map</li><li><b>EN / ES</b> switches language</li><li><b>Day / Night</b> switches the look</li><li><b>Share</b> send the card</li><li><b>Save contact</b> adds to phone</li><li><b>QR code</b> scan to open</li></ul>
</div>
<div class="client">
<h3>Keon Torres</h3>
<p>English &amp; Acting Coach / Instructor<br/>Vietnam &amp; Japan</p>
{keon}
<p class="langnote">Three languages on one card: English, Japanese and Vietnamese.</p>
<ul class="chips"><li><b>Message on LINE</b> opens a chat</li><li><b>Email</b> writes to him</li><li><b>EN / JA / VI</b> switches language</li><li><b>Day / Night</b> switches the look</li><li><b>Share</b> send the card</li><li><b>Save contact</b> adds to phone</li><li><b>QR code</b> scan to open</li><li><b>Add to home screen</b> installs like an app</li></ul>
</div>
</div>
<figure class="review"><div class="stars" aria-label="5 out of 5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><blockquote>&ldquo;Great product. Great service. Best digital business card out there! I&rsquo;ve had several and this is the most interactive I&rsquo;ve had. Pete&rsquo;s very accommodating and works with you on all the details till it&rsquo;s just right. So happy to do business with Torres Tech Remote!&rdquo;</blockquote><figcaption>Miriam Ramos, Alpha Fit Club &middot; Google review, 5.0</figcaption></figure>
</div></section>

<section id="how"><div class="wrap center reveal">
<div class="eyebrow">How it works</div>
<h2>See it before you pay.</h2>
<div class="steps">
<div class="step"><div class="step-phone"><img alt="Free preview form with required name and business name fields" decoding="async" loading="lazy" height="1170" width="840" src="/img/home/step-1-form.webp"/></div><span aria-label="Step 1" class="step-num">1</span><h3>Fill out our Free Preview form</h3><p>Only your name, business name, phone, email and a confirmation checkbox are required. All other questions are optional.</p></div>
<div class="step"><div class="step-phone"><img alt="A watermarked digital business card preview for Navalha Barber Co." decoding="async" loading="lazy" height="1796" width="840" src="/img/home/step-2-preview.webp"/></div><span aria-label="Step 2" class="step-num">2</span><h3>Get your free preview</h3><p>We create your free digital business card preview from the information you give us and email it to you for review. You can receive up to 3 free previews. You only pay if you approve your card.</p></div>
<div class="step"><div class="step-phone"><img alt="The live Navalha Barber Co. digital card with contact buttons and hours" decoding="async" loading="lazy" height="1700" width="840" src="/img/home/step-3-live.webp"/></div><span aria-label="Step 3" class="step-num">3</span><h3>Pay when you're happy</h3><p>You only pay when you’re happy with it. Then your card goes live with its own link and QR code.</p></div>
</div>
</div></section>

<section class="soft" id="languages"><div class="wrap lang-grid reveal">
<div>
<div class="eyebrow">Languages</div>
<h2>Up to 3 of 25 languages.</h2>
<p class="sub">Pick up to 3 languages for your card, like Spanish, Portuguese, Chinese, Japanese and Arabic. Customers switch between them on the card.</p>
</div>
<div class="lang-list">{lang_html}</div>
</div></section>

<section id="meet"><div class="wrap reveal"><div class="pedro-panel"><img alt="Pedro Torres, founder of Torres Tech Remote" class="pedro-portrait" height="336" width="336" loading="lazy" src="/img/pedro-official-336.webp"/><div>
<div class="eyebrow">Who makes your card</div>
<h2>Hi, I’m Pedro.</h2>
<p>I run Torres Tech Remote from the Ironbound, Newark. I make every card myself, and in the Ironbound I can come by your shop to set it up with you.</p>
<p>Send me your business name and I’ll make you a free preview and send you a link to review. You only pay if you like it.</p>
<div class="cta"><a class="btn btn-p" href="{PREVIEW}" rel="noopener nofollow" target="_blank">Fill in the form →</a><a class="btn btn-s" href="mailto:pedro_torres@torrestechremote.com">Email Pedro</a></div>
<div class="cred"><img src="/comptia-a-certification.7.png" alt="CompTIA A+ Certified" width="52" height="52" loading="lazy"/><div><b>CompTIA A+ Certified</b><span>Certified IT technician. I set up and look after your card myself.</span></div></div>
</div></div></div></section>

<section class="soft" id="pricing"><div class="wrap center reveal">
<div class="eyebrow">Pricing</div>
<h2>Free setup. Just a small monthly fee.</h2>
<div class="price">
<div class="pc">
<div class="tag">Design &amp; setup</div>
<div class="big">Free</div><div class="note">No setup fee.</div>
<ul class="ticks"><li>Your logo and brand colors</li><li>Call, text, WhatsApp, email, directions and website buttons</li><li>Hours, services and prices, photos, payment links</li><li>QR code, Share and Save contact</li><li>Up to 3 of 25 languages</li><li>Installs like an app on iPhone and Android, no app store</li><li><b>Up to 3 free previews before you pay</b></li></ul>
</div>
<div class="pc hi">
<div class="tag">Hosting &amp; updates</div>
<div class="big">$10<small> /month</small></div><div class="note">or <b>$100 per year</b>, 2 months free</div>
<ul class="ticks"><li>Hosting and security updates</li><li>Unlimited changes to your hours, prices, photos and links</li><li>Your QR code never changes, so printed codes keep working</li></ul>
<a class="btn btn-p" href="{PREVIEW}" rel="noopener nofollow" target="_blank">Get my free preview →</a>
</div>
</div>
<details class="order" id="order">
<summary>Already approved your preview? Pay here</summary>
<div class="order-body">
<p id="order-intro">Enter the unlock code we sent you with your preview. Use the same name, business name and phone you gave us. No preview yet? <a href="mailto:pedro_torres@torrestechremote.com">Ask for one first</a>, it’s free.</p>
<form class="order-unlock" id="order-unlock">
<label for="order-code">Unlock code</label>
<div class="unlock-row">
<input autocapitalize="characters" autocomplete="off" id="order-code" name="code" placeholder="From your preview" required="" spellcheck="false" type="text"/>
<button class="btn btn-p" type="submit">Unlock</button>
</div>
<p aria-live="polite" class="order-msg" id="order-msg" role="status"></p>
</form>
<noscript><p>No code box? <a href="mailto:pedro_torres@torrestechremote.com">Email us</a> for your payment link.</p></noscript>
<p class="order-msg ok" hidden="" id="order-ready">Your preview is ready to go live. At checkout, use the same name, business name and phone you gave us. Pick a plan:</p>
<div hidden="" id="order-pay">
<a class="btn btn-p" id="order-monthly" rel="noopener" target="_blank">Make it live: $10/month</a>
<a class="btn btn-p" id="order-yearly" rel="noopener" target="_blank">Make it live: $100/year</a>
</div>
<p class="fine">Card accepted online and in person. Cash in person for yearly plans. In-person service in the Ironbound, Newark NJ; online orders available in the US and its territories, and to US citizens abroad paying with a US card or bank account. See the <a href="/tos.html">Terms</a>.</p>
</div>
</details>
</div></section>

<section id="teams"><div class="wrap center reveal">
<div class="eyebrow">For businesses</div>
<h2>Multiple locations or employees?</h2>
<p class="sub">Select the option that fits your organization, or combine them. Each business is different, so we provide a custom quote based on your number of locations and employees. Setup is free. The business pays for all the cards.</p>
<p class="talk" style="margin-top:14px">Run a gym or fitness studio? <a href="/digital-business-card-for-gyms/">See the digital business card for gyms</a>.</p>
<div class="tcards">
<div class="tcard"><p class="label">Option 1</p><h3>Multiple locations</h3><p>A single card lists every location, each with its own address, directions, phone number and hours. Suited to retail, fitness and multi-site businesses.</p>
<a class="btn btn-s" href="https://cards.torrestechremote.com/corner-table-cafe/" rel="noopener" target="_blank">See an example: Corner Table Café</a>
<a class="btn btn-p" href="{QUOTE_FORM}" rel="noopener nofollow" target="_blank">Request a quote: multiple locations</a></div>
<div class="tcard"><p class="label">Option 2</p><h3>Single location, multiple employees</h3><p>Each employee receives an individual card with their name, photo and contact details. One office card lists the entire team.</p>
<a class="btn btn-s" href="https://cards.torrestechremote.com/harbor-realty/" rel="noopener" target="_blank">See an example: Harbor Realty</a>
<a class="btn btn-p" href="{QUOTE_FORM}" rel="noopener nofollow" target="_blank">Request a quote: multiple employees</a></div>
<div class="tcard"><p class="label">Option 3</p><h3>Multiple locations and employees</h3><p>Multiple locations with individual employee cards. Each employee can be assigned to the location where they work.</p>
<a class="btn btn-s" href="https://cards.torrestechremote.com/brightside-dental/" rel="noopener" target="_blank">See an example: Brightside Dental</a>
<a class="btn btn-p" href="{QUOTE_FORM}" rel="noopener nofollow" target="_blank">Request a quote: both</a></div>
</div>
<p class="talk">Prefer to talk? Call <a href="tel:+12017722106">(201) 772-2106</a> or email <a href="mailto:pedro_torres@torrestechremote.com">pedro_torres@torrestechremote.com</a>.</p>
</div></section>

<section class="soft" id="faq"><div class="wrap center reveal">
<div class="eyebrow">FAQ</div>
<h2>Common questions.</h2>
<div class="faq">{faq_html}</div>
</div></section>

<section><div class="wrap reveal">
<div class="cta-band">
<h2>See your card before you pay.</h2>
<p>Call, email or fill in a short form, and we’ll make you a free preview. Up to 3 free previews. You only pay when you’re happy with it.</p>
<div class="cta">
<a class="btn btn-p" href="{PREVIEW}" rel="noopener nofollow" target="_blank">Request your free preview →</a>
<a class="btn btn-s" href="tel:+12017722106">Call (201) 772-2106</a>
<a class="btn btn-s" href="{SMS}">Text Pedro</a>
<a class="btn btn-s" href="{MAILTO}">Or email us</a>
</div>
<p class="fine">Call and Text open on your phone. Email works from a computer or a phone.</p>
<p class="fine">Free preview. No payment or credit card required. Just your name, business name, phone and email to get started.</p>
<p class="fine">See it live: <a href="https://cards.torrestechremote.com/navalha-barber-co/" rel="noopener" target="_blank">demo card</a> · <a href="https://cards.torrestechremote.com/torres-tech-remote/" rel="noopener" target="_blank">our own card</a></p>
</div>
</div></section>
</main>
<footer><div class="wrap">
<div class="foot">
<div><a class="brand" href="/"><img alt="TTR" src="/img/ttr-monogram.webp" width="61" height="40"/> Torres Tech Remote</a><p>Digital Business Cards · Ironbound, Newark, NJ</p><div class="footer-social"><div aria-label="Torres Tech Remote social links" class="social-row">{SOCIAL}</div></div></div>
<div><h3>Torres Tech Remote</h3><a href="/">Home</a><a href="/digital-business-card-for-gyms/">Cards for gyms</a><a href="mailto:pedro_torres@torrestechremote.com">Contact</a><a href="/tos.html">Terms</a><a href="/privacy.html">Privacy</a></div>
<div><h3>Languages</h3><a href="/" aria-current="page">English</a><a hreflang="es" lang="es" href="/es/">Español</a><a hreflang="pt-PT" lang="pt-PT" href="/pt/">Português</a></div>
</div>
<div class="copy"><span>© 2026 Torres Tech Remote</span><span>Newark, NJ</span></div>
</div></footer>
<script src="/home.js"></script>
<script>
  {locks}
{unlock}
</script>
<!-- Cloudflare Web Analytics --><script data-cf-beacon='{{"token": "c60da00970ce404fbd115d07cfea6c99"}}' src="https://static.cloudflareinsights.com/beacon.min.js" type="module"></script><!-- End Cloudflare Web Analytics -->
</body>
</html>
'''

if "--stdout" in sys.argv:
    sys.stdout.write(HEAD + BODY)
    sys.exit(0)
live = "--live" in sys.argv
out = root / ("index.html" if live else "index-new.html")
out.write_text(HEAD + BODY, encoding="utf-8")
print("wrote", out, out.stat().st_size, "bytes")
