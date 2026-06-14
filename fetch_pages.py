import os, requests
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124 Safari/537.36"}
os.makedirs("_raw", exist_ok=True)
for lang, url in (("de", "https://maybetattoo.de/"), ("en", "https://maybetattoo.de/en")):
    r = requests.get(url, headers=H, timeout=40)
    r.raise_for_status()
    open(f"_raw/page_{lang}.html", "w", encoding="utf-8").write(r.text)
    print(lang, len(r.text), "bytes")
print("done")
