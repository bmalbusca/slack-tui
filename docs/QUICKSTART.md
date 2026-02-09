# Quick Start Guide - From Zero to Running

This guide will get you from a completely clean machine to running Slack TUI in under 10 minutes.

## Prerequisites

- A Unix-like system (Linux, macOS, WSL on Windows)
- Internet connection
- Admin/sudo access (for Python installation if needed)
- A Slack workspace where you can create apps

## Step 1: Install Python 3.11+

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip git
```

### macOS

```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11 git
```

### Verify Installation

```bash
python3 --version  # Should show 3.11 or higher
```

## Step 2: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/slack-tui.git
cd slack-tui

# Run automated setup
./setup.sh
```

The setup script will:
- ✓ Check Python version
- ✓ Create virtual environment
- ✓ Install all dependencies
- ✓ Create config directory
- ✓ Copy .env template

## Step 3: Get Your Slack Token

### 3.1 Create Slack App

1. Go to **https://api.slack.com/apps**
2. Click **"Create New App"**
3. Select **"From scratch"**
4. App Name: `My Slack TUI`
5. Select your workspace
6. Click **"Create App"**

### 3.2 Add OAuth Scopes

1. In the left sidebar, click **"OAuth & Permissions"**
2. Scroll to **"User Token Scopes"**
3. Click **"Add an OAuth Scope"** and add these (one by one):

```
channels:history       # Read public channels
channels:read          # View channel info
chat:write             # Send messages
files:write            # Upload files
groups:history         # Read private channels
groups:read            # View private channel info
im:history             # Read DMs
im:read                # View DM info
mpim:history           # Read group DMs
mpim:read              # View group DM info
search:read            # Search messages
users:read             # View users
users:read.email       # View user emails
```

### 3.3 Install App and Get Token

1. At the top of the page, click **"Install to Workspace"**
2. Review permissions and click **"Allow"**
3. You'll see **"User OAuth Token"** - it starts with `xoxp-`
4. Click **"Copy"** to copy the token

## Step 4: Configure Token

### Option A: Using .env file (Recommended)

```bash
# Edit the .env file
nano .env

# Add your token (replace the placeholder):
SLACK_TUI_SLACK_USER_TOKEN=xoxp-paste-your-token-here

# Save and exit (Ctrl+O, Enter, Ctrl+X in nano)
```

### Option B: Using environment variable

```bash
# Add to your shell profile (~/.bashrc or ~/.zshrc)
export SLACK_TUI_SLACK_USER_TOKEN=xoxp-your-token-here

# Or set for current session only
export SLACK_TUI_SLACK_USER_TOKEN=xoxp-your-token-here
```

## Step 5: Run the App

```bash
# Activate virtual environment (if not already active)
source .venv/bin/activate

# Launch TUI
slack-tui
```

You should see:
```
✓ Authenticated as user U123456 on My Workspace

[TUI interface loads with channels on left, messages on right]
```

## Common First-Time Issues

### "command not found: slack-tui"

```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Or use Python module directly
python -m slack_tui.main
```

### "No Slack token found"

```bash
# Verify .env file has token
cat .env | grep SLACK_TUI_SLACK_USER_TOKEN

# Or pass token directly
slack-tui --token xoxp-your-token-here
```

### "Invalid token format"

Make sure your token:
- Starts with `xoxp-` (not `xoxb-`)
- Is a **User OAuth Token** (not Bot Token)
- Has no extra spaces or quotes

### "Missing scopes"

Go back to Slack app settings → OAuth & Permissions → Add missing scopes → Reinstall app → Copy new token

## Quick Usage Examples

### TUI Mode

```bash
# Launch interactive TUI
slack-tui

# Navigation:
# - Select channel from left sidebar
# - Type message in input field (bottom)
# - Press Enter to send
# - Ctrl+V for VIP messages
# - Ctrl+R for channel recap (use Q/E to navigate)
# - Ctrl+C to quit
```

### CLI Mode (Quick Actions)

```bash
# Send a message
slack-tui --send "#general" "Hello from CLI!"

# View VIP messages
slack-tui --vip

# Add VIP user
slack-tui --vip-add @boss

# List all channels
slack-tui --list-channels
```

## What's Next?

1. **Add VIP Users** - Mark important people for priority filtering
   ```bash
   slack-tui --vip-add @boss
   slack-tui --vip-add @client
   ```

2. **Try Recap Mode** - Swipe through channel summaries
   ```bash
   # In TUI: Press Ctrl+R, then Q/E to navigate
   ```

3. **Read Full Docs** - Learn all features
   ```bash
   less README.md
   less INSTALL.md
   ```

4. **Customize Settings** - Edit `.env` file for preferences

## Deactivating Virtual Environment

When done:

```bash
deactivate
```

## Uninstallation

```bash
# Remove virtual environment
rm -rf .venv

# Remove config (WARNING: Deletes saved tokens!)
rm -rf ~/.config/slack-tui

# Remove source (if desired)
cd ..
rm -rf slack-tui
```

## Getting Help

- Run: `slack-tui --help-auth` for authentication help
- Run: `slack-tui --help` for all options
- Read: `README.md` for full documentation
- Visit: https://github.com/yourusername/slack-tui/issues

---

**Total setup time: ~5-10 minutes** ⏱️

**Happy Slacking! 🚀**
