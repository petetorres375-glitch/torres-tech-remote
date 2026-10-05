"""Build the per-tool landing pages from _tools/tool_pages.py.

Run from the website folder:  python3 _tools/build_tool_pages.py

Every fact on these pages must match what the tool does in the Workblox
apps (inputs, outputs, file types, limits, storage). Check the app before
changing a claim. contract-analyzer.html, resume-builder.html and
ats-resume-checker.html are hand-written and not generated here.
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from tool_pages import PAGES  # noqa: E402

SITE = "https://torrestechremote.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APPS = {
    "business": {
        "name": "Workblox Business",
        "theme": "",
        "signup": "https://business.torrestechremote.com/?signup",
        "anchor": "/#business",
        "count": 16,
        "app_id": "#business-app",
        "tiers": [("1&ndash;3 tools", "$25"), ("4&ndash;7 tools", "$40"), ("8&ndash;16 tools", "$75")],
        "from": "$25/mo",
        "pick": "Pick the ones your business runs on and pay for those. Single user, no per-seat pricing.",
    },
    "personal": {
        "name": "Workblox Personal",
        "theme": "theme-personal",
        "signup": "https://workblox.torrestechremote.com/?signup",
        "anchor": "/#personal",
        "count": 7,
        "app_id": "#personal-app",
        "tiers": [("1&ndash;2 tools", "$10"), ("3&ndash;4 tools", "$15"), ("5&ndash;7 tools", "$20")],
        "from": "$10/mo",
        "pick": "Pick the ones you'll use and pay for those.",
    },
}

FINE_PRINT = ("Every plan starts with a 7-day free trial. A card is required to start; cancel before "
              "the trial ends and you won't be charged. Cancel whenever you like from Settings &rarr; "
              "Manage billing &mdash; access runs through the end of your billing period. Available to "
              "customers in the United States and U.S. territories only.")

ANALYTICS = ("<!-- Cloudflare Web Analytics --><script type='module' "
             "src='https://static.cloudflareinsights.com/beacon.min.js' "
             "data-cf-beacon='{\"token\": \"c60da00970ce404fbd115d07cfea6c99\"}'></script>"
             "<!-- End Cloudflare Web Analytics -->")


def attr(s):
    """Plain text for a meta/JSON value; page bodies are written as HTML already."""
    return html.escape(html.unescape(s), quote=True)


def cost_faq(p, app):
    t = app["tiers"]
    return ("What does it cost?",
            f"{p['tool']} is part of {app['name']}. You pick your tools and pay by how many: "
            f"{t[0][1]}/mo for {t[0][0]}, {t[1][1]}/mo for {t[1][0]}, or {t[2][1]}/mo for {t[2][0]}, "
            "with a 7-day free trial.")


def example_html(ex):
    if not ex:
        return ""
    after = ex["after"]
    if isinstance(after, list):
        after = "<ul>" + "".join(f"<li>{x}</li>" for x in after) + "</ul>"
    return f"""
<section class="section section-alt" id="example">
  <div class="container">
    <div class="section-label">Example</div>
    <h2>{ex['heading']}</h2>
    <p class="section-sub">{ex['sub']}</p>
    <div class="ba">
      <div class="ba-box">
        <div class="ex-label" style="margin-top:0;">What you enter</div>
        <p class="ba-quote">{ex['before']}</p>
      </div>
      <div class="ba-box after">
        <div class="ex-label" style="margin-top:0;">What you get</div>
        {f'<div class="ba-job">{ex["after_title"]}</div>' if ex.get("after_title") else ""}
        {after}
      </div>
    </div>
    <p class="example-foot">Example only, shortened. Real results depend on what you enter.</p>
  </div>
