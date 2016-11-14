#!flask/bin/python
import re

import requests
from flask import Flask
from flask import request
from github3 import login

from d4 import main

app = Flask(__name__, static_url_path='/static')

redirect_file = open("static/redirect.html")
REDIRECT_PAGE = redirect_file.read()
redirect_file.close()
del redirect_file
dashboard_file = open("static/dashboard.html")
DASHBOARD_PAGE = dashboard_file.read()
dashboard_file.close()
del dashboard_file


@app.route("/api", methods=["GET"])
def hello_world():
    return "Hello, World!"


@app.route("/", methods=["GET"])
def login_page():
    return app.send_static_file("login.html")


@app.route("/redirect", methods=["GET"])
def login_redirect():
    code = request.args.get("code")
    response = requests.post("https://github.com/login/oauth/access_token?client_id=56e49d113b3037c709a7" +
                             "&client_secret=aa2f85d97a29ad2c4791af0abd869a24a45eb970&code=" + code)
    content = response.content.decode()
    match = re.match("access_token=(.+?)&|$", content)
    token = match.group(1)
    gh = login(token=token)
    user = gh.user()
    return REDIRECT_PAGE.replace("{{ name }}", user.name).replace("{{ login }}", user.login).replace("{{ token }}", token)


@app.route("/dashboard", methods=["GET"])
def dashboard():
    token = request.args.get("token")
    gh = login(token=token)
    user = gh.user()
    return DASHBOARD_PAGE.replace("{{ name }}", user.name).replace("{{ login }}", user.login).replace("{{ token }}", token)


@app.route("/check", methods=["GET"])
def check_for_update():
    token = request.args.get("token")
    pr_url = main.run(token)
    return 'Done. A <a href="' + pr_url + '">pull request</a> has been created.'


if __name__ == "__main__":
    app.run(debug=True)
