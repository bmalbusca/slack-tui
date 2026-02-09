import os
import json
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from config.settings import Settings

class TestTokenResolution(unittest.TestCase):
    def test_env_overrides_file(self):
        with TemporaryDirectory() as td:
            cfg = Path(td)
            s = Settings(config_dir=cfg)
            # write file token
            (cfg / "tokens.json").write_text(json.dumps({"token": "file-token"}))
            s._load()
            os.environ["SLACK_TOKEN"] = "env-token"
            try:
                self.assertEqual(s.get_token(), "env-token")
            finally:
                os.environ.pop("SLACK_TOKEN", None)

    def test_file_used_when_no_env(self):
        with TemporaryDirectory() as td:
            cfg = Path(td)
            s = Settings(config_dir=cfg)
            (cfg / "tokens.json").write_text(json.dumps({"token": "file-token"}))
            s._load()
            self.assertEqual(s.get_token(), "file-token")

if __name__ == "__main__":
    unittest.main()
