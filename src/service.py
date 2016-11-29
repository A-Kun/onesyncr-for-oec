#!flask/bin/python
import re
import requests
import main
from flask import Flask
from flask import request
from github3 import login
# from d4 import main

app = Flask(__name__, static_url_path='/static')


@app.route("/", methods=["GET"])
def login_page():
    return app.send_static_file("login.html")


@app.route("/redirect", methods=["GET"])
def login_redirect():
    redirect_file = open("static/redirect.html")
    redirect_page = redirect_file.read()
    redirect_file.close()
    code = request.args.get("code")
    response = requests.post("https://github.com/login/oauth/access_token?client_id=56e49d113b3037c709a7" +
                             "&client_secret=aa2f85d97a29ad2c4791af0abd869a24a45eb970&code=" + code)
    content = response.content.decode()
    match = re.match("access_token=(.+?)&|$", content)
    token = match.group(1)
    gh = login(token=token)
    user = gh.user()
    return redirect_page.replace("{{ name }}", user.name).replace("{{ login }}", user.login).replace("{{ token }}", token)


@app.route("/dashboard", methods=["GET"])
def dashboard():
    dashboard_file = open("static/dashboard.html")
    dashboard_page = dashboard_file.read()
    dashboard_file.close()
    token = request.args.get("token")
    gh = login(token=token)
    user = gh.user()
    return dashboard_page.replace("{{ name }}", user.name).replace("{{ login }}", user.login).replace("{{ token }}", token)


@app.route("/check", methods=["GET"])
def check_for_update():
    token = request.args.get("token")
    pr_url = main.main()
    return 'Done. A <a href="' + pr_url + '">pull request</a> has been created.'


@app.route("/report", methods=["GET"])
def report_page():
    report_file = open("static/report.html")
    report_page = report_file.read()
    report_file.close()



    return app.send_static_file("report.html")


if __name__ == "__main__":
    app.run(debug=True)
