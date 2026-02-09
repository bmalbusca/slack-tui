"""Configuration management for Slack TUI."""
import json
import os
from pathlib import Path
from typing import Optional


class Settings:
    """Application settings."""
    
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'slack-tui-app'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.token_file = self.config_dir / 'tokens.json'
        self.vip_file = self.config_dir / 'vip_users.json'
        self.settings_file = self.config_dir / 'settings.json'
        
        self._load()
    
    def _load(self):
        """Load configuration."""
        self.tokens = self._load_json(self.token_file, {})
        self.vip_users = self._load_json(self.vip_file, [])
        self.settings = self._load_json(self.settings_file, {
            'compact_mode': True,
            'messages_per_page': 20
        })
    
    def _load_json(self, path, default):
        """Load JSON file."""
        if path.exists():
            try:
                return json.loads(path.read_text())
            except:
                return default
        return default
    
    def _save_json(self, path, data):
        """Save JSON file."""
        path.write_text(json.dumps(data, indent=2))
        if path == self.token_file:
            try:
                path.chmod(0o600)  # Secure permissions
            except:
                pass  # Windows doesn't support chmod the same way
    
    def get_token(self) -> Optional[str]:
        """Get stored token."""
        # Check environment first
        token = os.environ.get('SLACK_TUI_TOKEN')
        if token:
            return token
        
        # Check file
        return self.tokens.get('user_token')
    
    def save_token(self, token: str):
        """Save token."""
        self.tokens['user_token'] = token
        self._save_json(self.token_file, self.tokens)
    
    def get_vip_users(self):
        """Get VIP users list."""
        return self.vip_users
    
    def add_vip_user(self, user_id: str, username: str):
        """Add VIP user."""
        user = {'id': user_id, 'username': username}
        if user not in self.vip_users:
            self.vip_users.append(user)
            self._save_json(self.vip_file, self.vip_users)
    
    def remove_vip_user(self, user_id: str):
        """Remove VIP user."""
        self.vip_users = [u for u in self.vip_users if u['id'] != user_id]
        self._save_json(self.vip_file, self.vip_users)
    
    def is_vip(self, user_id: str) -> bool:
        """Check if user is VIP."""
        return any(u['id'] == user_id for u in self.vip_users)
