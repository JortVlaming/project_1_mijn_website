from datetime import datetime

from flask import Flask, render_template, request

from database import Database, User, Post

app = Flask(__name__)

app.secret_key = "7VLNMnLD3*sS2QgC"

db = Database()

@app.route('/')
def home():
    return render_template("index.html", recents=[])

@app.route('/search')
def search():
    # TODO search
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


if __name__ == '__main__':
    app.run(port=5500, debug=True)
