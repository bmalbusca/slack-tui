"""Configuration management for Slack TUI."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from platformdirs import user_config_dir


class Settings:
    """Application settings.

    Token resolution precedence:
      1) CLI argument (handled by caller)
      2) environment variable SLACK_TOKEN (preferred) or SLACK_TUI_TOKEN (legacy)
      3) saved config file
    """

    APP_NAME = "slack-tui-app"

    def __init__(self, config_dir: Optional[Path] = None):
        # New, OS-appropriate config directory
        self.config_dir = Path(config_dir) if config_dir else Path(user_config_dir(self.APP_NAME))
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Legacy path (~/.config/slack-tui-app) migration (best-effort)
        legacy_dir = Path.home() / ".config" / self.APP_NAME
        if legacy_dir.exists() and legacy_dir.is_dir():
            for fname in ("tokens.json", "vip_users.json", "settings.json"):
                src = legacy_dir / fname
                dst = self.config_dir / fname
                if src.exists() and not dst.exists():
                    try:
                        dst.write_bytes(src.read_bytes())
                    except Exception:
                        pass

        self.token_file = self.config_dir / "tokens.json"
        self.vip_file = self.config_dir / "vip_users.json"
        self.settings_file = self.config_dir / "settings.json"

        self._load()

    def _load(self):
        """Load configuration."""
        self.tokens = self._load_json(self.token_file, {})
        self.vip_users = self._load_json(self.vip_file, [])
        self.settings = self._load_json(
            self.settings_file,
            {
                "compact_mode": True,
                "messages_per_page": 20,
                "default_types": "public_channel",
            },
        )

    def _load_json(self, path: Path, default):
        """Load JSON file."""
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                return default
        return default

    def _save_json(self, path: Path, data):
        """Save JSON file."""
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        if path == self.token_file:
            # Best-effort secure permissions; Windows may ignore chmod
            try:
                path.chmod(0o600)
            except Exception:
                pass

    def get_token_from_env(self) -> Optional[str]:
        """Get token from environment variables."""
        return os.environ.get("SLACK_TOKEN") or os.environ.get("SLACK_TUI_TOKEN")

    def get_token(self) -> Optional[str]:
        """Get stored token (env preferred)."""
        token = self.get_token_from_env()
        if token:
            return token
        return self.tokens.get("token")

    def save_token(self, token: str):
        """Save token."""
        self.tokens["token"] = token
        self._save_json(self.token_file, self.tokens)

    def get_default_types(self) -> str:
        return self.settings.get("default_types", "public_channel")

    def set_default_types(self, types: str):
        self.settings["default_types"] = types
        self._save_json(self.settings_file, self.settings)

    def get_vip_users(self):
        """Get VIP users list."""
        return self.vip_users

    def add_vip_user(self, user_id: str, username: str):
        """Add VIP user."""
        user = {"id": user_id, "username": username}
        if user not in self.vip_users:
            self.vip_users.append(user)
            self._save_json(self.vip_file, self.vip_users)

    def remove_vip_user(self, user_id: str):
        """Remove VIP user."""
        self.vip_users = [u for u in self.vip_users if u["id"] != user_id]
        self._save_json(self.vip_file, self.vip_users)

    def is_vip(self, user_id: str) -> bool:
        """Check if user is VIP."""
        return any(u["id"] == user_id for u in self.vip_users)



from datetime import datetime, timezone

def get_tokens(self) -> dict:
    return self.tokens or {}

def save_tokens(
    self,
    *,
    access_token: str,
    refresh_token: str | None = None,
    expires_at: str | None = None,
    token_type: str | None = None,
):
    self.tokens.update({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_at": expires_at,
        "token_type": token_type,
    })
    self._save_json(self.token_file, self.tokens)

def get_access_token(self) -> str | None:
    import os
    return os.environ.get("SLACK_TOKEN") or self.tokens.get("access_token")

def get_refresh_token(self) -> str | None:
    return self.tokens.get("refresh_token")

def token_expired(self) -> bool:
    exp = self.tokens.get("expires_at")
    if not exp:
        return False
    try:
        return datetime.now(timezone.utc) >= datetime.fromisoformat(exp)
    except Exception:
        return False
