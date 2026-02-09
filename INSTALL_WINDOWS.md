# Windows Installation Guide

## Prerequisites

1. **Python 3.11+** - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify: `python --version`

2. **Git** (optional) - For cloning repository

## Installation

### Method 1: Extract from ZIP/TAR

```cmd
REM Extract slack-tui-app.tar.gz to a folder
REM Open Command Prompt in that folder

REM Run setup
setup.bat
```

### Method 2: Manual Installation

```cmd
REM Navigate to project folder
cd C:\path\to\slack-tui-app

REM Install dependencies
pip install -r requirements.txt

REM Create config directory (optional, auto-created on first run)
mkdir %USERPROFILE%\.config\slack-tui-app
```

## Get Slack Token

1. Go to https://api.slack.com/apps
2. Create New App → From scratch
3. Add User Token Scopes (see README.md)
4. Install to Workspace
5. Copy User OAuth Token (xoxp-...)

## Configure Token

### Option 1: Environment Variable (Session)

```cmd
set SLACK_TUI_TOKEN=xoxp-your-token-here
python slack-tui.py --channels
```

### Option 2: Persistent Environment Variable

1. Press `Win + X` → System
2. Advanced system settings → Environment Variables
3. Under "User variables", click New
4. Variable name: `SLACK_TUI_TOKEN`
5. Variable value: `xoxp-your-token-here`
6. Click OK

Restart Command Prompt, then:
```cmd
python slack-tui.py --channels
```

### Option 3: Pass Token Each Time

```cmd
python slack-tui.py --token xoxp-your-token --channels
```

## Usage

```cmd
REM List channels
python slack-tui.py --channels

REM Send message
python slack-tui.py --send "#general" "Hello from Windows!"

REM Show messages
python slack-tui.py --show "#general"

REM VIP messages
python slack-tui.py --vip-add @boss
python slack-tui.py --vip

REM Channel recap
python slack-tui.py --recap
```

## Troubleshooting

### "python: command not found"

Python not in PATH. Reinstall Python and check "Add to PATH" option.

### "pip: command not found"

```cmd
python -m pip install -r requirements.txt
```

### Module Import Errors

```cmd
REM Reinstall dependencies
pip uninstall slack-sdk
pip install -r requirements.txt
```

### Terminal Encoding Issues

```cmd
REM Set UTF-8 encoding
chcp 65001
python slack-tui.py --channels
```

### Recap Mode (Q/E Navigation)

Recap mode requires terminal with raw input support. Use:
- Windows Terminal (recommended)
- PowerShell
- Git Bash

Standard Command Prompt may not support interactive recap properly.

## Configuration Files

Located in: `%USERPROFILE%\.config\slack-tui-app\`

- `tokens.json` - Saved tokens
- `vip_users.json` - VIP user list
- `settings.json` - App settings

## Running from Anywhere

### Create Batch Script

Create `slack-tui.bat` in a folder that's in your PATH (e.g., `C:\bin\`):

```batch
@echo off
python C:\path\to\slack-tui-app\slack-tui.py %*
```

Then you can run from anywhere:
```cmd
slack-tui --vip
```

### Or Use Python Scripts

Add to PATH, then run:
```cmd
python -m slack_tui.slack-tui
```

## Getting Help

```cmd
python slack-tui.py --help
python slack-tui.py --help-auth
```

## Notes

- File permissions (chmod) don't work the same on Windows - tokens.json won't have Unix-style permissions
- Interactive recap (Q/E keys) works best in Windows Terminal or PowerShell
- Use forward slashes or double backslashes in paths: `C:/path/to/file` or `C:\\path\\to\\file`
