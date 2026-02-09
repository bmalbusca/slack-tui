"""Slack authentication with error handling."""
from typing import Optional, Tuple
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class AuthError(Exception):
    """Authentication error."""
    pass


class SlackAuth:
    """Handles Slack authentication."""
    
    # Supported token types and their prefixes
    SUPPORTED_TOKEN_TYPES = {
        'xoxp-': 'User OAuth Token',
        'xoxb-': 'Bot User OAuth Token',
        'xoxe.xoxp-': 'App Bot Access Token',
        'xoxe-': 'App Bot Refresh Token',
        'xapp-': 'App-Level Token'
    }
    
    def __init__(self, settings):
        self.settings = settings
        self.client: Optional[WebClient] = None
        self.user_id: Optional[str] = None
        self.team_id: Optional[str] = None
        self.team_name: Optional[str] = None
        self.token_type: Optional[str] = None
    
    def _detect_token_type(self, token: str) -> Optional[str]:
        """Detect the type of Slack token."""
        for prefix, token_type in self.SUPPORTED_TOKEN_TYPES.items():
            if token.startswith(prefix):
                return token_type
        return None
    
    async def authenticate(self, token: Optional[str] = None) -> Tuple[bool, str]:
        """
        Authenticate with Slack.
        
        Supports all Slack token types:
        - xoxp-* (User OAuth Token)
        - xoxb-* (Bot User OAuth Token)
        - xoxe.xoxp-* (Enterprise User Token)
        - xoxe-* (Enterprise Token)
        - xapp-* (App-Level Token)
        
        Args:
            token: Slack token. If None, loads from config.
        
        Returns:
            (success, message) tuple
        """
        # Get token from arg, env, or file
        auth_token = token or self.settings.get_token()
        
        if not auth_token:
            raise AuthError(
                "No Slack token found.\n\n"
                "Provide token using one of these methods:\n"
                "1. Command line: python slack-tui.py --token xoxp-your-token\n"
                "2. Environment variable: export SLACK_TUI_TOKEN=xoxp-your-token\n"
                "3. Stored in config after first use\n\n"
                "Supported token types:\n"
                "  • xoxp-*        User OAuth Token (recommended)\n"
                "  • xoxb-*        Bot User OAuth Token\n"
                "  • xoxe.xoxp-*   App Bot Access Token\n"
                "  • xoxe-*        App Bot Refresh Token\n"
                "  • xapp-*        App-Level Token\n\n"
                "Get token from: https://api.slack.com/apps\n"
                "- Create app → OAuth & Permissions\n"
                "- Install to workspace\n"
                "- Copy token (User or Bot OAuth Token)"
            )
        
        # Detect and validate token type
        self.token_type = self._detect_token_type(auth_token)
        
        if not self.token_type:
            # Try to provide helpful error based on token format
            if auth_token.startswith("xox"):
                raise AuthError(
                    f"Unrecognized token format: {auth_token[:10]}...\n\n"
                    "Supported token formats:\n"
                    "  • xoxp-*        User OAuth Token\n"
                    "  • xoxb-*        Bot User OAuth Token\n"
                    "  • xoxe.xoxp-*   App Bot Access Token\n"
                    "  • xoxe-*        App Bot Refresh Token\n"
                    "  • xapp-*        App-Level Token\n\n"
                    "Please check your token at:\n"
                    "https://api.slack.com/apps → Your App → OAuth & Permissions"
                )
            else:
                raise AuthError(
                    "Invalid token format.\n\n"
                    "Token should start with 'xox' followed by type identifier.\n"
                    "Example: xoxp-123456789012-123456789012-...\n\n"
                    "Get token from:\n"
                    "https://api.slack.com/apps → Your App → OAuth & Permissions"
                )
        
        # Initialize client
        self.client = WebClient(token=auth_token)
        
        try:
            # Test authentication
            response = self.client.auth_test()
            
            # Extract authentication info
            self.user_id = response.get("user_id")
            self.team_id = response.get("team_id")
            self.team_name = response.get("team", "Unknown Team")
            
            # For bot tokens, user_id might be bot_id
            if not self.user_id and "bot_id" in response:
                self.user_id = response["bot_id"]
            
            # Save token for future use
            self.settings.save_token(auth_token)
            
            # Build success message based on token type
            user_display = response.get("user", response.get("bot_id", "Unknown"))
            
            success_msg = f"Authenticated as {user_display} on {self.team_name}"
            if self.token_type:
                success_msg += f"\nToken type: {self.token_type}"
            
            return True, success_msg
            
        except SlackApiError as e:
            error_code = e.response["error"]
            
            if error_code == "invalid_auth":
                raise AuthError(
                    "Invalid authentication token.\n\n"
                    "Your token may be:\n"
                    "• Expired or revoked\n"
                    "• From different workspace\n"
                    "• Incorrectly copied (missing characters)\n\n"
                    f"Token type detected: {self.token_type or 'Unknown'}\n\n"
                    "Get new token from:\n"
                    "https://api.slack.com/apps → Your App → OAuth & Permissions"
                )
            elif error_code == "token_revoked":
                raise AuthError(
                    "Token has been revoked.\n\n"
                    "Generate new token:\n"
                    "1. Go to https://api.slack.com/apps\n"
                    "2. Select your app\n"
                    "3. OAuth & Permissions → Reinstall to Workspace\n"
                    "4. Copy new token (User or Bot OAuth Token)"
                )
            elif error_code == "not_authed":
                raise AuthError(
                    "Authentication required.\n\n"
                    "No valid token provided or token is empty.\n"
                    "Please provide a valid Slack token."
                )
            elif error_code == "account_inactive":
                raise AuthError(
                    "Account is inactive.\n\n"
                    "Please check:\n"
                    "• Your workspace membership status\n"
                    "• Whether your account has been deactivated\n"
                    "• Contact your workspace admin if needed"
                )
            else:
                raise AuthError(
                    f"Slack API error: {error_code}\n\n"
                    f"Token type: {self.token_type or 'Unknown'}\n\n"
                    f"For help, visit: https://api.slack.com/methods/auth.test"
                )
        
        except Exception as e:
            raise AuthError(
                f"Authentication error: {str(e)}\n\n"
                "Please check:\n"
                "• Internet connection\n"
                "• Token format and validity\n"
                "• Slack service status: https://status.slack.com\n\n"
                f"Token type: {self.token_type or 'Unknown'}"
            )
    
    def get_client(self) -> WebClient:
        """Get authenticated Slack client."""
        if not self.client:
            raise AuthError("Not authenticated. Call authenticate() first.")
        return self.client
    
    def is_authenticated(self) -> bool:
        """Check if authenticated."""
        return self.client is not None
