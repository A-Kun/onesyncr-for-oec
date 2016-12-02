import requests
import json
import base64
import github3
from github3 import login


TARGET_USERNAME = "poppintk"
QUERY_STRING = "?client_id=56e49d113b3037c709a7&client_secret=aa2f85d97a29ad2c4791af0abd869a24a45eb970"


def push_file(path, commit_msg, content, token):
    try:
        gh = login(token=token)
        user = gh.user()
        repo = gh.repository(user.login, "open_exoplanet_catalogue")
        if not repo:
            target_repo = gh.repository(TARGET_USERNAME, "open_exoplanet_catalogue")
            target_repo.create_fork()
            repo = gh.repository(user.login, "open_exoplanet_catalogue")
        github_api_base_url = "https://api.github.com/repos/" + user.login + "/open_exoplanet_catalogue/contents/"
        try:  # file does not exist, create the file
            repo.create_file(path, commit_msg, content.encode())
            print("create", end=" ", flush=True)
            return True
        except github3.models.GitHubError:  # file already exists, update the file instead
            response = requests.get(github_api_base_url + path + QUERY_STRING).content
            sha = json.loads(response.decode())["sha"]
            remote_content = base64.b64decode(json.loads(response.decode())["content"].encode()).decode()
            if content != remote_content:
                repo.update_file(path, commit_msg, content.encode(), sha)
                print("modify", end=" ", flush=True)
                return False

            print("no change", end=" ", flush=True)
    except:
        pass


def create_pull_request(title, token):
    gh = login(token=token)
    user = gh.user()
    target_repo = gh.repository(TARGET_USERNAME, "open_exoplanet_catalogue")
    return target_repo.create_pull(title, "master", user.login + ":master")
