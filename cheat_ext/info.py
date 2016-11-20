from __future__ import print_function

from git import Repo
from git.exc import InvalidGitRepositoryError
import os

from .exceptions import CheatExtException
from .utils import (
    get_ext_path, get_sheet_path, get_available_sheets_at
)


def ls():
    ext_dir = get_ext_path()

    if not os.path.isdir(ext_dir):
        print("there is no repository installed")
        return

    def is_git_dir(sheet):
        try:
            Repo(os.path.join(ext_dir, sheet))
            return True
        except InvalidGitRepositoryError:
            return False

    sheet_dirs = list(filter(is_git_dir, os.listdir(ext_dir)))
    sheet_dirs.sort()

    if sheet_dirs:
        print("installed repository:")
        for sheet in sheet_dirs:
            print(sheet.replace("_", "/"))
    else:
        print("there is no repository installed")


def info(repo):
    sheet_dir = get_sheet_path(repo)
    if not os.path.isdir(sheet_dir):
        raise CheatExtException(
            "%s hadn't been installed yet at %s" % (repo, sheet_dir))

    sheets = get_available_sheets_at(sheet_dir)
    if sheets:
        print("%d sheets found at %s" % (len(sheets), repo))
        for sheet in get_available_sheets_at(sheet_dir):
            print(sheet)
    else:
        print("no sheet found at %s" % repo)
