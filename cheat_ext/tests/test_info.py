from mock import patch, call
from tempfile import mkdtemp
import os
import unittest

from cheat_ext.exceptions import CheatExtException
from cheat_ext.info import info


class TestInfo(unittest.TestCase):
    def setUp(self):
        self.sheet_dir = os.path.join(mkdtemp(), "autor_repo")
        os.mkdir(self.sheet_dir)

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
            info("autor/repo")

    @patch("sys.stdout")
    def test_info_no_sheets(self, stdout):
        info("autor/repo")

        stdout.write.assert_has_calls([
            call("no sheet found at autor/repo"),
            call("\n"),
        ])
