#!flask/bin/python
import glob
import re
import requests
import main
import xmltools
from flask import Flask
from flask import request
from github3 import login


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
    with open("static/dashboard.html") as dashboard_file:
        dashboard_page = dashboard_file.read()

    token = request.args.get("token")
    gh = login(token=token)
    user = gh.user()
    return dashboard_page.replace("{{ name }}", user.name).replace("{{ login }}", user.login).replace("{{ token }}", token)


@app.route("/check", methods=["GET"])
def check_for_update():
    main.main()
    return ""


@app.route("/report", methods=["GET"])
def report():
    token = request.args.get("token")
    gh = login(token=token)
    user = gh.user()

    with open("static/report.html") as report_file:
        report_page = report_file.read()

    template = """<tr>
    <td>{{ status }}</td>
    <td>{{ filename }}</td>
    <td>{{ compare }}</td>
    <td>{{ edit }}</td>
    {{ operation }}
    </tr>"""

    html = ""

    result = main.check_difference()

    count = 1
    for next_file in result:
        name = next_file[0].split("/")[-1]
        status = next_file[1]
        if status == "Modified":
            icon_status = '<i class="fa fa-pencil" title="' + status + '"></i>'
        else:
            icon_status = '<i class="fa fa-plus" title="' + status + '"></i>'
        icon_compare = '''<a href="javascript:window.open('/report/compare?file=''' + name + '''');"><i class="fa fa-search"></i></a>'''
        icon_edit = '''<a href="javascript:window.open('/report/edit?file=''' + name + '''');"><i class="fa fa-pencil-square-o"></i></a>'''
        icon_accept = '''<td id="''' + str(count) + '''"><a href="javascript:accept(''' + "'" + next_file[0] + "'," + str(count) + ''');"><i class="fa fa-check right-margin"></i>Accept</a></td>'''
        html += template.replace("{{ filename }}", name).replace("{{ status }}", icon_status).replace("{{ compare }}", icon_compare).replace("{{ edit }}", icon_edit).replace("{{ operation }}", icon_accept)
        count += 1

    xmltools.ensure_empty_dir("_data/accepted")

    return report_page.replace("{{ name }}", user.name).replace("{{ login }}", user.login).replace("{{ token }}", token).replace("{{ report }}", html)


@app.route("/report/compare", methods=["GET"])
def compare():
    with open("static/compare.html") as compare_file:
        compare_page = compare_file.read()

    file = request.args.get("file")
    file = "_data/OEC/" + file

    try:
        file_old = open(file.replace("_data/OEC/", "_data/OEC_old/"), encoding="utf8")
        file_new = open(file, encoding="utf8")
        content_old = file_old.read()
        content_new = file_new.read()
        file_old.close()
        file_new.close()
        compare_page = compare_page.replace("{{ old }}", content_old.replace("<", "&lt;").replace(">", "&gt;"))
        compare_page = compare_page.replace("{{ new }}", content_new.replace("<", "&lt;").replace(">", "&gt;"))
    except FileNotFoundError:
        file_new = open(file, encoding="utf8")
        content_new = file_new.read()
        file_new.close()
        compare_page = compare_page.replace("{{ old }}", "")
        compare_page = compare_page.replace("{{ new }}", content_new.replace("<", "&lt;").replace(">", "&gt;"))

    return compare_page


@app.route("/report/accept", methods=["GET"])
def accept():
    file = request.args.get("file")
    main.accept(file)
    return ""


@app.route("/report/edit", methods=["GET"])
def edit():
    with open("static/edit.html") as file:
        edit_page = file.read()

    file_name = request.args.get("file")
    file_name = "_data/OEC/" + file_name
    with open(file_name, encoding="utf8") as file:
        file_content = file.read()

    return edit_page.replace("{{ file }}", file_content.replace("\n", "\\n"))


@app.route("/report/edit/save", methods=["POST"])
def save():
    content = request.get_data()

    file_name = request.args.get("file")
    with open("_data/OEC/" + file_name, "wb") as file:
        file.write(content)

    return ""


@app.route("/report/pull-request", methods=["GET"])
def pull_request():
    token = request.args.get("token")
    gh = login(token=token)
    user = gh.user()
    email = user.email

    with open("static/pull-request.html") as pull_request_file:
        pull_request_page = pull_request_file.read()

    pr_url = main.create_pull_request(token)

    with open("_data/accepted/pr", "w") as file:
        file.write(pr_url)

    email = "" if not email else email
    if email:
        email_button = ('''<div id="email-button"><a href="javascript:sendEmail('{{ email }}')">'''
                        + '''<i class="fa fa-envelope-o right-margin"></i>Send email receipt</a></div><br>''')
    else:
        email_button = ('<div id="email-button" class="greyout" title="Your GitHub account does not have a public '
                        + 'email."><i class="fa fa-envelope-o right-margin"></i>Send email receipt</div><br>')

    return pull_request_page.replace("{{ email_button }}", email_button).replace("{{ name }}", user.name)\
        .replace("{{ login }}", user.login).replace("{{ email }}", email).replace("{{ token }}", token)\
        .replace("{{ pr_url }}", pr_url)


@app.route("/report/email", methods=["GET"])
def send_email():
    token = request.args.get("token")

    file_list = glob.glob("_data/accepted/*.xml")
    for i in range(len(file_list)):
        file_list[i] = file_list[i].split("/")[-1]

    with open("_data/accepted/pr", "r") as file:
        pr_number = file.read()

    main.send_email(token, file_list, pr_number)
    return ""


if __name__ == "__main__":
    app.run(debug=True)
