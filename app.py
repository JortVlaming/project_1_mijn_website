import datetime
from secrets import compare_digest

from flask import Flask, render_template, request, session, redirect, url_for, abort, jsonify
from werkzeug.security import generate_password_hash

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
    return render_template("index.html", recents=db.get_recent_posts(), session=session, hide_search_bar=True)

@app.route('/search')
def search():
    results = db.userManager.search_for_users(request.args.get("query"))

    print(results)

    return render_template("search.html", results=results, query=request.args.get("query"), hide_search_bar=True)

@app.route('/user/<string:name>')
def user(name:str):
    if not db.userManager.user_exists(name):
        return redirect(url_for("user_self"))
    return render_template("user.html", requested_user=db.userManager.get_user_information(name), posts=db.userManager.get_user_posts(name))

@app.route("/user/me")
def user_self():
    if get_user_from_session() is None:
        return redirect(url_for("home"))

    return redirect(url_for("user", name=get_user_from_session().username))

@app.route("/user/update", methods=["POST"])
def edit_user():
    user = get_user_from_session()

    if user is None:
        return redirect(url_for("login"))

    naam = request.form["displayNameInput"]
    opleiding = request.form["opleidingInput"]
    aboutme = request.form["descriptionInput"]

    db.userManager.set_displayname(user.id, naam)
    db.userManager.set_opleiding(user.id, opleiding)
    db.userManager.set_aboutme(user.id, aboutme)

    return redirect(url_for("user_self"))

@app.route('/login')
def login():
    if get_user_from_session() is not None:
        return redirect(url_for("user_self"))
    return render_template("login.html", hide_login_button=True, s_error=request.args.get("s_error"), l_error=request.args.get("l_error"), hide_search_bar=True)

@app.route('/auth/login')
def login_callback():
    username = request.args.get("username")
    password = request.args.get("password")

    if not db.userManager.user_exists(username):
        return abort(501)

    valid = db.userManager.verify_login(username, password)

    if not valid:
        return redirect(url_for("login", l_error="Invalid username or password"))

    token = db.tokenManager.generate_token(db.userManager.username_to_id(username), username, password)

    session["token"] = token

    return redirect(url_for("home"))

@app.route('/auth/signup')
def signup_callback():
    username = request.args.get("username")
    password = request.args.get("password")
    confirm_password = request.args.get("confirm_password")

    if db.userManager.user_exists(username):
        return redirect(url_for("login", s_error="Username already registered"))

    if not compare_digest(password, confirm_password):
        return redirect(url_for("login", s_error="Passwords do not match"))

    db.userManager.add_user(username, username, generate_password_hash(password), "", "")

    token = db.tokenManager.generate_token(db.userManager.username_to_id(username), username, password)

    session["token"] = token

    return redirect(url_for("finish_signup_callback"))

@app.route('/auth/finish_signup', methods=["POST", "GET"])
def finish_signup_callback():
    user = get_user_from_session()
    if request.method == "POST":
        db.userManager.set_aboutme(user.id, request.form.get("aboutme"))
        db.userManager.set_opleiding(user.id, request.form.get("opleiding"))

        return redirect(url_for("user_self"))
    else:
        return render_template("complete_signup.html", hide_login_button=True, hide_search_bar=True)

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

@app.before_request
def pre_load():
    if get_user_from_session() is None:
        pass


    user = get_user_from_session()

    if user is None:
        return

    if (user.aboutme is None or user.aboutme == "" or user.opleiding is None or user.opleiding == "") and request.path != "/auth/finish_signup" and not request.path.startswith("/static"):
        return redirect(url_for("finish_signup_callback"))

@app.context_processor
def inject_template_scope():
    injections = dict()

    injections.update(user=get_user_from_session(), pdate=prettydate, show_aside=True, hide_search_bar=False)

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
