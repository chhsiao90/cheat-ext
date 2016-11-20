from __future__ import print_function

from git import Repo
from git.exc import InvalidGitRepositoryError
import shutil
import os

from .exceptions import CheatExtException
from .utils import get_github_url, get_sheet_path


def install(repo):
    sheet_dir = get_sheet_path(repo)
    if os.path.exists(sheet_dir):
        raise CheatExtException(
            "%s had been installed at %s" % (repo, sheet_dir))

    github_url = get_github_url(repo)
    Repo.clone_from(github_url, sheet_dir, branch="master")
    print("%s is installed successfully" % repo)


def upgrade(repo):
    sheet_dir = get_sheet_path(repo)
    if not os.path.isdir(sheet_dir):
        raise CheatExtException(
            "%s hadn't been installed yet at %s" % (repo, sheet_dir))

    try:
        git_repo = Repo(sheet_dir)
    except InvalidGitRepositoryError:
        raise CheatExtException("Not a git directory at %s" % sheet_dir)
    else:
        git_repo.remote().pull()
        print("%s is upgraded successfully" % repo)


def remove(repo):
    sheet_dir = get_sheet_path(repo)
    if not os.path.isdir(sheet_dir):
        raise CheatExtException(
            "%s hadn't been installed yet at %s" % (repo, sheet_dir))

    shutil.rmtree(sheet_dir)
    print("%s is removed successfully" % repo)
