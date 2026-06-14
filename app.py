"""MaybeTattoo Berlin — Flask application.

Serves the marketing site (home, artists, gallery, about, contact) and a small
booking API. Language (en/de) is resolved from ?lang=, a cookie, then default
'en'; the client-side toggle handles instant switching after first paint.
"""
import json
import os
from datetime import datetime

from flask import (
    Flask, jsonify, make_response, redirect, render_template, request, url_for,
)

import data
from i18n import TRANSLATIONS, t

app = Flask(__name__)

BOOKINGS_FILE = os.path.join(os.path.dirname(__file__), "bookings.jsonl")
SUPPORTED_LANGS = ("en", "de")


def current_lang():
    lang = request.args.get("lang") or request.cookies.get("lang") or "en"
    return lang if lang in SUPPORTED_LANGS else "en"


@app.context_processor
def inject_globals():
    lang = current_lang()

    def _t(key):
        return t(lang, key)

    return {
        "lang": lang,
        "t": _t,
        "translations_json": json.dumps(TRANSLATIONS),
        "studio": data.STUDIO,
        "logo": data.logo(),
        "gallery_categories": data.GALLERY_CATEGORIES,
        "services": data.SERVICES,
        "year": datetime.now().year,
    }


def _resp(template, **ctx):
    """Render and persist the language choice in a cookie."""
    resp = make_response(render_template(template, **ctx))
    lang = current_lang()
    if request.args.get("lang") in SUPPORTED_LANGS:
        resp.set_cookie("lang", lang, max_age=60 * 60 * 24 * 365, samesite="Lax")
    return resp


@app.route("/")
def home():
    return _resp(
        "index.html",
        featured_artists=data.FEATURED_ARTISTS,
        artist_photo=data.artist_photo,
        gallery_preview=data.gallery_preview(),
        reviews=data.REVIEWS,
        stats=data.STUDIO["stats"],
    )


@app.route("/artists")
def artists():
    return _resp(
        "artists.html",
        artists=data.ARTISTS,
        artist_photo=data.artist_photo,
        pricing=data.PRICING,
    )


@app.route("/gallery")
def gallery():
    category = request.args.get("category", "all")
    return _resp(
        "gallery.html",
        images=data.gallery_images(),
        active_category=category,
    )


@app.route("/about")
def about():
    return _resp(
        "about.html",
        studio_images=data.studio_images(),
    )


@app.route("/contact")
def contact():
    return _resp(
        "contact.html",
        artists=data.ARTISTS,
    )


@app.route("/api/book", methods=["POST"])
def api_book():
    payload = request.get_json(silent=True) or request.form.to_dict()
    if not payload:
        return jsonify({"ok": False, "error": "No data received"}), 400

    record = {
        "received_at": datetime.utcnow().isoformat() + "Z",
        "ip": request.remote_addr,
        "data": payload,
    }
    try:
        with open(BOOKINGS_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        pass  # ephemeral filesystems on some hosts; still notify via console

    print("=" * 60)
    print("NEW BOOKING REQUEST")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print("=" * 60)

    return jsonify({"ok": True, "message": "Booking received"})


@app.errorhandler(404)
def not_found(_e):
    return _resp("404.html"), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
