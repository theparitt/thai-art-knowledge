"""Find and download freely licensed reference photos from Wikimedia Commons, with attribution metadata.

  python3 commons.py search <topic> "<query>" [n]      -> research/candidates/<topic>/NN.jpg + meta.json + sheet.jpg
  python3 commons.py cat <topic> "Category:..." [n]
  python3 commons.py pick <topic> <NN> <name> "<caption th>"   -> images/photos/<name>.jpg + entry in images/photos/manifest.json

Only free licences are kept (CC0, public domain, CC BY, CC BY-SA). Every published photo keeps author, licence and source URL.
"""
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
CAND = ROOT / "research" / "candidates"
PHOTOS = ROOT / "images" / "photos"
API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "thai-art-knowledge/1.0 (https://thai-art-knowledge.pages.dev; research use)"}
FREE = re.compile(r"^(CC0|Public domain|PD|CC BY(-SA)? \d|CC BY(-SA)?$|Attribution|GFDL)", re.I)


def get(params):
    url = API + "?" + urllib.parse.urlencode({**params, "format": "json"})
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.load(r)


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def query(params, n):
    p = {"action": "query", "prop": "imageinfo", "iiprop": "url|size|extmetadata|mime", "iiurlwidth": 1024, **params}
    pages = get(p).get("query", {}).get("pages", {})
    out = []
    for pg in sorted(pages.values(), key=lambda q: q.get("index", 0)):
        ii = (pg.get("imageinfo") or [{}])[0]
        m = ii.get("extmetadata", {})
        lic = strip(m.get("LicenseShortName", {}).get("value"))
        if not ii or ii.get("mime") not in ("image/jpeg", "image/png") or not FREE.match(lic or ""):
            continue
        if ii.get("width", 0) < 600:
            continue
        out.append(dict(title=pg["title"], thumb=ii.get("thumburl"), page=ii.get("descriptionurl"), license=lic,
                        license_url=strip(m.get("LicenseUrl", {}).get("value")), artist=strip(m.get("Artist", {}).get("value")),
                        credit=strip(m.get("Credit", {}).get("value"))[:200],
                        desc=strip(m.get("ImageDescription", {}).get("value"))[:400], width=ii["width"], height=ii["height"]))
        if len(out) >= n:
            break
    return out


def fetch(topic, items):
    d = CAND / topic
    d.mkdir(parents=True, exist_ok=True)
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8")) if (d / "meta.json").exists() else []
    seen = {m["title"] for m in meta}
    for it in items:
        if it["title"] in seen:
            continue
        k = len(meta)
        path = d / f"{k:02d}.jpg"
        try:
            with urllib.request.urlopen(urllib.request.Request(it["thumb"], headers=UA), timeout=90) as r:
                path.write_bytes(r.read())
            im = Image.open(path).convert("RGB")
            im.save(path, quality=88)
        except Exception as e:  # noqa
            print("skip", it["title"], e)
            continue
        it["file"] = path.name
        meta.append(it)
        seen.add(it["title"])
    (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    sheet(topic, meta)
    for i, m in enumerate(meta):
        print(f"{i:02d} {m['title'][5:80]} | {m['license']} | {m['desc'][:90]}")


def sheet(topic, meta):
    d = CAND / topic
    tw, th = 330, 260
    cols = 4
    rows = (len(meta) + cols - 1) // cols
    sh = Image.new("RGB", (cols * tw, rows * (th + 22)), "white")
    dr = ImageDraw.Draw(sh)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except OSError:
        font = None
    for i, m in enumerate(meta):
        im = Image.open(d / m["file"])
        im.thumbnail((tw - 6, th - 6))
        x, y = (i % cols) * tw, (i // cols) * (th + 22)
        sh.paste(im, (x + 3, y + 22))
        dr.text((x + 4, y + 1), f"{i:02d}", fill="red", font=font)
    sh.save(d / "sheet.jpg", quality=80)


def pick(topic, idx, name, caption):
    meta = json.loads((CAND / topic / "meta.json").read_text(encoding="utf-8"))
    m = meta[int(idx)]
    PHOTOS.mkdir(parents=True, exist_ok=True)
    im = Image.open(CAND / topic / m["file"])
    im.thumbnail((1400, 1400))
    im.save(PHOTOS / f"{name}.jpg", quality=86)
    man_p = PHOTOS / "manifest.json"
    man = json.loads(man_p.read_text(encoding="utf-8")) if man_p.exists() else {}
    man[name] = dict(file=f"images/photos/{name}.jpg", caption=caption, title=m["title"], source=m["page"], author=m["artist"],
                     license=m["license"], license_url=m["license_url"], description=m["desc"])
    man_p.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print("picked", name, "<-", m["title"], m["license"])


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "search":
        n = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        fetch(sys.argv[2], query({"generator": "search", "gsrsearch": sys.argv[3], "gsrnamespace": 6, "gsrlimit": 40}, n))
    elif cmd == "cat":
        n = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        fetch(sys.argv[2], query({"generator": "categorymembers", "gcmtitle": sys.argv[3], "gcmtype": "file", "gcmlimit": 60}, n))
    elif cmd == "pick":
        pick(*sys.argv[2:6])
