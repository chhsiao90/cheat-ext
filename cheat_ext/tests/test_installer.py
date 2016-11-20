from git.exc import InvalidGitRepositoryError
from mock import patch
import os
from tempfile import mkdtemp
import unittest

from cheat_ext.exceptions import CheatExtException
from cheat_ext.installer import (
    install, upgrade, remove,
)


class TestInstaller(unittest.TestCase):
    def setUp(self):
        self.sheet_dir = os.path.join(mkdtemp(), "autor_repo")

        self.get_sheet_path = \
            patch("cheat_ext.installer.get_sheet_path").start()
        self.get_sheet_path.return_value = self.sheet_dir

        self.Repo = patch("cheat_ext.installer.Repo").start()

    def test_install(self):
        install("author/repo")

        self.get_sheet_path.assert_called_with("author/repo")
        self.Repo.clone_from.assert_called_with(
            "https://github.com/author/repo.git", self.sheet_dir,
            branch="master")

    def test_install_cheatsheets_installed(self):
        os.mkdir(self.sheet_dir)

        with self.assertRaises(CheatExtException):
            install("author/repo")

        self.get_sheet_path.assert_called_with("author/repo")
        self.Repo.clone_from.assert_not_called()

    def test_upgrade(self):
        os.mkdir(self.sheet_dir)

        upgrade("author/repo")

        self.get_sheet_path.assert_called_with("author/repo")
        self.Repo.assert_called_with(self.sheet_dir)
        self.Repo(self.sheet_dir).remote().pull.assert_called_with()

    def test_upgrade_failed_with_not_installed(self):
        with self.assertRaises(CheatExtException):
            upgrade("author/repo")

        self.get_sheet_path.assert_called_with("author/repo")
        self.Repo.asesrt_not_called()

    def test_upgrade_failed_with_not_git_dir(self):
        self.Repo.side_effect = InvalidGitRepositoryError
        os.mkdir(self.sheet_dir)

        with self.assertRaises(CheatExtException):
            upgrade("author/repo")

        self.get_sheet_path.assert_called_with("author/repo")
        self.Repo.asesrt_not_called()

    def test_remove(self):
        os.mkdir(self.sheet_dir)

        remove("author/repo")

        self.get_sheet_path.assert_called_with("author/repo")
        self.assertFalse(os.path.exists(self.sheet_dir))

    def test_remove_failed_with_not_installed(self):
        with self.assertRaises(CheatExtException):
            remove("author/repo")

        self.get_sheet_path.assert_called_with("author/repo")
