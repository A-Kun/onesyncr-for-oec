import requests
import json
import github3
from github3 import login

GITHUB_API_BASE_URL = "https://api.github.com/repos/A-Kun/open_exoplanet_catalogue/contents/"

gh = login("A-Kun", token="67a91ee33e366d0576f2136c6e4d7c03e44ee6aa")
repo = gh.repository("A-Kun", "open_exoplanet_catalogue")
target_repo = gh.repository("OpenExoplanetCatalogue", "open_exoplanet_catalogue")

def push_file(path, title, content):
    try:
        repo.create_file(path, title, content.encode())
    except github3.models.GitHubError: # file already exists, update the file instead
        response = requests.get("https://api.github.com/repos/A-Kun/open_exoplanet_catalogue/contents/testfile.txt").content
        sha = json.loads(str(response)[2:-1])["sha"]
        repo.update_file(path, title, content.encode(), sha)

def create_pull_request(title):
    return target_repo.create_pull(title, "master", "A-Kun:master")


if __name__ == "__main__":
    # sample calls to functions
    push_file("testfile.txt", "Test commit", "This is a test file.")
    create_pull_request("Test PR (DO NOT MERGE)")
