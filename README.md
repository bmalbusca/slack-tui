# Slack TUI - Terminal Interface for Slack

A focused, terminal-based Slack client with VIP filtering and channel recap functionality.

## Features

- 🎯 **Simple CLI** - No complex TUI, just clean command-line interface
- ⭐ **VIP Filtering** - Priority messages from important people
- 📊 **Channel Recap** - Navigate channel summaries with Q/E keys
- 🔍 **Message Search** - Find messages across workspace
- 💬 **Send & Receive** - Full message support
- 🆔 **Message IDs** - Unique IDs for easy reference

## Requirements

- Python 3.11+
- Slack workspace with app creation permissions
- Slack token (User, Bot, or App token)

## Supported Token Types

✅ **xoxp-*** - User OAuth Token (recommended for full access)
✅ **xoxb-*** - Bot User OAuth Token
✅ **xoxe.xoxp-*** - App Bot Access Token
✅ **xoxe-*** - App Bot Refresh Token
✅ **xapp-*** - App-Level Token

## Quick Start

### 1. Installation

```bash
# Clone repository
git clone https://github.com/yourusername/slack-tui-app.git
cd slack-tui-app

# Run setup
./setup.sh
```

### 2. Get Slack Token

You can use any of these token types:

#### Option A: User OAuth Token (xoxp-*) - Recommended

1. Go to **https://api.slack.com/apps**
2. Click **"Create New App"** → **"From scratch"**
3. Name: "My Slack TUI"
4. Select your workspace
5. Go to **"OAuth & Permissions"**
6. Add **User Token Scopes**:
   - `channels:history`, `channels:read`
   - `chat:write`, `files:write`
   - `groups:history`, `groups:read`
   - `im:history`, `im:read`
   - `mpim:history`, `mpim:read`
   - `search:read`
   - `users:read`, `users:read.email`
7. Click **"Install to Workspace"**
8. Copy **"User OAuth Token"** (starts with `xoxp-`)

#### Option B: Bot User OAuth Token (xoxb-*)

1. Follow steps 1-4 above
2. Go to **"OAuth & Permissions"**
3. Add **Bot Token Scopes** (same as above)
4. Click **"Install to Workspace"**
5. Copy **"Bot User OAuth Token"** (starts with `xoxb-`)

#### Option C: App Bot Tokens (xoxe-*, xoxe.xoxp-*)

For Enterprise Grid or app installations:
- **xoxe.xoxp-*** - App Bot Access Token (active session)
- **xoxe-*** - App Bot Refresh Token (to refresh access)

These are typically used in Enterprise Grid environments or when using the newer app token flow.

#### Option D: App-Level Token (xapp-*)

For Socket Mode and app-level features:
1. Go to your app settings
2. Navigate to "App-Level Tokens"
3. Generate token with appropriate scopes
4. Copy the token (starts with `xapp-`)

### 3. Configure Token

```bash
# Option 1: Environment variable
export SLACK_TOKEN=xoxp-your-token

# Option 2: Pass on command line
python slack-tui.py --token xoxp-your-token --channels
```

## Usage

### Send Messages

```bash
# Send to channel
python slack-tui.py --send "#general" "Hello team!"

# Send to user
python slack-tui.py --send "@alice" "Hi Alice!"
```

### View Messages

```bash
# Show recent messages
python slack-tui.py --show "#general"

# Show last 50 messages
python slack-tui.py --show "#general" -l 50
```

### VIP Features

```bash
# Add VIP users
python slack-tui.py --vip-add @boss
python slack-tui.py --vip-add @client

# View VIP messages
python slack-tui.py --vip

# List VIP users
python slack-tui.py --vip-list

# Remove VIP user
python slack-tui.py --vip-remove @username
```

### Channel Recap

```bash
# Interactive recap (use Q/E to navigate, X to exit)
python slack-tui.py --recap
```

### Search

```bash
# Search messages
python slack-tui.py --search "project deadline"
```

### List Channels

```bash
# Show all channels you're in
python slack-tui.py --channels
```

## Project Structure

```
slack-tui-app/
├── slack-tui.py              # Main CLI application
├── requirements.txt          # Python dependencies
├── setup.sh                  # Installation script
├── examples.sh               # Usage examples
├── README.md                 # This file
│
├── config/                   # Configuration management
│   ├── __init__.py
│   └── settings.py           # Settings and token storage
│
├── connectors/               # Slack authentication
│   ├── __init__.py
│   └── slack_auth.py         # OAuth authentication
│
├── messages/                 # Message handling
│   ├── __init__.py
│   ├── message_handler.py    # Send/receive messages
│   └── vip_listener.py       # VIP filtering
│
├── processors/               # Message processors
│   ├── __init__.py
│   ├── autocomplete.py       # Fuzzy matching
│   └── recap.py              # Channel recap
│
└── docs/                     # Documentation
    ├── QUICKREF.md           # Quick reference
    ├── QUICKSTART.md         # Getting started guide
    └── PROJECT_SUMMARY.md    # Complete project overview
```

## Configuration

Configuration stored in `~/.config/slack-tui-app/`:

- `tokens.json` - Stored tokens (chmod 0600)
- `vip_users.json` - VIP user list
- `settings.json` - App preferences

## Examples

See `examples.sh` for more usage examples:

```bash
# View all examples
./examples.sh

# Run specific example
./examples.sh 1
```

## Troubleshooting

### Authentication Issues

**"No token found"**
```bash
# Set environment variable
export SLACK_TOKEN=xoxp-your-token  # or xoxb-, xoxe-, xapp-

# Or pass directly
python slack-tui.py --token xoxp-your-token --channels
```

**"Invalid token format"**
- Supported formats: xoxp-, xoxb-, xoxe.xoxp-, xoxe-, xapp-
- Check that token is correctly copied (no spaces, complete)
- Verify token hasn't expired or been revoked

**"Unrecognized token format"**
- Make sure token starts with one of: xoxp-, xoxb-, xoxe.xoxp-, xoxe-, xapp-
- Legacy tokens (xoxa-, xoxr-) are not supported

**"Missing scopes"**
- Go to api.slack.com/apps → Your App
- Add missing scopes to User Token Scopes or Bot Token Scopes
- Reinstall app to workspace
- Get new token

### For More Help

```bash
# Show authentication help
python slack-tui.py --help-auth

# Show all options
python slack-tui.py --help
```

## Documentation

- **QUICKREF.md** - Quick command reference
- **QUICKSTART.md** - Detailed setup guide
- **PROJECT_SUMMARY.md** - Complete project documentation

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

```bash
# Format code
black .

# Lint
ruff check .
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

## License

MIT License - See LICENSE file

## Support

- Issues: https://github.com/yourusername/slack-tui-app/issues
- Discussions: https://github.com/yourusername/slack-tui-app/discussions

---

Made with ❤️ for focused work

## Permissions & Scopes

This tool uses Slack's **Web API**. Authentication (`auth.test`) can succeed even when a token cannot read channels/messages.

- Default mode is **public channels only** (`--types public_channel`) to minimize required scopes.
- See **PERMISSIONS.md** for a command → API method → scope matrix.
- If you get `missing_scope` or `not_allowed_token_type`, your token/workspace policy does not allow the requested operation.

### Common minimal scopes (public channels)

- `channels:read` (list public channels)
- `channels:history` (read messages)
- `users:read` (optional; username resolution)

