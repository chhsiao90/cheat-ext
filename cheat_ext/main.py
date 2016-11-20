import argparse

from cheat_ext.info import info, ls
from cheat_ext.installer import (
    install, upgrade, remove
)
from cheat_ext.linker import link, unlink


def _install(args):
    install(args.repository)
    link(args.repository)


def _upgrade(args):
    upgrade(args.repository)
    link(args.repository)


def _remove(args):
    unlink(args.repository)
    remove(args.repository)


def _info(args):
    info(args.repository)


def _ls(args):
    ls()


parser = argparse.ArgumentParser(description="cheat extension")

subparsers = parser.add_subparsers()

install_parser = subparsers.add_parser("install")
install_parser.add_argument("repository", type=str)
install_parser.set_defaults(func=_install)


upgrade_parser = subparsers.add_parser("upgrade")
upgrade_parser.add_argument("repository", type=str)
upgrade_parser.set_defaults(func=_upgrade)

remove_parser = subparsers.add_parser("remove")
remove_parser.add_argument("repository", type=str)
remove_parser.set_defaults(func=_remove)

info_parser = subparsers.add_parser("info")
info_parser.add_argument("repository", type=str)
info_parser.set_defaults(func=_info)

ls_parser = subparsers.add_parser("ls")
ls_parser.set_defaults(func=_ls)


def main():
    options = parser.parse_args()
    options.func(options)
