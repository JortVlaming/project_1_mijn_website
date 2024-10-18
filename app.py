import datetime
import math

from flask import Flask, render_template, request, session, redirect, url_for, abort

from database import Database, User

app = Flask(__name__)

app.secret_key = "7VLNMnLD3*sS2QgC"

db = Database()

def get_user_from_session() -> User | None:
    if "token" not in session:
        return None
    if session.get("token") is None:
        return None
    if not db.tokenManager.verify_token(session["token"]):
        return None

    return db.tokenManager.token_to_user(session["token"])

@app.route('/')
def home():
    return render_template("index.html", recents=[], session=session)

@app.route('/search')
def search():
    results = db.userManager.search_for_users(request.args.get("query"))

    print(results)

    return render_template("search.html", results=results, query=request.args.get("query"))

@app.route('/user/<string:name>')
def user(name:str):
    if not db.userManager.user_exists(name):
        return 404
    return render_template("user.html", requested_user=db.userManager.get_user_information(name), posts=db.userManager.get_user_posts(name))

@app.route("/user/me")
def user_self():
    if get_user_from_session() is None:
        return abort(404)

    return redirect(url_for("user", name=get_user_from_session().username))

@app.route('/login')
def login():
    return render_template("login.html", hide_login_button=True)

@app.route('/auth/login')
def login_callback():
    username = request.args.get("username")
    password = request.args.get("password")

    if not db.userManager.user_exists(username):
        return abort(501)

    valid = db.userManager.verify_login(username, password)

    if not valid:
        # TODO redirect back to login with error
        return abort(501)

    token = db.tokenManager.generate_token(db.userManager.username_to_id(username), username, password)

    session["token"] = token

    return redirect(url_for("home"))

@app.route('/auth/logout')
def logout_callback():
    session.pop("token", None)
    return redirect(url_for("home"))

@app.route('/api/create_post', methods=["POST"])
def create_post():
    if get_user_from_session() is None:
        return abort(401)

    if request.form.get("content") == "":
        return redirect(url_for("user_self"))

    db.userManager.create_post(get_user_from_session(), request.form.get("content"))

    return redirect(url_for("user_self"))

@app.context_processor
def inject_template_scope():
    injections = dict()

    injections.update(user=get_user_from_session(), pdate=prettydate)

    return injections

def prettydate(d):
    diff = datetime.datetime.now() - d
    s = diff.seconds
    if diff.days > 7:
        return d.strftime('%d %b %y')
    elif diff.days == 1:
        return '1 day ago'
    elif diff.days > 1:
        return '{} days ago'.format(int(diff.days))
    elif s <= 1:
        return 'just now'
    elif s < 60:
        return '{} seconds ago'.format(int(s))
    elif s < 120:
        return '1 minute ago'
    elif s < 3600:
        return '{} minutes ago'.format(int(s/60))
    elif s < 7200:
        return '1 hour ago'
    else:
        return '{} hours ago'.format(int(s/3600))

if __name__ == '__main__':
    app.run(port=5500, debug=True)
