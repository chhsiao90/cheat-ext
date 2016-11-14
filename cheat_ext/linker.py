from __future__ import print_function
import re
import sys
import os

from .exceptions import CheatExtException
from .utils import get_cheat_path, get_sheet_path


def link(repo):
    cheat_dir = get_cheat_path()
    sheet_dir = get_sheet_path(repo)
    if not os.path.isdir(sheet_dir):
        raise CheatExtException(
            "%s hadn't been installed yet at %s" % (repo, sheet_dir))

    sheets = _available_sheets(sheet_dir)
    _check_sheets_availability(cheat_dir, sheets)
    for sheet in sheets:
        os.symlink(
            os.path.join(sheet_dir, sheet),
            os.path.join(cheat_dir, sheet))


def _available_sheets(sheet_dir):
    def is_sheet(f):
        return (
            not os.path.isdir(os.path.join(sheet_dir, f)) and
            re.match(r"^[a-zA-Z-_]+$", f))
    return list(filter(is_sheet, os.listdir(sheet_dir)))


def _check_sheets_availability(cheat_dir, sheets):
    def is_sheet_exists(sheet):
        return os.path.exists(os.path.join(cheat_dir, sheet))
    error_sheets = filter(is_sheet_exists, sheets)
    if error_sheets:
        for error_sheet in error_sheets:
            print("%s had been defined" % error_sheet, file=sys.stderr)
        raise CheatExtException
