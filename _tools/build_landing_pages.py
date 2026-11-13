"""Build niche + language landing pages for the digital business cards.

Run from the website folder:  python3 _tools/build_landing_pages.py

Inputs (all under _tools/seo/):
  niches/<niche>.json   one file per niche; "pages" holds one entry per language
  copy/<lang>.json      wording shared by every page in that language
  landing.html          the one page template

Output: <path>/index.html for every page, e.g. es/tarjeta-limpieza/index.html,
and the matching <url> entries in sitemap.xml (added once, never duplicated).

Every claim (price, free setup, free preview, languages) must match
digital-business-cards.html. Check that page before changing one here.
Write each language by hand; do not machine-translate pages.
"""
import glob
import html
import json
import os
import re
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEO = os.path.join(ROOT, "_tools", "seo")
SITE = "https://torrestechremote.com"
# Same quote form as the "Request a quote" link on digital-business-cards.html
QUOTE_URL = "https://docs.google.com/forms/d/e/1FAIpQLSenglfDQ0WaNQpeYR2ZBD-Y4AP6W5HduUZSNqFPebuN1tnx-Q/viewform"


def esc(s):
    return html.escape(s, quote=True)


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def render(tpl, values):
    out = tpl
    for k, v in values.items():
        out = out.replace("{{" + k + "}}", v)
    left = re.findall(r"\{\{(\w+)\}\}", out)
    if left:
        raise SystemExit(f"Template placeholders not filled: {sorted(set(left))}")
    return out


def example_html(ex):
    if not ex:
        return ""
    return ('<section><div class="wrap ex">'
            f'<img src="/{esc(ex["image"])}" alt="{esc(ex["alt"])}" loading="lazy" width="200"/>'
            f'<p>{esc(ex["caption"])}</p></div></section>')


def phone_html(copy):
    groups = "".join(
        f"<div><h3>{esc(h)}</h3>" + "".join(f"<p><b>{esc(os_)}.</b> {esc(t)}</p>" for os_, t in steps) + "</div>"
        for h, steps in copy["phone_groups"])
    return (f'<section><div class="wrap"><h2>{esc(copy["phone_title"])}</h2>'
            f'<p style="margin-bottom:18px">{esc(copy["phone_lead"])}</p><div class="ph">{groups}</div>'
            f'<p class="help">{esc(copy["phone_help"])}</p></div></section>')


def options_html(copy):
    out = []
    for title, price, desc, cta, link in copy["price_options"]:
        quote = link == "QUOTE"
        href = QUOTE_URL if quote else link
        extra = ' target="_blank" rel="noopener nofollow"' if quote else ""
        out.append(f'<div class="opt"><h3>{esc(title)}</h3><p class="pr">{esc(price)}</p>'
                   f'<p>{esc(desc)}</p><a class="btn" href="{esc(href)}"{extra}>{esc(cta)}</a></div>')
    return "".join(out)


def problem_html(pr):
    if not pr:
        return ""
    paras = "".join(f"<p>{esc(x)}</p>" for x in pr["text"])
    return f'<section><div class="wrap prob"><h2>{esc(pr["title"])}</h2>{paras}</div></section>'


def hreflang(pages):
    """Link every language version of a niche to the others (only if there are 2+)."""
    if len(pages) < 2:
        return ""
    tags = [f'<link rel="alternate" hreflang="{l}" href="{SITE}/{p["path"]}/"/>' for l, p in pages.items()]
    first = next(iter(pages.values()))
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}/{first["path"]}/"/>')
    return "\n".join(tags)


