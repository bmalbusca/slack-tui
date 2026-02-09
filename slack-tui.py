#!/usr/bin/env python3
"""
Slack TUI - Main CLI Application
A focused terminal-based Slack client with VIP filtering and channel recap
"""
import argparse
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import Settings
from connectors.slack_auth import SlackAuth, AuthError
from messages.message_handler import MessageHandler, SlackPermissionError
from messages.vip_listener import VIPListener
from processors.autocomplete import fuzzy_match_channels, fuzzy_match_users, display_matches
from processors.recap import RecapManager
from utils.key_reader import read_key
from utils.types import normalize_types



class SlackTUI:
    """Main Slack TUI application."""
    
    def __init__(self):
        self.settings = Settings()
        self.auth = SlackAuth(self.settings)
        self.handler = None
        self.vip_listener = None
        self.recap_manager = None
        self.allowed_types = self.settings.get_default_types()
        self.debug = False

    def _print_permission_help(self, pe: SlackPermissionError) -> None:
        """Print actionable guidance for missing scopes / disallowed token types."""
        print("\n❌ Slack permission error", file=sys.stderr)
        print(f"- API method: {pe.method}", file=sys.stderr)
        print(f"- Error: {pe.error}", file=sys.stderr)

        if pe.needed:
            print(f"- Needed scopes: {pe.needed}", file=sys.stderr)
        if pe.provided:
            print(f"- Provided scopes: {pe.provided}", file=sys.stderr)

        # Practical next steps
        print("\nNext steps:", file=sys.stderr)
        print(f"1) Try minimal mode: --types public_channel (current: {self.allowed_types})", file=sys.stderr)
        print("2) Use a token that includes the required scopes (usually a bot token xoxb-… from a Slack app)", file=sys.stderr)
        print("3) If your workspace is locked down, share ADMIN_REQUEST.md with your Slack admins", file=sys.stderr)

        if pe.error == "not_allowed_token_type":
            print("\nTip: This token type is not permitted for this API method in your workspace.", file=sys.stderr)
            print("A bot token (xoxb-…) with explicit scopes is the most reliable option.", file=sys.stderr)

        print("\nSee PERMISSIONS.md for a command→scope matrix.", file=sys.stderr)
    
    async def authenticate(self, token=None, *, save_token: bool = False, types: str | None = None, debug: bool = False):
        """Authenticate with Slack."""
        try:
            self.debug = debug
            if types:
                self.allowed_types = normalize_types(types)
                self.settings.set_default_types(types)
            success, message = await self.auth.authenticate(token, save_token=save_token)
            if success:
                print(f"✓ {message}")
                self.handler = MessageHandler(self.auth.get_client())
                self.vip_listener = VIPListener(self.handler, self.settings)
                self.recap_manager = RecapManager(self.handler)
                # Capability probe: ensure we can list conversations for selected types
                try:
                    _ = self.handler.get_channels(types=self.allowed_types)
                except SlackPermissionError as pe:
                    self._print_permission_help(pe)
                    return False
                return True
            else:
                print(f"✗ {message}", file=sys.stderr)
                return False
        except AuthError as e:
            print(f"\n❌ Authentication Error:\n\n{e}\n", file=sys.stderr)
            print("For help with authentication, run: python slack-tui.py --help-auth")
            return False
    
    def send_message(self, channel, text, thread_ts=None):
        """Send a message to a channel."""
        if not self.handler:
            print("✗ Not authenticated", file=sys.stderr)
            return False
        
        channel_id = self.handler.resolve_channel(channel, types=self.allowed_types)
        if not channel_id:
            print(f"✗ Channel not found: {channel}", file=sys.stderr)
            return False
        
        try:
            result = self.handler.send_message(channel_id, text, thread_ts)
        except SlackPermissionError as pe:
            self._print_permission_help(pe)
            return False
        if result:
            print(f"✓ Message sent to {channel}")
            return True
        else:
            print(f"✗ Failed to send message", file=sys.stderr)
            return False
    
    def show_messages(self, channel, limit=20):
        """Show messages from a channel."""
        if not self.handler:
            print("✗ Not authenticated", file=sys.stderr)
            return
        
        channel_id = self.handler.resolve_channel(channel, types=self.allowed_types)
        if not channel_id:
            print(f"✗ Channel not found: {channel}", file=sys.stderr)
            return
        
        try:
            messages = self.handler.get_messages(channel_id, limit)
        except SlackPermissionError as pe:
            self._print_permission_help(pe)
            return
        
        print(f"\n{'='*60}")
        print(f"  Messages from {channel}")
        print(f"{'='*60}\n")
        
        for msg in reversed(messages):
            print(self.handler.format_message(msg, compact=True))
    
    def show_vip_messages(self):
        """Show VIP messages."""
        if not self.vip_listener:
            print("✗ Not authenticated", file=sys.stderr)
            return
        
        messages = self.vip_listener.get_vip_messages()
        
        print(f"\n{'='*60}")
        print(f"  VIP Messages ({len(messages)})")
        print(f"{'='*60}\n")
        
        if not messages:
            vip_users = self.settings.get_vip_users()
            if not vip_users:
                print("No VIP users configured.")
                print("\nAdd VIP users with: python slack-tui.py --vip-add @username")
            else:
                print("No recent VIP messages found.")
            return
        
        for msg in messages[:20]:
            print(self.vip_listener.format_vip_message(msg, compact=True))
    
    def show_channels(self):
        """List all channels."""
        if not self.handler:
            print("✗ Not authenticated", file=sys.stderr)
            return
        
        try:
            channels = self.handler.get_channels(types=self.allowed_types)
        except SlackPermissionError as pe:
            self._print_permission_help(pe)
            return
        member_channels = [c for c in channels if c.get("is_member")]
        
        print(f"\n{'='*60}")
        print(f"  Your Channels ({len(member_channels)})")
        print(f"{'='*60}\n")
        
        for channel in member_channels:
            topic = channel.get("topic", {}).get("value", "No topic")[:50]
            print(f"#{channel['name']:20} - {topic}")
    
    def search_messages(self, query, count=20):
        """Search for messages."""
        if not self.handler:
            print("✗ Not authenticated", file=sys.stderr)
            return
        
        try:
            results = self.handler.search_messages(query, count)
        except SlackPermissionError as pe:
            self._print_permission_help(pe)
            return
        
        print(f"\n{'='*60}")
        print(f"  Search results for: {query}")
        print(f"{'='*60}\n")
        
        if not results:
            print("No messages found.")
            return
        
        for msg in results:
            channel_name = msg.get("channel", {}).get("name", "unknown")
            print(f"#{channel_name} | {self.handler.format_message(msg, compact=True)}")
    
    def manage_vip(self, action, username=None):
        """Manage VIP users."""
        if action == "list":
            vip_users = self.settings.get_vip_users()
            if not vip_users:
                print("No VIP users configured.")
            else:
                print(f"\n{'='*60}")
                print(f"  VIP Users ({len(vip_users)})")
                print(f"{'='*60}\n")
                for user in vip_users:
                    print(f"  @{user['username']} ({user['id']})")
        
        elif action == "add" and username:
            if not self.handler:
                print("✗ Not authenticated", file=sys.stderr)
                return
            
            username = username.lstrip('@')
            user_id = self.handler.resolve_user(username)
            
            if user_id:
                user = self.handler.get_user(user_id)
                self.settings.add_vip_user(user_id, user['name'])
                print(f"✓ Added @{user['name']} to VIP list")
            else:
                print(f"✗ User not found: {username}", file=sys.stderr)
        
        elif action == "remove" and username:
            username = username.lstrip('@')
            # Find user ID from VIP list
            vip_users = self.settings.get_vip_users()
            user = next((u for u in vip_users if u['username'] == username), None)
            
            if user:
                self.settings.remove_vip_user(user['id'])
                print(f"✓ Removed @{username} from VIP list")
            else:
                print(f"✗ User not in VIP list: {username}", file=sys.stderr)
    
    def show_recap(self, interactive=False):
        """Show channel recap."""
        if not self.recap_manager:
            print("✗ Not authenticated", file=sys.stderr)
            return
        
        print("Generating recaps...")
        try:
            self.recap_manager.generate_recaps(types=self.allowed_types)
        except SlackPermissionError as pe:
            self._print_permission_help(pe)
            return
        
        if not self.recap_manager.recaps:
            print("No channel activity to recap.")
            return
        
        if interactive:
            self._interactive_recap()
        else:
            recap = self.recap_manager.get_current_recap()
            if recap:
                print(self.recap_manager.format_recap(recap, detailed=True))
    

