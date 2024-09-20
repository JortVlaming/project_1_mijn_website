from flask import Flask, render_template, session, redirect, url_for
from database import Database

app = Flask(__name__)

app.secret_key = "7VLNMnLD3*sS2QgC"

db = Database()

@app.route('/')
def home():
    return render_template("index.html", db=db, recents=[])

@app.route('/set_token')
def set_token():
    session["token"] = db.generate_token("test", "test")
    return redirect(url_for("home"))

@app.route('/reset_token')
def reset_token():
    session["token"] = None

    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(port=5500, debug=True)
