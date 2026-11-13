#!/usr/bin/env python3
"""Builds the Spanish one-page home (new orange look) from the English build.

  python3 _tools/build_home_es.py          -> writes es/index-new.html (local preview only)
  python3 _tools/build_home_es.py --live   -> writes es/index.html (the real Spanish home page)

How it works: it renders the English page (build_home_en.py, in memory), then swaps every English
piece of text for Spanish. Spanish that Pedro already proofread on the old pages is reused from
the old builders (build_sales_es.py / old home pairs, kept in _tools/es_legacy_pairs.json).
New Spanish is in es_new.py (TRANSLATIONS). Any visible English text left over is printed as a
warning, so nothing slips through untranslated.
"""
import json, pathlib, re, subprocess, sys, urllib.parse, html as htmllib

root = pathlib.Path(__file__).resolve().parent.parent
tools = root / "_tools"
sys.path.insert(0, str(tools))

# 1. English page (rendered in memory by the English builder)
en = subprocess.run([sys.executable, str(tools / "build_home_en.py"), "--stdout"], capture_output=True, text=True, check=True).stdout
s = en

# 2. Spanish already proofread by Pedro on the old pages
legacy = json.loads((tools / "es_legacy_pairs.json").read_text(encoding="utf-8"))
from es_new import TRANSLATIONS, RAW, KEEP  # noqa: E402


def variants(x):
    yield x
    if "&" in x and "&amp;" not in x:
        yield x.replace("&", "&amp;")
    if "'" in x:
        yield x.replace("'", "&#39;")


# raw HTML-level swaps first (longest first so inline links/tags stay intact)
pairs = [(a, b) for a, b in RAW] + [(a, b) for a, b in legacy]
pairs.sort(key=lambda p: -len(p[0]))
for a, b in pairs:
    for v in variants(a):
        if v in s:
            s = s.replace(v, b.replace("&", "&amp;") if v != a and "&amp;" in v else b)
            break

# 3. text-node pass for the rest
TOK = re.compile(r"(<script.*?</script>|<style.*?</style>|<svg.*?</svg>|<!--.*?-->|<[^>]+>)", re.S)
ATTR = re.compile(r'\b(alt|aria-label|title|placeholder)="([^"]*)"')
missing = []
EN_WORDS = set("the and your you to of for with is are on in it up we our from or can each every this that will be at by as an if so do how what who when which where have has not but about all more most one two three free just only any them they their its his her my me i out into than then also may per own off over under here there new now see get make made pick tap open".split())


ES_WORDS = set("el la los las de que su sus con para y un una es en por del al se le les nos tarjeta".split())


def looks_english(k):
    w = re.findall(r"[a-záéíóúñü]+", k.lower())
    if sum(x in ES_WORDS for x in w) >= 2:
        return False
    return any(w in EN_WORDS for w in re.findall(r"[a-z]+", k.lower()))


def tr(text):
    key = htmllib.unescape(text).strip()
    if key in TRANSLATIONS:
        return text.replace(text.strip(), TRANSLATIONS[key].replace("&", "&amp;") if "&amp;" in text else TRANSLATIONS[key])
    return None


def fix_attr(m):
    k = htmllib.unescape(m.group(2)).strip()
    if k in TRANSLATIONS:
        return f'{m.group(1)}="{TRANSLATIONS[k]}"'
    if looks_english(k) and k not in KEEP:
        missing.append(("attr:" + m.group(1), k))
    return m.group(0)


out = []
body_started = False
for tok in TOK.split(s):
    if tok.startswith("<body"):
        body_started = True
    if tok.startswith("<"):
        out.append(ATTR.sub(fix_attr, tok) if body_started else tok)
        continue
    if not body_started or not tok.strip():
        out.append(tok); continue
    r = tr(tok)
    if r is not None:
        out.append(r)
    else:
        k = htmllib.unescape(tok).strip()
        if looks_english(k) and k not in KEEP:
            missing.append(("text", k))
        out.append(tok)
s = "".join(out)

# 4. page-level changes (language, links, head)
from es_new import PAGE  # noqa: E402
s = PAGE(s)

dest = root / ("es/index.html" if "--live" in sys.argv else "es/index-new.html")
dest.write_text(s, encoding="utf-8")
print("wrote", dest, len(s), "bytes")
seen = set()
for kind, t in missing:
    if (kind, t) in seen:
        continue
    seen.add((kind, t))
    print("EN?", kind, "|", t)
print(len(seen), "leftover items")