</section>
"""


def page_html(p):
    app = APPS[p["app"]]
    url = f"{SITE}/{p['slug']}"
    cards = "\n".join(
        f'      <div class="card{" card-highlight" if i == len(p["outputs"]) - 1 and p.get("highlight_last") else ""}">'
        f"<h3>{h}</h3><p>{d}</p></div>"
        for i, (h, d) in enumerate(p["outputs"]))
    steps = "\n".join(f"      <li><h3>{h}</h3><p>{d}</p></li>" for h, d in p["steps"])
    callout = (f'\n    <div class="callout">\n      <span>&#9432;</span>\n      <span>{p["callout"]}</span>\n    </div>'
               if p.get("callout") else "")
    faqs = p["faqs"] + [cost_faq(p, app)]
    faq_html = "\n".join(
        f'      <details class="faq-item">\n        <summary>{q}</summary>\n'
        f'        <div class="faq-answer">{a}</div>\n      </details>' for q, a in faqs)
    tiers = "\n".join(
        f'      <div class="price"><div class="price-tools">{n}</div><div class="price-amt">{v}<span>/mo</span></div></div>'
        for n, v in app["tiers"])
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{url}#webpage",
                "url": url,
                "name": html.unescape(p["title"]),
                "isPartOf": {"@id": f"{SITE}/#website"},
                "about": {"@id": f"{SITE}/{app['app_id']}"},
                "publisher": {"@id": f"{SITE}/#organization"},
                "breadcrumb": {"@id": f"{url}#breadcrumb"},
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{url}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Workblox", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": html.unescape(p["tool"]), "item": url},
                ],
            },
        ],
    }
    body_class = f' class="{app["theme"]}"' if app["theme"] else ""
    short = "Business" if p["app"] == "business" else "Personal"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<!-- Generated by _tools/build_tool_pages.py from _tools/tool_pages.py. Edit those, not this file. -->
<title>{attr(p['title'])} | Workblox</title>
<meta name="description" content="{attr(p['description'])}"/>
<link rel="canonical" href="{url}"/>
<link rel="icon" type="image/png" sizes="16x16" href="/favicon/favicon-16.png"/>
<link rel="icon" type="image/png" sizes="32x32" href="/favicon/favicon-32.png"/>
<link rel="icon" type="image/png" sizes="192x192" href="/favicon/favicon-192.png"/>
<link rel="shortcut icon" href="/favicon/favicon.ico"/>
<link rel="apple-touch-icon" sizes="180x180" href="/favicon/favicon-180.png"/>
<meta property="og:type" content="website"/>
<meta property="og:url" content="{url}"/>
<meta property="og:title" content="{attr(p['title'])}"/>
<meta property="og:description" content="{attr(p['description'])}"/>
<meta property="og:image" content="{SITE}/og-image.png"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{attr(p['title'])}"/>
<meta name="twitter:description" content="{attr(p['description'])}"/>
<meta name="twitter:image" content="{SITE}/og-image.png"/>
<link rel="stylesheet" href="tool-pages.css"/>
<script type="application/ld+json">
{json.dumps(ld, indent=2, ensure_ascii=False)}
</script>
</head>
<body{body_class}>

<nav>
  <div class="nav-inner">
    <a href="/" class="nav-logo">
      <span class="nav-logo-mark">TTR</span>
      Torres Tech Remote
    </a>
    <ul class="nav-links">
      <li><a href="{app['anchor']}">All {short} tools</a></li>
      <li><a href="/#faq">FAQ</a></li>
      <li><a href="{app['signup']}">Start free trial</a></li>
    </ul>
  </div>
</nav>

<main>

<section class="tool-hero">
  <div class="container">
    <div class="app-pill"><span class="app-pill-dot"></span>{app['name']} &middot; {p['tool']}</div>
    <h1>{p['h1']}</h1>
    <p class="lead">{p['lead']}</p>
    <div class="actions">
      <a href="{app['signup']}" class="btn-primary">Start 7-day free trial</a>
      <a href="{'#example' if p.get('example') else '#how'}" class="btn-secondary">{'See an example' if p.get('example') else 'How it works'}</a>
    </div>
    <p class="hero-note">From {app['from']}. {p['hero_note']} Available in 24 languages.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-label">What you get</div>
    <h2>{p['outputs_heading']}</h2>
    <p class="section-sub">{p['outputs_sub']}</p>
    <div class="grid">
{cards}
    </div>
  </div>
</section>
{example_html(p.get('example'))}
<section class="section" id="how">
  <div class="container">
    <div class="section-label">How it works</div>
    <h2>{p['steps_heading']}</h2>
    <ol class="steps">
{steps}
    </ol>{callout}
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="section-label">Pricing</div>
    <h2>Pay for the tools you pick.</h2>
    <p class="section-sub">{p['tool']} is one of {app['count']} {app['name']} tools. {app['pick']}</p>
    <div class="price-row">
{tiers}
    </div>
    <p class="fine">{FINE_PRINT} <a href="{app['anchor']}">See all {app['count']} {short} tools</a>.</p>
  </div>
</section>

<section class="section">
  <div class="narrow">
    <div class="section-label">FAQ</div>
    <h2>Common questions.</h2>
    <div class="faq">
{faq_html}
    </div>
  </div>
</section>

<section class="cta">
  <h2>{p['cta']}</h2>
  <p>Try {p['tool']} free for 7 days with {app['name']}.</p>
  <div class="actions">
    <a href="{app['signup']}" class="btn-primary">Start 7-day free trial</a>
    <a href="{app['anchor']}" class="btn-secondary">See all {app['count']} {short} tools</a>
  </div>
</section>

</main>

<footer>
  <div class="footer-inner">
    <div class="footer-logo">
      <div class="footer-logo-mark">W</div>
      <div class="footer-brand">
        <div class="footer-logo-name">Workblox</div>
        <div class="footer-logo-sub">by Torres Tech Remote</div>
      </div>
    </div>
    <div class="footer-links">
      <a href="/#personal">Personal</a>
      <a href="/#business">Business</a>
      <a href="/#contact">Support</a>
      <a href="tos.html">Terms</a>
      <a href="privacy.html">Privacy</a>
      <a href="https://www.linkedin.com/in/pedro-torres-8a818241a/" target="_blank" rel="me noopener">LinkedIn</a>
    </div>
    <div class="footer-copy">&copy; 2026 Torres Tech Remote</div>
  </div>
</footer>

{ANALYTICS}
</body>
</html>
"""


def main():
    for p in PAGES:
        with open(os.path.join(ROOT, p["slug"]), "w", encoding="utf-8") as f:
            f.write(page_html(p))
        print("wrote", p["slug"])


if __name__ == "__main__":
    main()
