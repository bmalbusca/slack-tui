# Slack Token Types - Official Reference

This document explains all Slack token types supported by Slack TUI.

Reference: https://docs.slack.dev/authentication/tokens

## Supported Token Types

| Token Prefix | Official Name | Use Case | Documentation |
|--------------|---------------|----------|---------------|
| `xoxp-*` | **User Token** | User-level access | Best for personal use |
| `xoxb-*` | **Bot Token** | Bot functionality | For automated bots |
| `xoxe.xoxp-*` | **App Bot Access Token** | Enterprise Grid access | Enterprise apps |
| `xoxe-*` | **App Bot Refresh Token** | Token refresh | Enterprise refresh |
| `xapp-*` | **App-Level Token** | App-level events | Socket Mode |

## Quick Reference

### User Token (xoxp-*)
```bash
# Most common - full user access
export SLACK_TUI_TOKEN=xoxp-123456789012-123456789012-...
python slack-tui.py --channels
```

**When to use:**
- ✅ Personal Slack client
- ✅ Acting as yourself
- ✅ Full access to your channels
- ✅ Read/write messages as you

**Get it from:**
- https://api.slack.com/apps → Your App → OAuth & Permissions → **User OAuth Token**

### Bot Token (xoxb-*)
```bash
# For bot applications
export SLACK_TUI_TOKEN=xoxb-123456789012-123456789012-...
python slack-tui.py --channels
```

**When to use:**
- ✅ Building a bot
- ✅ Automated responses
- ✅ Bot sends messages
- ⚠️ Limited to bot's permissions

**Get it from:**
- https://api.slack.com/apps → Your App → OAuth & Permissions → **Bot User OAuth Token**

**Note:** Bot tokens send messages as your bot, not as you.

### App Bot Access Token (xoxe.xoxp-*)
```bash
# For Enterprise Grid apps
export SLACK_TUI_TOKEN=xoxe.xoxp-1-...
python slack-tui.py --channels
```

**When to use:**
- ✅ Enterprise Grid organizations
- ✅ Multi-workspace access
- ✅ Organization-wide apps

**Get it from:**
- Enterprise Grid admin console
- App management for Enterprise

### App Bot Refresh Token (xoxe-*)
```bash
# For refreshing Enterprise tokens
export SLACK_TUI_TOKEN=xoxe-1-...
```

**When to use:**
- ✅ Token refresh flows
- ✅ Long-lived Enterprise apps
- ⚠️ Typically used programmatically

### App-Level Token (xapp-*)
```bash
# For Socket Mode and app-level features
export SLACK_TUI_TOKEN=xapp-1-...
python slack-tui.py --channels
```

**When to use:**
- ✅ Socket Mode connections
- ✅ App-level events
- ✅ Real-time features

**Get it from:**
- https://api.slack.com/apps → Your App → Basic Information → **App-Level Tokens**

## Token Comparison

| Feature | User (xoxp) | Bot (xoxb) | Enterprise (xoxe) | App (xapp) |
|---------|-------------|------------|-------------------|------------|
| Personal use | ✅ Best | ❌ No | ✅ Yes | ❌ No |
| Bot features | ❌ No | ✅ Best | ✅ Yes | ⚠️ Limited |
| Send as you | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| Enterprise Grid | ❌ No | ❌ No | ✅ Yes | ⚠️ Limited |
| Socket Mode | ❌ No | ❌ No | ❌ No | ✅ Yes |

## Getting Started

### Recommended: User Token (xoxp-*)

**Step-by-step:**

1. Go to https://api.slack.com/apps
2. Click "Create New App" → "From scratch"
3. Name: "My Slack TUI"
4. Select workspace
5. Click "OAuth & Permissions"
6. Add User Token Scopes:
   - `channels:history`
   - `channels:read`
   - `chat:write`
   - `files:write`
   - `groups:history`
   - `groups:read`
   - `im:history`
   - `im:read`
   - `mpim:history`
   - `mpim:read`
   - `search:read`
   - `users:read`
   - `users:read.email`
7. Click "Install to Workspace"
8. Copy "User OAuth Token" (xoxp-...)

### For Bots: Bot Token (xoxb-*)

Same steps as above, but:
- Add scopes to "Bot Token Scopes" instead
- Copy "Bot User OAuth Token" (xoxb-...)

## Security Best Practices

### Storing Tokens

✅ **DO:**
```bash
# Environment variable
export SLACK_TUI_TOKEN=xoxp-...

# .env file (add to .gitignore)
SLACK_TUI_TOKEN=xoxp-...

# Config file (auto chmod 0600)
~/.config/slack-tui-app/tokens.json
```

❌ **DON'T:**
```bash
# Hardcode in scripts
TOKEN="xoxp-..."  # ❌ BAD

# Commit to Git
git add .env      # ❌ BAD

# Share publicly
echo $SLACK_TUI_TOKEN  # ❌ BAD in public logs
```

### Token Permissions

Each token type has different scopes:

- **User tokens** → User Token Scopes
- **Bot tokens** → Bot Token Scopes
- **Enterprise** → Organization scopes
- **App-level** → App-level scopes

Always use **least privilege** principle - only request scopes you need.

## Troubleshooting

### "Unrecognized token format"

**Cause:** Token doesn't match any supported prefix

**Fix:**
1. Check token starts with: `xoxp-`, `xoxb-`, `xoxe.xoxp-`, `xoxe-`, or `xapp-`
2. Verify token is complete (not truncated)
3. Ensure no spaces or quotes

### "Invalid auth"

**Cause:** Token is invalid, expired, or revoked

**Fix:**
1. Go to https://api.slack.com/apps
2. Reinstall app to workspace
3. Copy new token

### Bot can't see channels

**Cause:** Bot not invited to channels

**Fix:**
```
/invite @YourBot
```

Or use User token (xoxp-) for automatic access.

## Migration Between Token Types

### User → Bot
```bash
# Before (as you)
SLACK_TUI_TOKEN=xoxp-old

# After (as bot)
SLACK_TUI_TOKEN=xoxb-new

# Messages now sent as bot
```

### Bot → User
```bash
# Before (as bot)
SLACK_TUI_TOKEN=xoxb-old

# After (as you)
SLACK_TUI_TOKEN=xoxp-new

# Full access restored
```

## Examples

### Check Token Type

The app automatically detects and displays your token type:

```bash
python slack-tui.py --token xoxp-... --channels

# Output:
# ✓ Authenticated as yourname on Your Workspace
# Token type: User Token
```

### Multiple Workspaces

```bash
# Workspace 1 (User)
SLACK_TUI_TOKEN=xoxp-workspace1 python slack-tui.py --vip

# Workspace 2 (Bot)
SLACK_TUI_TOKEN=xoxb-workspace2 python slack-tui.py --send "#alerts" "Update"
```

## Official Documentation

- **Token Types:** https://docs.slack.dev/authentication/tokens
- **User Tokens:** https://docs.slack.dev/authentication/tokens/#user
- **Bot Tokens:** https://docs.slack.dev/authentication/tokens/#bot
- **App-Level Tokens:** https://api.slack.com/apis/connections/socket
- **OAuth Guide:** https://api.slack.com/authentication/oauth-v2

## Summary

✅ All 5 official Slack token types supported
✅ Auto-detection of token type
✅ Clear error messages
✅ Works with User, Bot, Enterprise, and App tokens

**Recommended:** Start with User Token (xoxp-*) for personal use.
