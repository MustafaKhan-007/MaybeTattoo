from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


@app.route("/artists")
def artists():
    return render_template("artists.html")


@app.route("/booking")
def booking():
    selected_artist = request.args.get("artist", "")
    return render_template("booking.html", selected_artist=selected_artist)


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
