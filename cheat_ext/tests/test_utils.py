import os
import unittest

from cheat_ext.utils import get_github_url, get_sheet_path


class TestUtils(unittest.TestCase):
    def test_get_github_url(self):
        self.assertEqual(
            get_github_url("chhsiao90/cheat-ext"),
            "https://github.com/chhsiao90/cheat-ext.git")

    def test_get_sheet_path(self):
        self.assertEqual(
            get_sheet_path("chhsiao90/cheat-ext"),
            os.path.join(
                os.path.expanduser("~"),
                ".cheat", ".ext", "chhsiao90_cheat-ext"))