def build_page(niche, lang, page, copy, alternates=""):
    url = f"{SITE}/{page['path']}/"
    faq = page["faq"]
    faq_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq
        ],
    }, ensure_ascii=False)
    faq_json = faq_json.replace("</", "<\\/")
    values = {
        "lang": lang,
        "url": url,
        "alternates": alternates,
        "problem_html": problem_html(page.get("problem")),
        "cta_url": esc(copy["cta_url"]),
        "sms_url": copy["sms_url"],
        "sms_label": esc(copy["sms_label"]),
        "sms_hint": esc(copy["sms_hint"]),
        "options_html": options_html(copy),
        "price_note": esc(copy["price_note"]),
        "phone_html": phone_html(copy),
        "example_html": example_html(page.get("example")),
        "faq_json": faq_json,
        "year": str(datetime.date.today().year),
        "buttons_html": "".join(
            f"<div><b>{esc(t)}</b> <span>{esc(d)}</span></div>" for t, d in page["buttons"]),
        "steps_html": "".join(
            f"<li><b>{esc(t)}</b>{esc(d)}</li>" for t, d in copy["steps"]),
        "uses_html": "".join(f"<li>{esc(x)}</li>" for x in page["uses"]),
        "why_html": "".join(f"<li>{esc(x)}</li>" for x in page["why"]),
        "price_html": "".join(f"<li>{esc(x)}</li>" for x in copy["price_lines"]),
        "faq_html": "".join(
            f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq),
    }
    for k in ("title", "description", "eyebrow", "h1", "lede", "uses_title", "why_title"):
        values[k] = esc(page[k])
    for k in ("nav_cta", "cta_primary", "cta_note", "how_title", "buttons_title",
              "buttons_lead", "price_title", "not_title",
              "faq_title", "final_title", "footer_privacy", "footer_terms", "footer_rights"):
        values[k] = esc(copy[k])
    # A page may override the shared "what it isn't" text.
    values["not_text"] = esc(page.get("not_text", copy["not_text"]))
    with open(os.path.join(SEO, "landing.html"), encoding="utf-8") as f:
        tpl = f.read()
    return url, render(tpl, values)


NEW_PARTS = {"en": ("index-new.html", "/"), "es": ("es/index-new.html", "/es/"), "pt-PT": ("pt/index-new.html", "/pt/")}


def home_parts(lang, pages):
    """Header and footer of the new home page for this language, with links adjusted for a gym page."""
    src, base = NEW_PARTS[lang]
    h = open(os.path.join(ROOT, src), encoding="utf-8").read()
    nav = re.search(r'<nav class="top">.*?</nav>', h, re.S).group(0)
    foot = re.search(r'<footer>.*?</footer>', h, re.S).group(0)
    nav = re.sub(r'href="#(\w+)"', lambda m: f'href="{base}#{m.group(1)}"', nav)
    code = {"en": "EN", "es": "ES", "pt-PT": "PT"}
    here = f"/{pages[lang]['path']}/"
    # language switch points to the gym page in each language
    nav = re.sub(r'<span class="lang">.*?</span>', '<span class="lang">' + " · ".join(
        (f'<b aria-current="page">{code[l]}</b>' if l == lang else f'<a hreflang="{l}" lang="{l}" href="/{pages[l]["path"]}/">{code[l]}</a>')
        for l in ("en", "es", "pt-PT") if l in pages) + '</span>', nav, flags=re.S)
    names = {"en": "English", "es": "Español", "pt-PT": "Português"}
    foot = re.sub(r'(<h3>[^<]*</h3>)(?:<a [^>]*>(?:English|Español|Português)</a>)+', lambda m: m.group(1) + "".join(
        (f'<a href="/{pages[l]["path"]}/" aria-current="page">{names[l]}</a>' if l == lang else f'<a hreflang="{l}" lang="{l}" href="/{pages[l]["path"]}/">{names[l]}</a>')
        for l in ("en", "es", "pt-PT") if l in pages), foot, count=1)
    return nav, foot


# One real Alpha Fit Club picture per button card, in the order of the card list (same order in every language).
BUTTON_PHOTOS = [
    ("brand", "feat-brand", False), ("booking", "gym-booking", True), ("text or call", "gym-textcall", True),
    ("save", "gym-save", True), ("directions", "gym-directions", True), ("promotion", "gym-promo", False),
    ("truemed", "gym-truemed", False), ("photos", "gym-photos", False), ("review", "gym-review", True), ("hours", "gym-hours", False),
]


PHOTO_LABELS = {
    "en": ["Your brand", "Booking button", "Call and text", "Save contact", "Directions", "Promotions", "HSA/FSA", "Photos", "Follow us", "Hours"],
    "es": ["Su marca", "Botón de reserva", "Llamar y escribir", "Guardar contacto", "Cómo llegar", "Promociones", "HSA/FSA", "Fotos", "Síganos", "Horario"],
    "pt-PT": ["A sua marca", "Botão de reserva", "Ligar e mensagem", "Guardar contacto", "Como chegar", "Promoções", "HSA/FSA", "Fotografias", "Siga-nos", "Horário"],
}


def buttons_with_photos(buttons, lang="en"):
    from PIL import Image
    out = []
    for i, (t, d) in enumerate(buttons):
        alt_, name, fit = BUTTON_PHOTOS[i]
        im = Image.open(os.path.join(ROOT, "img", "home", name + ".webp")).convert("RGB")
        w, h = im.size
        cls = "feature-photo feature-photo-fit" if fit else "feature-photo"
        bg = ' style="background:#%02x%02x%02x"' % im.getpixel((3, 3)) if fit else ""  # match the picture's own background
        out.append(f'<div class="fc"><div class="{cls}"{bg}><span class="pl">{esc(PHOTO_LABELS[lang][i])}</span><img alt="" loading="lazy" height="{h}" width="{w}" src="/img/home/{name}.webp"/></div>'
                   f'<h3>{esc(t)}</h3><p>{esc(d)}</p></div>')
    return "".join(out)


