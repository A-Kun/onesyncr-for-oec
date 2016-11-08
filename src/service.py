#!flask/bin/python
from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
import github3
from github3 import login
import requests
import re

app = Flask(__name__, static_url_path='/static')

file = open("static/dashboard.html")
DASHBOARD = file.read()
file.close()
del file


@app.route("/api", methods=["GET"])
def hello_world():
    return "Hello, World!"


@app.route("/", methods=["GET"])
def login_page():
    return app.send_static_file("login.html")


@app.route("/dashboard", methods=["GET"])
def login_github():
    code = request.args.get("code")
    response = requests.post("https://github.com/login/oauth/access_token?client_id=56e49d113b3037c709a7"
                             + "&client_secret=aa2f85d97a29ad2c4791af0abd869a24a45eb970&code=" + code)
    content = response.content.decode()
    match = re.match("access_token=(.+?)&|$", content)
    token = match.group(1)
    gh = login(token=token)
    user = gh.user()
    return DASHBOARD.replace("{{ name }}", user.name).replace("{{ login }}", user.login)


if __name__ == "__main__":
    app.run(debug=True)
