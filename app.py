from datetime import datetime

from flask import Flask, render_template, session, redirect, url_for, request
from database import Database, User

app = Flask(__name__)

app.secret_key = "7VLNMnLD3*sS2QgC"

db = Database()

@app.route('/')
def home():
    return render_template("index.html", db=db, recents=[])

@app.route('/search')
def search():
    # TODO search
    return render_template("search.html", db=db, results=[User(0, "test", "Jort Vlaming", "Software Developer", "Korte test about me"), User(0, "test", "Jort Vlaming", "Software Developer", "Korte test about me")], query=request.args.get("query"))

@app.route('/user')
def user():
    # todo display proper user information
    if (request.args.get("username") is None):
        return redirect(url_for("home"))
    return render_template("user.html", db=db, user=User(0, "test", "Jort Vlaming", "Software Developer", "Korte test about me"))

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
