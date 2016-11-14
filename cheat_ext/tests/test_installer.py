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
        self.sheet_dir = mkdtemp()
        self.repo_dir = os.path.join(self.sheet_dir, "author_repo")

        self.get_sheet_path = \
            patch("cheat_ext.installer.get_sheet_path").start()
        self.get_sheet_path.return_value = self.repo_dir

        self.Repo = patch("cheat_ext.installer.Repo").start()

    def test_install(self):
        install("author/repo")

        self.get_sheet_path.assert_called_with("author/repo")
        self.Repo.clone_from.assert_called_with(
            "https://github.com/author/repo.git", self.repo_dir,
            branch="master")

    def test_install_cheatsheets_installed(self):
        os.mkdir(self.repo_dir)

        with self.assertRaises(CheatExtException):
            install("author/repo")

        self.get_sheet_path.assert_called_with("author/repo")
        self.Repo.clone_from.assert_not_called()

    def test_upgrade(self):
        os.mkdir(self.repo_dir)

        upgrade("author/repo")

        self.get_sheet_path.assert_called_with("author/repo")
        self.Repo.assert_called_with(self.repo_dir)
        self.Repo(self.repo_dir).pull.assert_called_with()

    def test_upgrade_failed_with_not_installed(self):
        with self.assertRaises(CheatExtException):
            upgrade("author/repo")

        self.get_sheet_path.assert_called_with("author/repo")
        self.Repo.asesrt_not_called()

    def test_remove(self):
        os.mkdir(self.repo_dir)

        remove("author/repo")

        self.get_sheet_path.assert_called_with("author/repo")
        self.assertFalse(os.path.exists(self.repo_dir))

    def test_remove_failed_with_not_installed(self):
        with self.assertRaises(CheatExtException):
            remove("author/repo")

        self.get_sheet_path.assert_called_with("author/repo")
