#!/usr/bin/env python3
"""Terms (tos.html) and Privacy (privacy.html) in the new orange look: new header, footer and colors.
The wording is never touched: the text between <div class="page"> and the footer is copied as it is.

  python3 _tools/build_legal.py          -> tos-new.html and privacy-new.html (local preview)
  python3 _tools/build_legal.py --live   -> overwrites tos.html and privacy.html

Needs index-new.html (the new English home page) for the header and footer, so build that first.
Safe to re-run after going live: it reads the wording from whichever file holds it.
"""
import pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
live = "--live" in sys.argv
home = (root / "index-new.html").read_text(encoding="utf-8")
nav = re.search(r'<nav class="top">.*?</nav>', home, re.S).group(0)
nav = re.sub(r'href="#(\w+)"', r'href="/#\1"', nav)
footer = re.search(r"<footer>.*?</footer>", home, re.S).group(0)
# language links in the footer: this page is English only, so no page is "current"
footer = footer.replace(' aria-current="page"', "")

CSS = """
.legal{max-width:800px;margin:0 auto;padding:64px 24px 90px}
.legal .doc-eyebrow{font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--orange-text);margin-bottom:12px}
.legal h1{font-size:clamp(32px,5vw,46px);margin-bottom:10px}
.legal .doc-meta{font-size:14px;color:var(--muted);margin-bottom:34px}
.legal .notice{background:var(--peach);border:1px solid #f0d3bd;border-radius:16px;padding:18px 22px;margin-bottom:38px;font-size:15px;color:var(--ink);line-height:1.7}
.legal section{padding:0;margin-bottom:30px;border:0}
.legal .section-header{display:flex;align-items:baseline;gap:12px;margin-bottom:10px}
.legal .section-num{background:var(--orange);color:#fff;font-size:12px;font-weight:800;border-radius:999px;padding:3px 11px;white-space:nowrap}
.legal h2{font-size:19px;margin:0;letter-spacing:-.01em}
.legal p{color:var(--muted);font-size:15.5px;line-height:1.8;margin:0 0 12px}
.legal p strong,.legal li strong{color:var(--ink)}
.legal ul{margin:8px 0 12px 22px;color:var(--muted);display:flex;flex-direction:column;gap:7px;font-size:15.5px;line-height:1.75}
.legal a{color:var(--orange-text);text-decoration:underline}
.legal .caps{font-size:13.5px;line-height:1.75;color:var(--muted);border:1px solid var(--line);border-radius:14px;padding:16px 20px;background:#f8f9fc}
.legal a[style]{color:var(--orange-text)!important}
.legal hr{border:0;border-top:1px solid var(--line);margin:44px 0}
@media(max-width:600px){.legal{padding:40px 18px 64px}}
"""

for name, title in (("tos", "Terms of Service"), ("privacy", "Privacy Policy")):
    src = root / f"{name}.html"
    s = src.read_text(encoding="utf-8")
    m = re.search(r'<div class="page[^"]*">(.*?)\n</div>\n(?:\n<footer|</main>)', s, re.S)
    assert m, f"{name}: page wording not found"
    body = m.group(1)
    desc = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
    ttl = re.search(r"<title>(.*?)</title>", s).group(1)
    out = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{ttl}</title>
<meta name="description" content="{desc}"/>
<link rel="canonical" href="https://torrestechremote.com/{name}.html"/>
<link rel="icon" type="image/png" sizes="16x16" href="/favicon/ttr-16.png"/>
<link rel="icon" type="image/png" sizes="32x32" href="/favicon/ttr-32.png"/>
<link rel="icon" type="image/png" sizes="192x192" href="/favicon/ttr-192.png"/>
<link rel="shortcut icon" href="/favicon/ttr.ico"/>
<link rel="apple-touch-icon" sizes="180x180" href="/favicon/ttr-180.png"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin=""/>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap"/>
<link rel="stylesheet" href="/home.css"/>
<style>{CSS}</style>
</head>
<body id="top">
{nav}
<main>
<div class="page legal">{body}
</div>
</main>
{footer}
<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "c60da00970ce404fbd115d07cfea6c99"}}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>
'''
    dest = root / (f"{name}.html" if live else f"{name}-new.html")
    dest.write_text(out, encoding="utf-8")
    print("wrote", dest.name, len(out), "bytes")
