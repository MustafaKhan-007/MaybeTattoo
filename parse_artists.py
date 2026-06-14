"""
Parse artist portrait images from the DE page. Each artist sits in a Tilda
gallery card. We locate the artist name headings and pick the nearest full-size
tilda image that appears in the same card block.
Writes static/images/_artists.json
"""
import json
import os
import re

from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(ROOT, "static", "images", "_raw")
OUT = os.path.join(ROOT, "static", "images", "_artists.json")

NAMES = [
    "Valerii", "Viktoria", "Christian", "Kris", "Anastasija", "Fred",
    "Weys", "Aleks", "Igor", "Natali", "Julia", "Alex", "Rolando",
    "Andrey", "Evgeny", "Oleg",
]

FULL_IMG_RE = re.compile(
    r"https?://static\.tildacdn\.(?:com|net|one)/[^\s\"'\\)]+\.(?:jpg|jpeg|png|webp)",
    re.IGNORECASE,
)


def main():
    html = open(os.path.join(RAW_DIR, "page_de.html"), encoding="utf-8").read()
    soup = BeautifulSoup(html, "html.parser")

    # Tilda artist cards: find the gallery block containing "Tattoo-Artist" labels.
    # Strategy: find each text node that exactly equals an artist name within a
    # heading, climb to the enclosing card and collect the first full-size image.
    artists = {}
    # Find all elements whose text is one of the names
    for el in soup.find_all(string=re.compile("|".join(re.escape(n) for n in NAMES))):
        text = el.strip()
        # match exact-ish
        name = None
        for n in NAMES:
            if text == n or text == f"# {n}":
                name = n
                break
        if not name:
            continue
        # climb up to find a container that also has an image
        node = el
        chosen = None
        for _ in range(10):
            node = node.parent
            if node is None:
                break
            html_chunk = str(node)
            imgs = FULL_IMG_RE.findall(html_chunk)
            # exclude obvious icons/logos
            imgs = [i for i in imgs if not re.search(r"(logo|maybe|insta|whats|tattoo_1|vector|arrow|play|call|location|ellipse|group_1|frame)", i, re.I)]
            if imgs:
                chosen = imgs[0]
                break
        if chosen and name not in artists:
            artists[name] = chosen

    for k, v in artists.items():
        print(f"{k}: {v.split('/')[-2]}")
    print(f"\nMapped {len(artists)}/{len(NAMES)} artists")
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(artists, f, indent=2)


if __name__ == "__main__":
    main()
