"""
Final asset builder. Reads the parsed popup/artist data and the raw HTML, then
downloads full-resolution images into a clean folder layout that the Flask app
serves:

  static/img/artists/<slug>.png         artist portrait cut-outs
  static/img/gallery/<category>/NN.jpg   gallery works by category
  static/img/studio/NN.jpg               studio interior photos
  static/img/brand/...                   logo + icons

Also writes static/img/index.json describing what was downloaded.
Run: python build_assets.py
"""
import json
import os
import re
import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(ROOT, "static", "images", "_raw")
OUT = os.path.join(ROOT, "static", "img")
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124 Safari/537.36"}

# ---- artist name order (matches portrait DOM order) ----
ARTIST_ORDER = [
    "valerii", "viktoria", "christian", "kris", "anastasija", "fred",
    "weys", "aleks", "igor", "natali", "julia", "alex", "rolando",
    "andrey", "evgeny", "oleg",
]

# popup id -> our category slug
GALLERY_MAP = {
    "myrealizm": "realism",
    "mytattoographika": "graphic",
    "myminitattoo": "mini",
    "myperecritie": "overlapping",
    "mypirsing": "colour",       # piercing set reused as colour teaser
    "mygallery1": "polynesian",
}
CATEGORY_CAP = 20


def get(url):
    if url.startswith("//"):
        url = "https:" + url
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.content


def save(content, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(content)


def full_static_urls(url_list):
    """Keep only full-size static.tildacdn urls (drop thb thumbnails), dedupe."""
    out, seen = [], set()
    for u in url_list:
        if "thb.tildacdn" in u or "/resize" in u or "/resizeb" in u:
            continue
        if "static.tildacdn" not in u:
            continue
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def build_artists():
    block_html = ""
    html = open(os.path.join(RAW_DIR, "page_de.html"), encoding="utf-8").read()
    i = html.find("Valerii")
    start = html.rfind('id="rec', 0, i)
    end = html.find('id="rec', i)
    block = html[start:end]
    ordered = re.findall(r"static\.tildacdn\.com/tild[^\"']+\.png", block)
    portraits, seen = [], set()
    for u in ordered:
        fn = u.split("/")[-1]
        if re.search(r"(noroot|Remove-bg|IMG_0501|ohFk)", fn, re.I):
            full = "https://" + u
            if full not in seen:
                seen.add(full)
                portraits.append(full)
    mapping = {}
    for slug, url in zip(ARTIST_ORDER, portraits):
        try:
            save(get(url), os.path.join(OUT, "artists", f"{slug}.png"))
            mapping[slug] = f"img/artists/{slug}.png"
            print(f"  artist {slug} <- {url.split('/')[-2]}")
        except Exception as e:
            print(f"  ! artist {slug} failed: {e}")
        time.sleep(0.03)
    return mapping


def build_gallery():
    parsed = json.load(open(os.path.join(ROOT, "static", "images", "_parsed.json"), encoding="utf-8"))
    result = {}
    for popup, urls in parsed["popups"].items():
        cat = GALLERY_MAP.get(popup)
        if not cat:
            continue
        full = full_static_urls(urls)[:CATEGORY_CAP]
        files = result.setdefault(cat, [])
        for n, url in enumerate(full, 1):
            ext = os.path.splitext(urlparse(url).path)[1] or ".jpg"
            name = f"{cat}_{len(files)+1:02d}{ext}"
            try:
                save(get(url), os.path.join(OUT, "gallery", cat, name))
                files.append(f"img/gallery/{cat}/{name}")
                print(f"  gallery {cat} {name}")
            except Exception as e:
                print(f"  ! gallery {url} failed: {e}")
            time.sleep(0.03)
    return result


def build_studio_and_brand():
    """Pull studio interior photos + logo + hero from the page jpg/png set."""
    html = open(os.path.join(RAW_DIR, "page_de.html"), encoding="utf-8").read()
    # studio interior: the cozy-studio gallery uses jpeg photos. Grab a handful
    # of large static jpgs that are NOT in the work galleries (heuristic: unique
    # filenames like Snapseed / *.JPG / Group_*).
    studio_urls = []
    for u in re.findall(r"static\.tildacdn\.com/tild[^\"']+\.(?:jpe?g|JPG|JPEG)", html):
        fn = u.split("/")[-1]
        if re.search(r"(Snapseed|Snapsee|IMG_8|IMG_6|Group_|95E2|2569|97B2|620F)", fn):
            full = "https://" + u
            if full not in studio_urls:
                studio_urls.append(full)
    studio = []
    for n, url in enumerate(studio_urls[:10], 1):
        try:
            save(get(url), os.path.join(OUT, "studio", f"studio_{n:02d}.jpg"))
            studio.append(f"img/studio/studio_{n:02d}.jpg")
            print(f"  studio studio_{n:02d}.jpg")
        except Exception as e:
            print(f"  ! studio {url} failed: {e}")
        time.sleep(0.03)

    # logo
    brand = {}
    logo_url = "https://static.tildacdn.com/tild3837-3863-4433-a134-323866393461/__2022-02-21__081629.png"
    try:
        save(get(logo_url), os.path.join(OUT, "brand", "logo.png"))
        brand["logo"] = "img/brand/logo.png"
        print("  brand logo.png")
    except Exception as e:
        print(f"  ! logo failed: {e}")
    return studio, brand


def main():
    print("Building artists...")
    artists = build_artists()
    print("Building gallery...")
    gallery = build_gallery()
    print("Building studio + brand...")
    studio, brand = build_studio_and_brand()

    index = {"artists": artists, "gallery": gallery, "studio": studio, "brand": brand}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    print("\nSummary:")
    print("  artists:", len(artists))
    for c, fs in gallery.items():
        print(f"  gallery/{c}: {len(fs)}")
    print("  studio:", len(studio))
    print("wrote", os.path.join(OUT, "index.json"))


if __name__ == "__main__":
    main()
