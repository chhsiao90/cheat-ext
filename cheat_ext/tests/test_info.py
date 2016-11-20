from git.exc import InvalidGitRepositoryError
from mock import patch, call
import shutil
from tempfile import mkdtemp
import os
import unittest

from cheat_ext.exceptions import CheatExtException
from cheat_ext.info import info, ls


class TestInfo(unittest.TestCase):
    def setUp(self):
        self.ext_dir = mkdtemp()
        self.sheet_dir = os.path.join(self.ext_dir, "author_repo")
        os.mkdir(self.sheet_dir)

        self.get_ext_path = \
            patch("cheat_ext.info.get_ext_path").start()
        self.get_ext_path.return_value = self.ext_dir

        self.get_sheet_path = \
            patch("cheat_ext.info.get_sheet_path").start()
        self.get_sheet_path.return_value = self.sheet_dir

    def _make_sheets(self, sheets):
        for sheet in sheets:
            open(os.path.join(self.sheet_dir, sheet), "w").close()

    @patch("sys.stdout")
    def test_info(self, stdout):
        sheets = ["curl", "openssl", "http"]
        self._make_sheets(sheets)

        info("author/repo")

        stdout.write.assert_has_calls([
            call("3 sheets found at author/repo"),
            call("\n"),
            call("curl"),
            call("\n"),
            call("http"),
            call("\n"),
            call("openssl"),
            call("\n"),
        ])

    def test_info_failed_when_uninstalled(self):
        os.rmdir(self.sheet_dir)

        with self.assertRaises(CheatExtException):
            info("author/repo")

    @patch("sys.stdout")
    def test_info_no_sheets(self, stdout):
        info("author/repo")

        stdout.write.assert_has_calls([
            call("no sheet found at author/repo"),
            call("\n"),
        ])

    @patch("cheat_ext.info.Repo")
    @patch("sys.stdout")
    def test_ls(self, stdout, Repo):
        os.mkdir(os.path.join(self.ext_dir, "author_cheats"))
        os.mkdir(os.path.join(self.ext_dir, "mike_repo"))

        ls()

        stdout.write.assert_has_calls([
            call("installed repository:"),
            call("\n"),
            call("author/cheats"),
            call("\n"),
            call("author/repo"),
            call("\n"),
            call("mike/repo"),
            call("\n"),
        ])
        Repo.assert_has_calls([
            call(os.path.join(self.ext_dir, "author_repo")),
            call(os.path.join(self.ext_dir, "author_cheats")),
            call(os.path.join(self.ext_dir, "mike_repo")),
        ], any_order=True)

    @patch("sys.stdout")
    def test_ls_no_ext_dir(self, stdout):
        shutil.rmtree(self.ext_dir)

        ls()

        stdout.write.assert_has_calls([
            call("there is no repository installed"),
            call("\n"),
        ])

    @patch("sys.stdout")
    def test_ls_no_sheet_dirs(self, stdout):
        os.rmdir(self.sheet_dir)

        ls()

        stdout.write.assert_has_calls([
            call("there is no repository installed"),
            call("\n"),
        ])

    @patch("cheat_ext.info.Repo")
    @patch("sys.stdout")
    def test_ls_with_not_git_dirs(self, stdout, Repo):
        def repo_side_effect(sheet):
            if sheet in (
                os.path.join(self.ext_dir, "author_failed1"),
                os.path.join(self.ext_dir, "author_failed2"),
            ):
                raise InvalidGitRepositoryError
        Repo.side_effect = repo_side_effect

        os.mkdir(os.path.join(self.ext_dir, "author_failed1"))
        os.mkdir(os.path.join(self.ext_dir, "author_failed2"))

        ls()

        stdout.write.assert_has_calls([
            call("installed repository:"),
            call("\n"),
            call("author/repo"),
            call("\n"),
        ])
        Repo.assert_has_calls([
            call(os.path.join(self.ext_dir, "author_repo")),
            call(os.path.join(self.ext_dir, "author_failed1")),
            call(os.path.join(self.ext_dir, "author_failed2")),
        ], any_order=True)
