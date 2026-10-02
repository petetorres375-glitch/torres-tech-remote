"""Tell Bing (and the other IndexNow search engines) which pages changed.

    python3 _tools/indexnow.py contract-analyzer.html index.html
    python3 _tools/indexnow.py --all          # every page in sitemap.xml

The GitHub workflow .github/workflows/indexnow.yml runs this after every
push with the .html files that changed, so new and edited pages are picked
up without resubmitting the sitemap by hand. The key is public by design:
it proves the site is ours because only we can put the matching .txt file
at the site root.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
import xml.dom.minidom

HOST = "torrestechremote.com"
SITE = f"https://{HOST}"
KEY = "b25a70137286c7231481e8a50c8307ad"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def page_url(path):
    path = path.lstrip("./")
    return f"{SITE}/" if path == "index.html" else f"{SITE}/{path}"


def sitemap_urls():
    doc = xml.dom.minidom.parse(os.path.join(ROOT, "sitemap.xml"))
    return [n.firstChild.data.strip() for n in doc.getElementsByTagName("loc")]


def wait_until_live(url, timeout=300):
    """GitHub Pages publishes a minute or so after the push; don't ping Bing
    about a page it would still see as missing."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{url}?indexnow={int(time.time())}", timeout=20) as r:
                if r.status == 200:
                    return True
        except urllib.error.URLError:
            pass
        time.sleep(15)
    return False


def submit(urls):
    body = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": f"{SITE}/{KEY}.txt",
        "urlList": urls,
    }).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


def main(args):
    if args == ["--all"]:
        urls = sitemap_urls()
    else:
        urls = [page_url(a) for a in args if a.endswith(".html") and not a.startswith("_")]
    if not urls:
        print("No pages to submit.")
        return 0
    if not wait_until_live(f"{SITE}/{KEY}.txt"):
        print("Key file is not live yet; not submitting.")
        return 1
    for u in urls:
        if not wait_until_live(u, timeout=120):
            print(f"warning: {u} is not answering 200 (deleted pages are still reported)")
    status = submit(urls)
    print(f"IndexNow answered {status} for {len(urls)} URL(s)")
    # 200 = accepted, 202 = accepted and the key is still being checked.
    return 0 if status in (200, 202) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
