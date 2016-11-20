import re
import os


_GITHUB_URL = "https://github.com"

STATE_UNLINK = "unlink"
STATE_CONFLICT = "conflict"
STATE_LINKED = "linked"


def get_github_url(repo):
    return _GITHUB_URL + "/" + repo + ".git"


def get_cheat_path():
    return os.path.join(
        os.path.expanduser("~"),
        ".cheat")


def get_ext_path():
    return os.path.join(
        get_cheat_path(), ".ext")


def get_sheet_path(repo):
    return os.path.join(
        get_ext_path(),
        repo.replace("/", "_"))


def get_available_sheets_at(sheet_dir):
    def is_available_sheet(sheet):
        return (
            not os.path.isdir(os.path.join(sheet_dir, sheet)) and
            re.match(r"^[a-zA-Z-_]+$", sheet))
    sheets = list(filter(is_available_sheet, os.listdir(sheet_dir)))
    sheets.sort()
    return sheets


def get_sheets_with_state(cheat_dir, sheet_dir, sheets):
    def append_state(sheet):
        cheat_path = os.path.join(cheat_dir, sheet)
        if not os.path.exists(cheat_path):
            return (sheet, STATE_UNLINK)
        elif (os.path.islink(cheat_path) and
              os.readlink(cheat_path) == os.path.join(sheet_dir, sheet)):
            return (sheet, STATE_LINKED)
        else:
            return (sheet, STATE_CONFLICT)
    return list(map(append_state, sheets))


def filter_by_state(match, state_sheets):
    def filter_by_state_function(state_sheet):
        _, state = state_sheet
        return state == match
    return filter(filter_by_state_function, state_sheets)
