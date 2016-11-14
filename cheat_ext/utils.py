import os


_GITHUB_URL = "https://github.com"


def get_github_url(repo):
    return _GITHUB_URL + "/" + repo + ".git"


def get_sheet_path(repo):
    return os.path.join(
        os.path.expanduser("~"),
        ".cheat",
        repo.replace("/", "_"))


def get_cheat_path():
    return os.path.join(
        os.path.expanduser("~"),
        ".cheat")
