"""Static content/data for the MaybeTattoo Berlin site.

Artist roster, gallery categories, services, reviews and shared studio info.
Gallery image lists are loaded from the asset index produced by build_assets.py
so the site always reflects whatever was actually downloaded.
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- studio info
STUDIO = {
    "name": "MaybeTattoo Berlin",
    "address": "Dusseldorfer-Straße 48, 10707 Berlin",
    "hours": "Mon–Sun 10:00–22:00",
    "phone_display": "+49 30 52014472",
    "phone_tel": "+493052014472",
    "whatsapp": "https://wa.me/4917667383970",
    "instagram": "https://instagram.com/maybe.tattoo.de",
    "maps_link": "https://goo.gl/maps/p6c6DBGaWE1uQLmE7",
    "reviews_link": "https://goo.gl/maps/LXZLv4wHieKJCbLs7",
    "maps_embed": (
        "https://www.google.com/maps?q=Dusseldorfer-Stra%C3%9Fe+48,+10707+Berlin&output=embed"
    ),
    # No public YouTube id was discoverable in the source markup, so the home
    # page uses a styled placeholder player (see templates/index.html).
    "youtube_id": "",
    "legal": {
        "datenschutz": "http://maybetattoo.de/datenschutz",
        "agb": "http://maybetattoo.de/agb",
        "impressum": "http://maybetattoo.de/impressum",
        "cookies": "http://maybetattoo.de/Cookies",
    },
    "stats": [
        {"value": 14500, "suffix": "+", "key": "stat_clients"},
        {"value": 2000, "suffix": "+", "key": "stat_reviews"},
        {"value": 9, "suffix": "", "key": "stat_artists"},
        {"value": 5, "suffix": "+", "key": "stat_years"},
    ],
}

# ---------------------------------------------------------------- artists
# price_from = indicative session starting price (EUR). Only shown after the
# user opens a booking panel on /artists (never on the home page).
ARTISTS = [
    {"slug": "valerii", "name": "Valerii", "years": 20, "tattoos": 2935,
     "styles": ["Realistic", "Graphic", "Japanese", "Biomechanical", "Old School"],
     "price_from": 200,
     "bio_en": "Two decades behind the machine. Valerii blends realism with bold Japanese and biomechanical work.",
     "bio_de": "Zwei Jahrzehnte Erfahrung. Valerii verbindet Realismus mit kraftvollen japanischen und biomechanischen Motiven."},
    {"slug": "viktoria", "name": "Viktoria", "years": 6, "tattoos": 1213,
     "styles": ["Realism", "Japan", "Anime"],
     "price_from": 180,
     "bio_en": "Specialist in expressive realism, Japanese motifs and clean anime linework.",
     "bio_de": "Spezialistin für ausdrucksstarken Realismus, japanische Motive und klare Anime-Linien."},
    {"slug": "christian", "name": "Christian", "years": 22, "tattoos": 4287,
     "styles": ["Full Realistic", "Micro Realism"],
     "price_from": 220,
     "bio_en": "The studio's most experienced artist — full realistic and micro-realism portraits.",
     "bio_de": "Der erfahrenste Artist des Studios — vollständige Realistik und Micro-Realism-Porträts."},
    {"slug": "kris", "name": "Kris", "years": 6, "tattoos": 1167,
     "styles": ["Realism"],
     "price_from": 170,
     "bio_en": "Focused entirely on realism, Kris brings depth and contrast to every piece.",
     "bio_de": "Ganz auf Realismus fokussiert bringt Kris Tiefe und Kontrast in jedes Motiv."},
    {"slug": "anastasija", "name": "Anastasija", "years": 5, "tattoos": 1360,
     "styles": ["Realism", "Graphic"],
     "price_from": 160,
     "bio_en": "Combines fine realism with striking graphic compositions.",
     "bio_de": "Verbindet feinen Realismus mit markanten grafischen Kompositionen."},
    {"slug": "fred", "name": "Fred", "years": 7, "tattoos": 1860,
     "styles": ["Realism"],
     "price_from": 180,
     "bio_en": "Realism specialist with a meticulous eye for skin tone and texture.",
     "bio_de": "Realismus-Spezialist mit einem präzisen Blick für Hauttöne und Texturen."},
    {"slug": "weys", "name": "Weys", "years": 7, "tattoos": 1894,
     "styles": ["Realistic", "Graphic", "Minimalistic"],
     "price_from": 180,
     "bio_en": "From minimal fine-line to bold graphic realism — versatile and precise.",
     "bio_de": "Von minimalistischen Fine-Lines bis zu kraftvollem grafischem Realismus — vielseitig und präzise."},
    {"slug": "aleks", "name": "Aleks", "years": 16, "tattoos": 2481,
     "styles": ["Realistic", "Graphic", "Minimalistic"],
     "price_from": 200,
     "bio_en": "Sixteen years of experience across realistic, graphic and minimalistic styles.",
     "bio_de": "Sechzehn Jahre Erfahrung in realistischen, grafischen und minimalistischen Stilen."},
    {"slug": "igor", "name": "Igor", "years": 12, "tattoos": 1232,
     "styles": ["Realistic", "Graphic"],
     "price_from": 190,
     "bio_en": "Realistic and graphic work with strong composition and flow.",
     "bio_de": "Realistische und grafische Arbeiten mit starker Komposition und Fluss."},
    {"slug": "rolando", "name": "Rolando", "years": 6, "tattoos": 2235,
     "styles": ["Graphic", "Realism"],
     "price_from": 170,
     "bio_en": "Graphic-forward artist who loves bold, story-driven pieces.",
     "bio_de": "Grafisch orientierter Artist mit Liebe zu kraftvollen, erzählerischen Motiven."},
    {"slug": "andrey", "name": "Andrey", "years": 5, "tattoos": 1931,
     "styles": ["Realistic", "Graphic", "Minimalistic"],
     "price_from": 160,
     "bio_en": "Clean, modern realism and minimal graphic design.",
     "bio_de": "Sauberer, moderner Realismus und minimalistisches Grafikdesign."},
    {"slug": "evgeny", "name": "Evgeny", "years": 7, "tattoos": 2846,
     "styles": ["Realistic", "Graphic", "Minimalistic"],
     "price_from": 180,
     "bio_en": "High-volume realism specialist with a refined graphic touch.",
     "bio_de": "Produktiver Realismus-Spezialist mit feinem grafischem Gespür."},
    {"slug": "oleg", "name": "Oleg", "years": 9, "tattoos": 2635,
     "styles": ["Graphic", "Realism", "Cover Up"],
     "price_from": 190,
     "bio_en": "Cover-up expert — transforms old tattoos into bold new graphic realism.",
     "bio_de": "Cover-up-Experte — verwandelt alte Tattoos in kraftvollen neuen grafischen Realismus."},
]

ARTISTS_BY_SLUG = {a["slug"]: a for a in ARTISTS}
FEATURED_SLUGS = ["valerii", "christian", "weys", "aleks"]
FEATURED_ARTISTS = [ARTISTS_BY_SLUG[s] for s in FEATURED_SLUGS]

# ---------------------------------------------------------------- services
SERVICES = [
    {"slug": "realism", "icon": "fa-eye", "key": "svc_realism"},
    {"slug": "graphic", "icon": "fa-pen-nib", "key": "svc_graphic"},
    {"slug": "mini", "icon": "fa-feather", "key": "svc_mini"},
    {"slug": "overlapping", "icon": "fa-layer-group", "key": "svc_overlapping"},
    {"slug": "colour", "icon": "fa-palette", "key": "svc_colour"},
    {"slug": "polynesian", "icon": "fa-leaf", "key": "svc_polynesian"},
]

# ---------------------------------------------------------------- gallery
GALLERY_CATEGORIES = [
    {"slug": "realism", "key": "cat_realism"},
    {"slug": "graphic", "key": "cat_graphic"},
    {"slug": "mini", "key": "cat_mini"},
    {"slug": "overlapping", "key": "cat_overlapping"},
    {"slug": "colour", "key": "cat_colour"},
    {"slug": "polynesian", "key": "cat_polynesian"},
]


def _load_index():
    path = os.path.join(ROOT, "static", "img", "index.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {"artists": {}, "gallery": {}, "studio": [], "brand": {}}


_INDEX = _load_index()


def artist_photo(slug):
    return _INDEX.get("artists", {}).get(slug, "img/brand/logo.png")


def gallery_images(category=None):
    """Return list of {src, category} dicts."""
    g = _INDEX.get("gallery", {})
    items = []
    cats = [category] if category and category != "all" else [c["slug"] for c in GALLERY_CATEGORIES]
    for cat in cats:
        for src in g.get(cat, []):
            items.append({"src": src, "category": cat})
    return items


def gallery_preview():
    """9 images: 3 realism, 3 graphic, 3 mini for the home teaser."""
    g = _INDEX.get("gallery", {})
    out = []
    for cat in ("realism", "graphic", "mini"):
        for src in g.get(cat, [])[:3]:
            out.append({"src": src, "category": cat})
    return out


def studio_images():
    return _INDEX.get("studio", [])


def logo():
    return _INDEX.get("brand", {}).get("logo", "img/brand/logo.png")


# ---------------------------------------------------------------- reviews
REVIEWS = [
    {"name": "Gini", "text_en": "Absolutely in love with my arm piece. The detail is unreal and the studio is spotless.",
     "text_de": "Ich liebe mein Arm-Tattoo. Die Details sind unglaublich und das Studio ist makellos."},
    {"name": "Marcel", "text_en": "Best shoulder tattoo I could have asked for. Professional, friendly, painless as possible.",
     "text_de": "Das beste Schulter-Tattoo, das ich mir wünschen konnte. Professionell, freundlich, so schmerzfrei wie möglich."},
    {"name": "Anna", "text_en": "From the first consultation to the final session everything was perfect. Highly recommend!",
     "text_de": "Von der ersten Beratung bis zur letzten Sitzung war alles perfekt. Sehr zu empfehlen!"},
    {"name": "Andre", "text_en": "My arm and thigh tattoos turned out better than the sketch. True artists here.",
     "text_de": "Meine Arm- und Oberschenkel-Tattoos sind besser geworden als die Skizze. Echte Künstler hier."},
    {"name": "Cons", "text_en": "Huge back piece done over several sessions — flawless work and great atmosphere.",
     "text_de": "Großes Rücken-Tattoo über mehrere Sitzungen — makellose Arbeit und tolle Atmosphäre."},
    {"name": "Sofia", "text_en": "Clean lines, friendly team and they really listened to my idea. 5 stars.",
     "text_de": "Saubere Linien, freundliches Team und sie sind wirklich auf meine Idee eingegangen. 5 Sterne."},
]

# ---------------------------------------------------------------- pricing
PRICING = [
    {"key": "price_small", "from": 150},
    {"key": "price_medium", "from": 300},
    {"key": "price_large", "from": 600},
]