WHERE_LABELS = {
    "en": ["Front desk", "Flyers and posters", "Text messages", "Coaches and trainers"],
    "es": ["Mostrador", "Volantes y carteles", "Mensajes de texto", "Coaches y entrenadores"],
    "pt-PT": ["Balcão", "Folhetos e cartazes", "Mensagens de texto", "Coaches e treinadores"],
}


def uses_with_photos(uses, lang):
    from PIL import Image
    short = {"en": "en", "es": "es", "pt-PT": "pt"}[lang]
    photos = [("gym-where-qr", True), ("gym-where-poster", False), ("gym-where-text-" + short, True), ("gym-where-trainer", False)]
    out = []
    for i, text in enumerate(uses):
        name, fit = photos[i]
        im = Image.open(os.path.join(ROOT, "img", "home", name + ".webp")).convert("RGB")
        w, h = im.size
        cls = "feature-photo feature-photo-fit" if fit else "feature-photo"
        bg = ' style="background:#%02x%02x%02x"' % im.getpixel((3, 3)) if fit else ""
        out.append(f'<div class="fc"><div class="{cls}"{bg}><span class="pl">{esc(WHERE_LABELS[lang][i])}</span><img alt="" loading="lazy" height="{h}" width="{w}" src="/img/home/{name}.webp"/></div>'
                   f'<h3>{esc(text)}</h3></div>')
    return "".join(out)


WHY_TAGS = {
    "en": ["Touch-free", "In the moment", "Always current", "Your team", "Languages", "Set up"],
    "es": ["Sin esfuerzo", "En el momento", "Siempre al día", "Su equipo", "Idiomas", "Puesta en marcha"],
    "pt-PT": ["Sem esforço", "No momento", "Sempre atualizado", "A sua equipa", "Idiomas", "Configuração"],
}


def why_cards(why, lang):
    """One card per reason: first sentence is the title, the rest is the text (no new wording)."""
    out = []
    for i, text in enumerate(why):
        parts = re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÀ¿¡"“])', text.strip(), maxsplit=1)
        body = f"<p>{esc(parts[1])}</p>" if len(parts) > 1 else ""
        out.append(f'<div class="tcard"><p class="label">{esc(WHY_TAGS[lang][i])}</p><h3>{esc(parts[0])}</h3>{body}</div>')
    return "".join(out)


STEP_PHOTOS = ["step-1-form", "gym-step-2-preview", "gym-step-3-live"]


def steps_with_photos(steps):
    from PIL import Image
    out = []
    for i, (title, desc) in enumerate(steps, 1):
        name = STEP_PHOTOS[i - 1]
        w, h = Image.open(os.path.join(ROOT, "img", "home", name + ".webp")).size
        out.append(f'<div class="step"><div class="step-phone"><img alt="{esc(title)}" decoding="async" loading="lazy" height="{h}" width="{w}" src="/img/home/{name}.webp"/></div>'
                   f'<span class="step-num">{i}</span><h3>{esc(title)}</h3><p>{esc(desc)}</p></div>')
    return '<div class="steps">' + "".join(out) + "</div>"


