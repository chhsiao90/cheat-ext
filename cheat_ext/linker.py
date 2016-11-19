from __future__ import print_function
import re
import sys
import os

from .exceptions import CheatExtException
from .utils import get_cheat_path, get_sheet_path


_STATE_UNLINK = "unlink"
_STATE_CONFLICT = "conflict"
_STATE_LINKED = "linked"


def link(repo):
    cheat_dir = get_cheat_path()
    sheet_dir = get_sheet_path(repo)
    if not os.path.isdir(sheet_dir):
        raise CheatExtException(
            "%s hadn't been installed yet at %s" % (repo, sheet_dir))

    sheets = _available_sheets(sheet_dir)
    state_sheets = _state_sheets(cheat_dir, sheet_dir, sheets)

    _check_sheets_availability(state_sheets)

    for sheet, _ in filter(_sheets_with_state(_STATE_UNLINK), state_sheets):
        os.symlink(
            os.path.join(sheet_dir, sheet),
            os.path.join(cheat_dir, sheet))


def unlink(repo):
    cheat_dir = get_cheat_path()
    sheet_dir = get_sheet_path(repo)
    if not os.path.isdir(sheet_dir):
        raise CheatExtException(
            "%s hadn't been installed yet at %s" % (repo, sheet_dir))

    sheets = _available_sheets(sheet_dir)
    state_sheets = _state_sheets(cheat_dir, sheet_dir, sheets)

    _check_sheets_availability(state_sheets)

    for sheet, _ in filter(_sheets_with_state(_STATE_LINKED), state_sheets):
        os.unlink(os.path.join(cheat_dir, sheet))
        print("%s is unlinked" % sheet)


def _available_sheets(sheet_dir):
    def is_sheet(f):
        return (
            not os.path.isdir(os.path.join(sheet_dir, f)) and
            re.match(r"^[a-zA-Z-_]+$", f))
    return list(filter(is_sheet, os.listdir(sheet_dir)))


def _state_sheets(cheat_dir, sheet_dir, sheets):
    def sheet_with_state(sheet):
        cheat_path = os.path.join(cheat_dir, sheet)
        if not os.path.exists(cheat_path):
            return (sheet, _STATE_UNLINK)
        elif (os.path.islink(cheat_path) and
              os.readlink(cheat_path) == os.path.join(sheet_dir, sheet)):
            return (sheet, _STATE_LINKED)
        else:
            return (sheet, _STATE_CONFLICT)
    return list(map(sheet_with_state, sheets))


def _check_sheets_availability(state_sheets):
    error_sheets = list(filter(_sheets_with_state(_STATE_CONFLICT), state_sheets))
    if error_sheets:
        for error_sheet, _ in error_sheets:
            print("%s had been defined" % error_sheet, file=sys.stderr)
        raise CheatExtException


def _sheets_with_state(state):
    def filter_by_state(state_sheet):
        _, sheet_state = state_sheet
        return sheet_state == state
    return filter_by_state
