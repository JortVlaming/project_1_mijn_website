from datetime import datetime

from flask import Flask, render_template, request, session, redirect, url_for, abort

from database import Database, User, Post

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
    return render_template("search.html", results=db.userManager.search_for_users(request.args.get("query")), query=request.args.get("query"))

@app.route('/user/<string:name>')
def user(name:str):
    if not db.userManager.user_exists(name):
        return 404
    # todo display proper user information
    return render_template("user.html", user=db.userManager.get_user(name), posts=[Post("test", 0, "insert lorem ipsum die ik niet kan auto generaten want dit is vscode niet", datetime.now()),Post("test", 0, "insert lorem ipsum die ik niet kan auto generaten want dit is vscode niet", datetime.now()),Post("test", 0, "insert lorem ipsum die ik niet kan auto generaten want dit is vscode niet", datetime.now()),Post("test", 0, "insert lorem ipsum die ik niet kan auto generaten want dit is vscode niet", datetime.now())])

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

@app.context_processor
def inject_template_scope():
    injections = dict()

    injections.update(user=get_user_from_session())

    return injections


if __name__ == '__main__':
    app.run(port=5500, debug=True)
