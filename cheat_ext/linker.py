from __future__ import print_function
import sys
import os

from .exceptions import CheatExtException
from .utils import (
    STATE_UNLINK, STATE_LINKED, STATE_CONFLICT,
    get_cheat_path, get_sheet_path, get_available_sheets_at,
    get_sheets_with_state, filter_by_state,
)


def link(repo):
    cheat_dir = get_cheat_path()
    sheet_dir = get_sheet_path(repo)
    if not os.path.isdir(sheet_dir):
        raise CheatExtException(
            "%s hadn't been installed yet at %s" % (repo, sheet_dir))

    sheets = get_available_sheets_at(sheet_dir)
    state_sheets = get_sheets_with_state(cheat_dir, sheet_dir, sheets)

    _check_sheets_availability(state_sheets)

    for sheet, _ in filter_by_state(STATE_UNLINK, state_sheets):
        os.symlink(
            os.path.join(sheet_dir, sheet),
            os.path.join(cheat_dir, sheet))


def unlink(repo):
    cheat_dir = get_cheat_path()
    sheet_dir = get_sheet_path(repo)
    if not os.path.isdir(sheet_dir):
        raise CheatExtException(
            "%s hadn't been installed yet at %s" % (repo, sheet_dir))

    sheets = get_available_sheets_at(sheet_dir)
    state_sheets = get_sheets_with_state(cheat_dir, sheet_dir, sheets)

    _check_sheets_availability(state_sheets)

    for sheet, _ in filter_by_state(STATE_LINKED, state_sheets):
        os.unlink(os.path.join(cheat_dir, sheet))
        print("%s is unlinked" % sheet)


def _check_sheets_availability(state_sheets):
    error_sheets = list(filter_by_state(STATE_CONFLICT, state_sheets))
    if error_sheets:
        for error_sheet, _ in error_sheets:
            print("%s had been defined" % error_sheet, file=sys.stderr)
        raise CheatExtException
