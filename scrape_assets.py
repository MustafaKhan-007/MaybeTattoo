"""
One-off asset scraper for the MaybeTattoo rebuild.

Fetches the raw HTML of the German and English maybetattoo.de pages, extracts
every Tilda CDN image URL (thb.tildacdn.com + static.tildacdn.com), tries to
find the YouTube video id used in the "how we work" popup, and downloads all
images into static/images/ (categorised where we can infer it).

Run:  python scrape_assets.py
Output: static/images/_manifest.json  + downloaded image files
"""

import json
import os
import re
import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

PAGES = {
    "de": "https://maybetattoo.de/",
    "en": "https://maybetattoo.de/en",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(ROOT, "static", "images")
RAW_DIR = os.path.join(ROOT, "static", "images", "_raw")

TILDA_RE = re.compile(
    r"https?://(?:thb|static|optim)\.tildacdn\.(?:com|net|one)/[^\s\"'\\)]+",
    re.IGNORECASE,
)
YT_RE = re.compile(
    r"(?:youtube\.com/(?:embed/|watch\?v=)|youtu\.be/)([A-Za-z0-9_\-]{11})"
)


def fetch(url):
    print(f"  GET {url}")
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.text


def clean_url(u):
    # strip trailing punctuation that regex sometimes grabs
    return u.rstrip(".,);\\\"'")


def collect():
    os.makedirs(RAW_DIR, exist_ok=True)
    all_urls = set()
    youtube_ids = set()

    for lang, url in PAGES.items():
        try:
            html = fetch(url)
        except Exception as e:
            print(f"  ! failed {url}: {e}")
            continue

        with open(os.path.join(RAW_DIR, f"page_{lang}.html"), "w", encoding="utf-8") as f:
            f.write(html)

        for m in TILDA_RE.findall(html):
            all_urls.add(clean_url(m))
        for m in YT_RE.findall(html):
            youtube_ids.add(m)

        # also parse img/srcset/data-original attributes via bs4
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup.find_all(True):
            for attr in ("src", "data-original", "data-src", "href", "data-bg"):
                val = tag.get(attr)
                if val and "tildacdn" in val:
                    all_urls.add(clean_url(val))
            srcset = tag.get("srcset")
            if srcset:
                for part in srcset.split(","):
                    candidate = part.strip().split(" ")[0]
                    if "tildacdn" in candidate:
                        all_urls.add(clean_url(candidate))

    return sorted(all_urls), sorted(youtube_ids)


def download(urls):
    os.makedirs(IMG_DIR, exist_ok=True)
    manifest = []
    seen_names = {}
    for i, url in enumerate(urls):
        # normalise protocol-relative
        if url.startswith("//"):
            url = "https:" + url
        path = urlparse(url).path
        ext = os.path.splitext(path)[1].lower()
        if ext not in (".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"):
            # skip non-image (css/js) tilda assets
            continue
        base = os.path.basename(path) or f"img_{i}{ext}"
        # dedupe filenames
        if base in seen_names:
            base = f"{i}_{base}"
        seen_names[base] = True
        dest = os.path.join(IMG_DIR, base)
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            r.raise_for_status()
            with open(dest, "wb") as f:
                f.write(r.content)
            manifest.append({"url": url, "file": base, "bytes": len(r.content)})
            print(f"  saved {base} ({len(r.content)} bytes)")
        except Exception as e:
            print(f"  ! failed {url}: {e}")
        time.sleep(0.05)
    return manifest


def main():
    print("Collecting URLs...")
    urls, yt = collect()
    print(f"Found {len(urls)} tilda asset URLs, youtube ids: {yt}")
    manifest = download(urls)
    out = {
        "youtube_ids": yt,
        "image_count": len(manifest),
        "images": manifest,
        "all_urls": urls,
    }
    with open(os.path.join(IMG_DIR, "_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nDone. {len(manifest)} images saved to {IMG_DIR}")
    print(f"YouTube ids: {yt}")


if __name__ == "__main__":
    main()
