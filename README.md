# MaybeTattoo Berlin — Website

A full-stack prototype rebuild of the [MaybeTattoo Berlin](https://maybetattoo.de/)
studio website. Dark, bold, premium aesthetic with a Flask backend, a bilingual
(EN/DE) front end, a working booking API, and real imagery scraped from the
original site.

> Studio: **Düsseldorfer Straße 48, 10707 Berlin** · Mon–Sun 10:00–22:00

---

## Features

- **5 pages** — Home, Artists, Gallery, About, Contact & Booking
- **Dark editorial design** — Playfair Display + Inter, blood-red/gold accents,
  grain overlay, parallax hero, scroll-reveal animations, animated stat counters
- **Bilingual** — instant EN ⇄ DE toggle (client-side i18n object) with
  server-side first paint and cookie persistence
- **Artists page** — 13 artist cards; pricing is **hidden until** you click
  *Book with …*, which expands a booking accordion with a form
- **Gallery** — sticky category filter (Realism / Graphic / Mini / Overlapping /
  Colour / Polynesian) + Pinterest-style masonry + keyboard-navigable lightbox
- **Contact** — 3-step booking wizard (idea → details → confirm) posting to the API
- **Booking API** — `POST /api/book` logs to `bookings.jsonl` and prints to console
- **Conversion tools** — sticky WhatsApp bubble, GDPR cookie banner
- **Mobile-responsive** — reflows cleanly at ≤980px and ≤768px

---

## Tech stack

| Layer    | Choice                              |
| -------- | ----------------------------------- |
| Backend  | Python 3.11 + Flask                 |
| Frontend | Jinja2 templates, vanilla JS + CSS  |
| Fonts    | Google Fonts (Playfair / Inter)     |
| Icons    | Font Awesome 6 (CDN)                |
| Hosting  | Render.com (Frankfurt region)       |

---

## Project layout

```
MaybeTattoo/
├─ app.py               # Flask app + routes + /api/book
├─ data.py              # artists, gallery, services, reviews, studio info
├─ i18n.py              # EN/DE translation dictionary
├─ requirements.txt
├─ render.yaml          # Render.com web-service config
├─ templates/           # base, index, artists, gallery, about, contact, 404
├─ static/
│  ├─ css/style.css
│  ├─ js/main.js
│  └─ img/
│     ├─ artists/<slug>.png        # portrait cut-outs
│     ├─ gallery/<category>/*.jpeg # works by category
│     ├─ studio/*.jpg              # interior photos
│     ├─ brand/logo.png
│     └─ index.json                # asset manifest (read by data.py)
└─ scrape_assets.py / parse_assets.py / parse_artists.py / build_assets.py
                          # one-off scrapers used to download the imagery
```

---

## Run locally

```bash
# from the project root
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000>.

Booking submissions are appended to `bookings.jsonl` and printed to the console.

---

## Deploy to Render.com

This repo includes `render.yaml`, so the easiest path is a **Blueprint** deploy:

1. Push this folder to a GitHub repository.
2. In the Render dashboard → **New → Blueprint**, pick the repo.
3. Render reads `render.yaml` and creates a Python web service in **Frankfurt**:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - Python 3.11
4. Click **Apply** and wait for the build to finish.

### Manual setup (without the blueprint)

- Environment: **Python 3**
- Region: **Frankfurt (EU Central)**
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`

> Note: Render's free filesystem is ephemeral, so `bookings.jsonl` resets on
> redeploy. For production, swap the file write in `api_book()` for a database
> or an email/Telegram notification.

---

## Re-scraping the imagery

The images under `static/img/` were downloaded from the live site. To refresh
them, run the scrapers in order (requires `requests` + `beautifulsoup4`):

```bash
python scrape_assets.py    # download raw HTML + all Tilda assets
python parse_assets.py     # map gallery popups -> image URLs
python build_assets.py     # organise into static/img/ + write index.json
```

`data.py` reads `static/img/index.json`, so the site always reflects whatever
imagery is present.

---

## Notes & assumptions

- **YouTube video:** no public video id was discoverable in the original page's
  markup (Tilda loads it dynamically), so the home page shows a styled
  placeholder player labelled *"How We Work at MaybeTattoo"*. Drop a real id
  into `STUDIO["youtube_id"]` in `data.py` to embed a live `<iframe>`.
- **Artist portraits** were matched to names by document order from the original
  Zero-Block layout; a couple of face↔name pairings may be approximate in this
  prototype.
- **Pricing** is intentionally only revealed inside the booking accordion on
  `/artists`, never on the home page — per the brief.
- Legal links (Datenschutz, AGB, Impressum, Cookies) point to the originals on
  `maybetattoo.de`.
