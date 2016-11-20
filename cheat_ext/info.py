from __future__ import print_function
import os

from .exceptions import CheatExtException
from .utils import get_sheet_path, get_available_sheets_at


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
