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


if __name__ == "__main__":
    main()
