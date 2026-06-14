"""
Second pass: parse the saved raw HTML to (a) find the YouTube video id used in
the 'how we work' popup, and (b) map gallery popups to the image URLs that live
inside them. Writes static/images/_parsed.json.
"""
import json
import os
import re

from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(ROOT, "static", "images", "_raw")
OUT = os.path.join(ROOT, "static", "images", "_parsed.json")

POPUPS = [
    "myrealizm",
    "mytattoographika",
    "myminitattoo",
    "myperecritie",
    "mypirsing",
    "mygallery1",
]

TILDA_IMG_RE = re.compile(
    r"https?://[a-z]+\.tildacdn\.(?:com|net|one)/[^\s\"'\\)]+\.(?:jpg|jpeg|png|webp)",
    re.IGNORECASE,
)


def urls_in(node):
    found = []
    for el in node.find_all(True):
        for attr in ("src", "data-original", "data-src", "href", "style", "data-bg"):
            v = el.get(attr)
            if not v:
                continue
            for m in TILDA_IMG_RE.findall(v):
                found.append(m.rstrip(".,);"))
    # dedupe preserving order
    seen, out = set(), []
    for u in found:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def find_youtube(html):
    ids = set()
    for m in re.finditer(r"youtu(?:\.be/|be\.com/(?:embed/|watch\?v=|v/))([A-Za-z0-9_\-]{11})", html):
        ids.add(m.group(1))
    # tilda often stores video in data-content or vimeo/youtube fields
    for m in re.finditer(r"(?:videoid|video_id|youtube)['\"]?\s*[:=]\s*['\"]([A-Za-z0-9_\-]{11})", html, re.I):
        ids.add(m.group(1))
    return sorted(ids)


def main():
    result = {"youtube_ids": [], "popups": {}}
    for lang in ("de", "en"):
        path = os.path.join(RAW_DIR, f"page_{lang}.html")
        if not os.path.exists(path):
            continue
        html = open(path, encoding="utf-8").read()
        result["youtube_ids"] = sorted(set(result["youtube_ids"]) | set(find_youtube(html)))

        soup = BeautifulSoup(html, "html.parser")
        for popup in POPUPS:
            hook = soup.find(attrs={"data-tooltip-hook": f"#popup:{popup}"})
            if not hook:
                continue
            # climb to the record container
            container = hook
            for _ in range(6):
                if container.parent and container.parent.get("class") and \
                        any("t-rec" in c for c in container.parent.get("class")):
                    container = container.parent
                    break
                if container.parent:
                    container = container.parent
            imgs = urls_in(container)
            key = f"{popup}"
            prev = result["popups"].get(key, [])
            merged = prev + [u for u in imgs if u not in prev]
            result["popups"][key] = merged

    for k, v in result["popups"].items():
        print(f"{k}: {len(v)} images")
    print("youtube_ids:", result["youtube_ids"])

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
