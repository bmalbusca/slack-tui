"""Slack authentication with error handling."""
from __future__ import annotations

from typing import Optional, Tuple

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config.settings import Settings


class AuthError(Exception):
    """Authentication error."""
    pass


class SlackAuth:
    """Handles Slack authentication.

    Notes on token types:
    - xoxb- / xoxp- tokens are Web API tokens and are typically what you need for
      conversations.*, chat.*, users.*, search.* calls.
    - xapp- is an app-level token used for Socket Mode and cannot call Web API methods.
    - xoxe.* tokens are short-lived enterprise tokens; this app does NOT implement OAuth refresh.
      If you use an expiring token, you'll need to refresh it outside this app.
    """

    SUPPORTED_PREFIXES = {
        "xoxp-": "User OAuth Token (Web API)",
        "xoxb-": "Bot User OAuth Token (Web API)",
        "xapp-": "App-Level Token (Socket Mode only; NOT Web API)",
        "xoxe.": "Enterprise token (often short-lived; Web API may be restricted)",
    }

    def __init__(self, settings: Settings):
        self.settings = settings
        self.client: Optional[WebClient] = None
        self.token_type: Optional[str] = None
        self.user_id: Optional[str] = None
        self.team_id: Optional[str] = None
        self.team_name: str = "Unknown Team"

    def _detect_token_type(self, token: str) -> Optional[str]:
        for prefix, label in self.SUPPORTED_PREFIXES.items():
            if token.startswith(prefix):
                return label
        return None

    async def authenticate(self, token: Optional[str] = None, *, save_token: bool = False) -> Tuple[bool, str]:
        """Authenticate with Slack.

        Token resolution precedence:
          1) token arg
          2) env var SLACK_TOKEN (preferred) / SLACK_TUI_TOKEN (legacy)
          3) config file

        If save_token is True and token is provided, persist it to config.
        """
        auth_token = token or self.settings.get_token()

        if not auth_token:
            raise AuthError(
                "No Slack token found.\n\n"
                "Provide a token using one of these methods:\n"
                "1) CLI:     python slack-tui.py --token xoxb-...\n"
                "2) ENV:     set SLACK_TOKEN=xoxb-... (Windows) / export SLACK_TOKEN=... (macOS/Linux)\n"
                "3) CONFIG:  saved token in the app config directory\n\n"
                "Recommended token types for this app: xoxb- (bot) or xoxp- (user), with the required scopes."
            )

        self.token_type = self._detect_token_type(auth_token) or "Unknown token type"
        self.client = WebClient(token=auth_token)

        try:
            resp = self.client.auth_test()
            self.user_id = resp.get("user_id") or resp.get("bot_id")
            self.team_id = resp.get("team_id")
            self.team_name = resp.get("team", "Unknown Team")

            if token and save_token:
                self.settings.save_token(auth_token)

            user_display = resp.get("user") or resp.get("bot_id") or "Unknown"
            return True, f"Connected to {self.team_name} as {user_display}"

        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            if error_code in ("invalid_auth", "not_authed", "token_revoked"):
                raise AuthError(
                    f"Slack authentication failed: {error_code}.\n\n"
                    f"Detected token type: {self.token_type}.\n"
                    "Get a Web API token (xoxb-/xoxp-) from your Slack app OAuth & Permissions page."
                )
            raise AuthError(f"Slack authentication failed: {error_code}")

    def get_client(self) -> WebClient:
        if not self.client:
            raise AuthError("Not authenticated")
        return self.client

    def get_token_type(self) -> str:
        return self.token_type or "Unknown"



def refresh_access_token(self) -> str:
    import os
    from datetime import datetime, timedelta, timezone
    from slack_sdk.errors import SlackApiError

    refresh_token = self.settings.get_refresh_token()
    if not refresh_token:
        raise AuthError("No refresh token stored. Use -r/--refresh-token first.")

    client_id = os.environ.get("SLACK_CLIENT_ID")
    client_secret = os.environ.get("SLACK_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise AuthError("SLACK_CLIENT_ID / SLACK_CLIENT_SECRET not set.")

    try:
        resp = self.client.api_call(
            "oauth.v2.access",
            http_verb="POST",
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": client_id,
                "client_secret": client_secret,
            },
        )
    except SlackApiError as e:
        raise AuthError(f"Token refresh failed: {e.response.get('error')}")

    access_token = resp.get("access_token") or resp.get("authed_user", {}).get("access_token")
    expires_in = resp.get("expires_in")

    if not access_token:
        raise AuthError("Refresh succeeded but no access token returned.")

    expires_at = None
    if expires_in:
        expires_at = (datetime.now(timezone.utc) + timedelta(seconds=int(expires_in))).isoformat()

    self.settings.save_tokens(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at,
        token_type="enterprise_oauth",
    )
    return access_token