def build_page_new_html(lang, page, copy, pages):
    url = f"{SITE}/{page['path']}/"
    faq = page["faq"]
    faq_json = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}, ensure_ascii=False).replace("</", "<\\/")
    nav, foot = home_parts(lang, pages)
    pr = page.get("problem")
    problem = ""
    if pr:
        problem = ('<section class="gsec soft"><div class="wrap center"><h2>' + esc(pr["title"]) + '</h2><div class="gprob" style="margin-top:22px">'
                   + "".join(f"<p>{esc(x)}</p>" for x in pr["text"]) + '</div></div></section>')
    ex = page.get("example")
    example = ""
    if ex:
        example = ('<section class="gsec soft"><div class="wrap"><div class="gex">'
                   f'<img src="/{esc(ex["image"])}" alt="{esc(ex["alt"])}" loading="lazy" width="230"/><p>{esc(ex["caption"])}</p></div></div></section>')
    # One card per phone (iPhone, Android), each with numbered steps for every task.
    oses = []
    for _, steps in copy["phone_groups"]:
        for o, _t in steps:
            if o not in oses:
                oses.append(o)
    cards = []
    for o in oses:
        parts = []
        for h, steps in copy["phone_groups"]:
            for o2, txt in steps:
                if o2 == o:
                    items = "".join(f"<li>{esc(x)}</li>" for x in re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚ])", txt.strip()))
                    parts.append(f'<h4>{esc(h)}</h4><ol class="gsteps">{items}</ol>')
        cards.append(f'<div class="gcard gphone"><h3>{esc(o)}</h3>{"".join(parts)}</div>')
    phone = (f'<section class="gsec"><div class="wrap center"><h2>{esc(copy["phone_title"])}</h2><p class="sub">{esc(copy["phone_lead"])}</p>'
             f'<div class="gcards gphones">{"".join(cards)}</div><p class="ghelp">{esc(copy["phone_help"])}</p></div></section>')
    opts = []
    for title, price, desc, cta, link in copy["price_options"]:
        quote = link == "QUOTE"
        href = QUOTE_URL if quote else link
        opts.append(f'<div class="gcard"><h3>{esc(title)}</h3><p class="gprice">{esc(price)}</p><p>{esc(desc)}</p>'
                    f'<a class="btn btn-p" href="{esc(href)}" rel="noopener nofollow" target="_blank">{esc(cta)}</a></div>')
    values = {
        "lang": lang, "url": url, "alternates": hreflang(pages), "faq_json": faq_json,
        "nav_html": nav, "footer_html": foot, "problem_html": problem, "example_html": example, "phone_html": phone,
        "soft_buttons": "" if pr else "",
        "cta_url": esc(copy["cta_url"]), "sms_url": copy["sms_url"],
        "buttons_html": buttons_with_photos(page["buttons"], lang),
        "steps_html": steps_with_photos(copy["steps"]),
        "uses_html": uses_with_photos(page["uses"], lang),
        "why_html": why_cards(page["why"], lang),
        "price_html": "".join(f"<li>{esc(x)}</li>" for x in copy["price_lines"]),
        "options_html": "".join(opts),
        "faq_html": "".join(f'<details><summary>{esc(q)}</summary><div class="faq-answer">{esc(a)}</div></details>' for q, a in faq),
        "not_text": esc(page.get("not_text", copy["not_text"])),
    }
    for k in ("title", "description", "eyebrow", "h1", "lede", "uses_title", "why_title"):
        values[k] = esc(page[k])
    for k in ("cta_primary", "cta_note", "how_title", "buttons_title", "buttons_lead", "price_title", "not_title", "faq_title", "final_title",
              "sms_label", "sms_hint", "price_note"):
        values[k] = esc(copy[k])
    tpl = open(os.path.join(SEO, "landing-new.html"), encoding="utf-8").read()
    return render(tpl, values)


def update_sitemap(urls):
    path = os.path.join(ROOT, "sitemap.xml")
    with open(path, encoding="utf-8") as f:
        xml = f.read()
    today = datetime.date.today().isoformat()
    for u in urls:
        if f"<loc>{u}</loc>" in xml:
            continue
        entry = (f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n"
                 f"    <priority>0.7</priority>\n  </url>\n")
        xml = xml.replace("</urlset>", entry + "</urlset>")
    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)


def main_new(live=False):
    """Gym pages in the new look. Preview (default): <path>/index-new.html. --live writes index.html."""
    for npath in sorted(glob.glob(os.path.join(SEO, "niches", "*.json"))):
        niche = load(npath)
        for lang, page in niche["pages"].items():
            copy = load(os.path.join(SEO, "copy", f"{lang}.json"))
            out = build_page_new_html(lang, page, copy, niche["pages"])
            dest = os.path.join(ROOT, page["path"], "index.html" if live else "index-new.html")
            with open(dest, "w", encoding="utf-8") as f:
                f.write(out)
            print("built", dest)


def main():
    built = []
    for npath in sorted(glob.glob(os.path.join(SEO, "niches", "*.json"))):
        niche = load(npath)
        for lang, page in niche["pages"].items():
            copy = load(os.path.join(SEO, "copy", f"{lang}.json"))
            url, out = build_page(niche["niche"], lang, page, copy, hreflang(niche["pages"]))
            dest = os.path.join(ROOT, page["path"], "index.html")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8") as f:
                f.write(out)
            built.append(url)
            print("built", page["path"] + "/index.html")
    update_sitemap(built)


import sys
if __name__ == "__main__":
    if "--new" in sys.argv:
        main_new(live="--live" in sys.argv)
    else:
        main()
