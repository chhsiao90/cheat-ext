from mock import patch
import os
import shutil
from tempfile import mkdtemp
import unittest

from cheat_ext.exceptions import CheatExtException
from cheat_ext.linker import link


class TestLinker(unittest.TestCase):
    def setUp(self):
        tmp_dir = mkdtemp()
        self.cheat_dir = os.path.join(tmp_dir, ".cheat")
        self.repo_dir = os.path.join(
            self.cheat_dir, "cheat-ext", "author_repo")
        os.makedirs(self.repo_dir)

        self.get_cheat_path = patch("cheat_ext.linker.get_cheat_path").start()
        self.get_cheat_path.return_value = self.cheat_dir

        self.get_sheet_path = patch("cheat_ext.linker.get_sheet_path").start()
        self.get_sheet_path.return_value = self.repo_dir

    def test_link(self):
        files = ["openssl", "curl", "top"]
        for f in files:
            open(os.path.join(self.repo_dir, f), "w").close()

        link("author/repo")

        for f in files:
            cheat_link = os.path.join(self.cheat_dir, f)
            self.assertTrue(os.path.islink(cheat_link))
            self.assertEqual(
                os.readlink(cheat_link),
                os.path.join(self.repo_dir, f))

        self.get_cheat_path.assert_called_with()
        self.get_sheet_path.assert_called_with("author/repo")

    def test_link_exclude_files(self):
        files = [".git", "test.py"]
        for f in files:
            open(os.path.join(self.repo_dir, f), "w").close()

        link("author/repo")

        for f in files:
            self.assertFalse(os.path.exists(os.path.join(self.cheat_dir, f)))

    def test_link_exclude_dir(self):
        os.mkdir(os.path.join(self.repo_dir, "src"))

        link("author/repo")

        self.assertFalse(os.path.exists(os.path.join(self.cheat_dir, "src")))

    def test_link_failed_when_uninstalled(self):
        shutil.rmtree(self.repo_dir)

        with self.assertRaises(CheatExtException):
            link("author/repo")
