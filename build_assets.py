"""
Rebuild assets (v2) using the freshly fetched _raw HTML.

Fixes:
  * artist portraits  -> matched to names by vertical (top) document order
  * studio interiors  -> the real IMG_648x.JPG photos from the studio record
  * gallery categories -> only the categories that have real source galleries
                          (realism, graphic, mini, overlapping, piercing)

Run after _refetch.py.  Writes static/img/index.json.
"""
import json, os, re, shutil, time
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, "_raw")
OUT = os.path.join(ROOT, "static", "img")
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124 Safari/537.36"}

de = open(os.path.join(RAW, "page_de.html"), encoding="utf-8").read()

# popup id -> category slug (only galleries that actually contain images)
GALLERY_MAP = {
    "myrealizm": "realism",
    "mytattoographika": "graphic",
    "myminitattoo": "mini",
    "myperecritie": "overlapping",
    "mypirsing": "piercing",
}
CAP = 20

NAMES = ["Valerii","Viktoria","Christian","Kris","Anastasija","Fred","Weys",
         "Aleks","Igor","Natali","Julia","Alex","Rolando","Andrey","Evgeny","Oleg"]
PORTRAIT_RE = re.compile(r"(noroot|IMG_0501|ohFk|Remove-bg)", re.I)


def get(url):
    if url.startswith("//"): url = "https:" + url
    r = requests.get(url, headers=H, timeout=40); r.raise_for_status()
    return r.content

def save(content, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "wb").write(content)

def full_only(urls):
    out, seen = [], set()
    for u in urls:
        if "thb.tildacdn" in u or "/resize" in u: continue
        if "static.tildacdn" not in u: continue
        if u not in seen: seen.add(u); out.append(u)
    return out


# ---------------- artists: zip portraits & names by document top order ----------
def first_top(eid):
    m = re.search(r'data-elem-id="'+re.escape(eid)+r'"[^{]*\{([^}]*)\}', de)
    if m:
        t = re.findall(r'top:\s*(-?\d+)px', m.group(1))
        if t: return int(t[0])
    return None

def build_artists():
    i = de.find("Valerii")
    a, b = de.rfind('id="rec', 0, i), de.find('id="rec', i)
    soup = BeautifulSoup(de[a:b], "html.parser")
    names, imgs = [], []
    seen_names = set()
    for el in soup.find_all(class_="tn-elem"):
        eid = el.get("data-elem-id")
        if not eid: continue
        img = el.find("img")
        if img and img.get("data-original") and PORTRAIT_RE.search(img["data-original"]):
            t = first_top(eid)
            if t is not None: imgs.append((t, img["data-original"]))
        else:
            txt = el.get_text(strip=True).lstrip("# ").strip()
            if txt in NAMES and txt not in seen_names:
                t = first_top(eid)
                if t is not None:
                    names.append((t, txt)); seen_names.add(txt)
    names.sort(); imgs.sort()
    mapping = {}
    for (nt, name), (it, url) in zip(names, imgs):
        mapping[name.lower()] = url
    # download
    out = {}
    for slug, url in mapping.items():
        try:
            save(get(url), os.path.join(OUT, "artists", f"{slug}.png"))
            out[slug] = f"img/artists/{slug}.png"
            print(f"  artist {slug} <- {url.split('/')[-2]}")
        except Exception as e:
            print(f"  ! artist {slug}: {e}")
        time.sleep(0.03)
    return out


# ---------------- gallery ----------
def popup_images(name):
    soup = BeautifulSoup(de, "html.parser")
    hook = soup.find(attrs={"data-tooltip-hook": f"#popup:{name}"})
    if not hook: return []
    c = hook
    for _ in range(6):
        if c.parent and c.parent.get("class") and any("t-rec" in x for x in c.parent.get("class")):
            c = c.parent; break
        if c.parent: c = c.parent
    urls = []
    for el in c.find_all(True):
        for at in ("data-original", "src", "href"):
            v = el.get(at)
            if v and "static.tildacdn" in v and re.search(r"\.(jpe?g|png|webp)$", v, re.I):
                urls.append(v)
    return full_only(urls)

def build_gallery():
    # wipe old gallery dirs to remove wrong categories
    gdir = os.path.join(OUT, "gallery")
    if os.path.isdir(gdir): shutil.rmtree(gdir)
    result = {}
    for popup, cat in GALLERY_MAP.items():
        urls = popup_images(popup)[:CAP]
        files = []
        for url in urls:
            ext = os.path.splitext(urlparse(url).path)[1] or ".jpg"
            name = f"{cat}_{len(files)+1:02d}{ext}"
            try:
                save(get(url), os.path.join(OUT, "gallery", cat, name))
                files.append(f"img/gallery/{cat}/{name}")
            except Exception as e:
                print(f"  ! gallery {url}: {e}")
            time.sleep(0.03)
        result[cat] = files
        print(f"  gallery {cat}: {len(files)}")
    return result


# ---------------- studio ----------
def build_studio():
    sdir = os.path.join(OUT, "studio")
    if os.path.isdir(sdir): shutil.rmtree(sdir)
    idx = de.find("gemütliches Studio")
    a = de.rfind('id="rec', 0, idx); b = de.find('id="rec', idx)
    b2 = de.find('id="rec', b + 10)
    block = de[a:(b2 if b2 > 0 else b)]
    urls = full_only(re.findall(r'https?://static\.tildacdn\.com/[^\s"\']+\.(?:jpe?g|JPG|JPEG)', block))
    # keep only the real interior photos (IMG_648x series)
    urls = [u for u in urls if re.search(r"IMG_648", u)]
    out = []
    for n, url in enumerate(urls[:8], 1):
        try:
            save(get(url), os.path.join(OUT, "studio", f"studio_{n:02d}.jpg"))
            out.append(f"img/studio/studio_{n:02d}.jpg")
            print(f"  studio studio_{n:02d}.jpg <- {url.split('/')[-1]}")
        except Exception as e:
            print(f"  ! studio {url}: {e}")
        time.sleep(0.03)
    return out


def main():
    print("artists..."); artists = build_artists()
    print("gallery..."); gallery = build_gallery()
    print("studio...");  studio = build_studio()
    logo = "img/brand/logo.png"
    index = {"artists": artists, "gallery": gallery, "studio": studio, "brand": {"logo": logo}}
    json.dump(index, open(os.path.join(OUT, "index.json"), "w", encoding="utf-8"), indent=2)
    print("\nartists:", len(artists), "| studio:", len(studio))
    for c, f in gallery.items(): print(f"  {c}: {len(f)}")
    print("wrote index.json")


if __name__ == "__main__":
    main()