def _interactive_recap(self):
    """Interactive recap with Q/E navigation (cross-platform)."""
    recap = self.recap_manager.get_current_recap()
    print("\033[2J\033[H")  # Clear screen
    print(self.recap_manager.format_recap(recap, detailed=True))
    print("\n[Q] Previous | [E] Next | [X] Exit\n")

    while True:
        try:
            char = read_key()
        except RuntimeError as e:
            print(f"\n✗ {e}", file=sys.stderr)
            break

        if not char:
            continue

        if char == "q":
            recap = self.recap_manager.previous_recap()
        elif char == "e":
            recap = self.recap_manager.next_recap()
        elif char == "x":
            break
        else:
            continue

        print("\033[2J\033[H")
        print(self.recap_manager.format_recap(recap, detailed=True))
        print("\n[Q] Previous | [E] Next | [X] Exit\n")

    print("\nExited recap mode.")


def show_auth_help():
    """Show detailed authentication help."""
    help_text = """
╔═══════════════════════════════════════════════════════════════╗
║                  Slack TUI - Authentication Help              ║
╚═══════════════════════════════════════════════════════════════╝

🔐 Supported Token Types (Official Slack Documentation)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reference: https://docs.slack.dev/authentication/tokens

✅ xoxp-*        User Token (recommended for personal use)
✅ xoxb-*        Bot Token
✅ xoxe.xoxp-*   App Bot Access Token (Enterprise Grid)
✅ xoxe-*        App Bot Refresh Token (Enterprise Grid)
✅ xapp-*        App-Level Token (Socket Mode)

📋 Getting a User Token (xoxp-*) - Recommended
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Go to https://api.slack.com/apps
2. Click "Create New App" → "From scratch"
3. Name your app (e.g., "My Slack TUI")
4. Select your workspace
5. Click "OAuth & Permissions" in sidebar
6. Scroll to "User Token Scopes" and add:
   
   • channels:history, channels:read
   • chat:write, files:write
   • groups:history, groups:read
   • im:history, im:read
   • mpim:history, mpim:read
   • search:read
   • users:read, users:read.email

7. Click "Install to Workspace"
8. Copy the "User OAuth Token" (xoxp-...)

📋 Getting a Bot Token (xoxb-*)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Same steps as above, but:
- Add scopes to "Bot Token Scopes" instead
- Copy "Bot User OAuth Token" (xoxb-...)

💾 Providing Your Token
━━━━━━━━━━━━━━━━━━━━━
Method 1 - Command line:
  python slack-tui.py --token xoxp-your-token

Method 2 - Environment variable:
  export SLACK_TOKEN=xoxp-your-token
  python slack-tui.py

Method 3 - .env file:
  Create .env file with: SLACK_TOKEN=xoxp-your-token

🔒 Security
━━━━━━━━━━
• Token stored in ~/.config/slack-tui-app/tokens.json (chmod 0600)
• Never commit tokens to version control
• All token types are equally secure

❓ Which Token Type?
━━━━━━━━━━━━━━━━━━
• Personal use → User Token (xoxp-*)
• Bot features → Bot Token (xoxb-*)
• Enterprise Grid → App Bot tokens (xoxe-*, xoxe.xoxp-*)
• Socket Mode → App-Level Token (xapp-*)

For detailed information: docs/TOKEN_TYPES.md
"""
    print(help_text)


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog='slack-tui',
        description='Focused terminal-based Slack client with VIP filtering',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    # Auth
    parser.add_argument('-t', '--token', help='Slack Web API token (xoxb-* or xoxp-* recommended)')
    parser.add_argument('--save-token', action='store_true', help='Save the provided token to the local config file')
    parser.add_argument('--types', default=None, help='Conversation types for channel discovery (comma-separated). Default: public_channel')
    parser.add_argument('--debug', action='store_true', help='Show debug tracebacks on errors')
    parser.add_argument('--help-auth', action='store_true', help='Show authentication help')
    
    # Quick actions
    parser.add_argument('--send', nargs=2, metavar=('CHANNEL', 'MESSAGE'),
                       help='Send message to channel')
    parser.add_argument('-s', '--show', metavar='CHANNEL', help='Show messages from channel')
    parser.add_argument('-l', '--limit', type=int, default=20, help='Message limit')
    
    # VIP
    parser.add_argument('--vip', action='store_true', help='Show VIP messages')
    parser.add_argument('--vip-add', metavar='USER', help='Add user to VIP list')
    parser.add_argument('--vip-remove', metavar='USER', help='Remove user from VIP list')
    parser.add_argument('--vip-list', action='store_true', help='List VIP users')
    
    # Other
    parser.add_argument('--channels', action='store_true', help='List all channels')
    parser.add_argument('--search', metavar='QUERY', help='Search messages')
    parser.add_argument('--recap', action='store_true', help='Show channel recap (Q/E to navigate)')
    
    args = parser.parse_args()
    
    if args.help_auth:
        show_auth_help()
        return
    
    # Initialize app
    app = SlackTUI()
    
    # Authenticate
    if not await app.authenticate(args.token, save_token=args.save_token, types=args.types, debug=args.debug):
        sys.exit(1)
    
    # Handle actions
    if args.send:
        channel, message = args.send
        app.send_message(channel, message)
    
    elif args.show:
        app.show_messages(args.show, args.limit)
    
    elif args.vip:
        app.show_vip_messages()
    
    elif args.vip_list:
        app.manage_vip("list")
    
    elif args.vip_add:
        app.manage_vip("add", args.vip_add)
    
    elif args.vip_remove:
        app.manage_vip("remove", args.vip_remove)
    
    elif args.channels:
        app.show_channels()
    
    elif args.search:
        app.search_messages(args.search)
    
    elif args.recap:
        app.show_recap(interactive=True)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
