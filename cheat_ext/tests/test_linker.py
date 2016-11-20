from mock import patch
import os
import shutil
from tempfile import mkdtemp
import unittest

from cheat_ext.exceptions import CheatExtException
from cheat_ext.linker import link, unlink


class TestLinker(unittest.TestCase):
    def setUp(self):
        tmp_dir = mkdtemp()
        self.cheat_dir = os.path.join(tmp_dir, ".cheat")
        self.sheet_dir = os.path.join(
            self.cheat_dir, "cheat-ext", "author_repo")
        os.makedirs(self.sheet_dir)

        self.get_cheat_path = patch("cheat_ext.linker.get_cheat_path").start()
        self.get_cheat_path.return_value = self.cheat_dir

        self.get_sheet_path = patch("cheat_ext.linker.get_sheet_path").start()
        self.get_sheet_path.return_value = self.sheet_dir

    def _make_unlink_sheets(self, sheets):
        for sheet in sheets:
            open(os.path.join(self.sheet_dir, sheet), "w").close()

    def _make_link_sheets(self, sheets):
        for sheet in sheets:
            os.symlink(
                os.path.join(self.sheet_dir, sheet),
                os.path.join(self.cheat_dir, sheet))

    def test_link(self):
        sheets = ["openssl", "curl", "top"]
        self._make_unlink_sheets(sheets)

        link("author/repo")

        for sheet in sheets:
            cheat_link = os.path.join(self.cheat_dir, sheet)
            self.assertTrue(os.path.islink(cheat_link))
            self.assertEqual(
                os.readlink(cheat_link),
                os.path.join(self.sheet_dir, sheet))

    def test_link_exclude_files(self):
        sheets = [".git", "test.py"]
        self._make_unlink_sheets(sheets)

        link("author/repo")

        for sheet in sheets:
            self.assertFalse(os.path.exists(os.path.join(self.cheat_dir, sheet)))

    def test_link_exclude_dir(self):
        os.mkdir(os.path.join(self.sheet_dir, "src"))

        link("author/repo")

        self.assertFalse(os.path.exists(os.path.join(self.cheat_dir, "src")))

    def test_link_failed_when_uninstalled(self):
        shutil.rmtree(self.sheet_dir)

        with self.assertRaises(CheatExtException):
            link("author/repo")

    def test_link_with_linked(self):
        sheets = ["openssl", "top"]
        exist_file = "curl"

        self._make_unlink_sheets(sheets + [exist_file])
        open(os.path.join(self.cheat_dir, exist_file), "w").close()

        with self.assertRaises(CheatExtException):
            link("author/repo")

        for sheet in sheets:
            self.assertFalse(os.path.exists(os.path.join(self.cheat_dir, sheet)))

    def test_unlink(self):
        sheets = ["openssl", "curl", "top"]

        self._make_unlink_sheets(sheets)
        self._make_link_sheets(sheets)

        unlink("author/repo")

        for sheet in sheets:
            self.assertFalse(os.path.exists(os.path.join(self.cheat_dir, sheet)))

    def test_unlin_failed_when_uninstalled(self):
        shutil.rmtree(self.sheet_dir)

        with self.assertRaises(CheatExtException):
            unlink("author/repo")
