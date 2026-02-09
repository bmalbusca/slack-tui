import unittest
from unittest import mock

from utils.key_reader import read_key

class TestKeyReader(unittest.TestCase):
    def test_requires_tty(self):
        with mock.patch("sys.stdin.isatty", return_value=False):
            with self.assertRaises(RuntimeError):
                read_key()

if __name__ == "__main__":
    unittest.main()
