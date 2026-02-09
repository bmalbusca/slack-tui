import unittest
from utils.types import normalize_types

class TestNormalizeTypes(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize_types(" public_channel , private_channel , public_channel "), "public_channel,private_channel")
        self.assertEqual(normalize_types(""), "public_channel")
        self.assertEqual(normalize_types("im,mpim"), "im,mpim")

if __name__ == "__main__":
    unittest.main()
