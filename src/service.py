#!flask/bin/python
import re
import requests
import main
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
    dashboard_file = open("static/dashboard.html")
    dashboard_page = dashboard_file.read()
    dashboard_file.close()
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

    report_file = open("static/report.html")
    report_page = report_file.read()
    report_file.close()

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
            icon_status = '<i class="fa fa-ellipsis-h" title="' + status + '"></i>'
        else:
            icon_status = '<i class="fa fa-plus" title="' + status + '"></i>'
        icon_compare = '''<a href="javascript:window.open('/report/compare?file=''' + name + '''');"><i class="fa fa-search"></i></a>'''
        icon_edit = '''<a href="javascript:window.open('/report/edit?file=''' + name + '''');"><i class="fa fa-pencil"></i></a>'''
        icon_accept = '''<td id="''' + str(count) + '''"><a href="javascript:accept(''' + "'" + next_file[0] + "'," + str(count) + ''');"><i class="fa fa-check right-margin"></i>Accept</a></td>'''
        html += template.replace("{{ filename }}", name).replace("{{ status }}", icon_status).replace("{{ compare }}", icon_compare).replace("{{ edit }}", icon_edit).replace("{{ operation }}", icon_accept)
        count += 1

    return report_page.replace("{{ name }}", user.name).replace("{{ login }}", user.login).replace("{{ token }}", token).replace("{{ report }}", html)


@app.route("/report/compare", methods=["GET"])
def compare():
    compare_file = open("static/compare.html")
    compare_page = compare_file.read()
    compare_file.close()

    file = request.args.get("file")
    file = "_data/OEC/" + file

    try:
        file_old = open(file.replace("_data/OEC/", "_data/OEC_old/"))
        file_new = open(file)
        content_old = file_old.read()
        content_new = file_new.read()
        file_old.close()
        file_new.close()
        compare_page = compare_page.replace("{{ old }}", content_old.replace("<", "&lt;").replace(">", "&gt;"))
        compare_page = compare_page.replace("{{ new }}", content_new.replace("<", "&lt;").replace(">", "&gt;"))
    except FileNotFoundError:
        file_new = open(file)
        content_new = file_new.read()
        file_new.close()
        compare_page = compare_page.replace("{{ new }}", content_new.replace("<", "&lt;").replace(">", "&gt;"))

    return compare_page


@app.route("/report/accept", methods=["GET"])
def accept():
    return ""


@app.route("/report/edit", methods=["GET"])
def edit():
    file = open("static/edit.html")
    edit_page = file.read()
    file.close()

    file_name = request.args.get("file")
    file_name = "_data/OEC/" + file_name
    file = open(file_name)
    file_content = file.read()
    file.close()

    return edit_page.replace("{{ file }}", file_content.replace("\n", "\\n"))


if __name__ == "__main__":
    app.run(debug=True)
