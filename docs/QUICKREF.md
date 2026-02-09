# Slack TUI - Quick Reference

## Basic Commands

### Send Messages
```bash
python slack-tui.py --send "#channel" "message"     # Send to channel
python slack-tui.py --send "@user" "message"        # Send to user
```

### View Messages
```bash
python slack-tui.py --show "#channel"               # Show messages
python slack-tui.py --show "#channel" -l 50         # Show 50 messages
```

### Search
```bash
python slack-tui.py --search "keyword"              # Search messages
```

### VIP Management
```bash
python slack-tui.py --vip                           # Show VIP messages
python slack-tui.py --vip-add @username             # Add to VIP list
python slack-tui.py --vip-remove @username          # Remove from VIP
python slack-tui.py --vip-list                      # List VIP users
```

### Channel Recap
```bash
python slack-tui.py --recap                         # Interactive recap
# Press Q for previous, E for next, X to exit
```

### Other Commands
```bash
python slack-tui.py --channels                      # List all channels
python slack-tui.py --help                          # Show all options
python slack-tui.py --help-auth                     # Authentication help
```

## Message Format

### Compact (default)
```
[abc123] 14:30:15 alice: Hey team, quick update 🧵
```

### With VIP indicator
```
[def456] 14:31:22 ⭐boss: Important message
```

## Configuration

### Token Storage
Tokens stored in: `~/.config/slack-tui-app/tokens.json`

### Supported Token Types
- `xoxp-*` - User OAuth Token (recommended)
- `xoxb-*` - Bot User OAuth Token
- `xoxe.xoxp-*` - Enterprise User Token
- `xoxe-*` - Enterprise Token
- `xapp-*` - App-Level Token

### VIP Users
VIP list in: `~/.config/slack-tui-app/vip_users.json`

### Environment Variables
```bash
export SLACK_TUI_TOKEN=xoxp-your-token  # Any token type works
```

## Common Workflows

### Morning Routine
```bash
# Check VIP messages
python slack-tui.py --vip

# Quick recap of all channels
python slack-tui.py --recap

# Check specific channel
python slack-tui.py --show "#team" -l 20
```

### Send Updates
```bash
# Send to multiple channels
for channel in team general dev; do
  python slack-tui.py --send "#$channel" "Update message"
done
```

### Search History
```bash
# Find discussion
python slack-tui.py --search "project deadline"
```

## Keyboard Shortcuts (Recap Mode)

| Key | Action |
|-----|--------|
| `Q` | Previous channel |
| `E` | Next channel |
| `X` | Exit recap mode |

## Troubleshooting

### Authentication
```bash
# Get detailed auth help
python slack-tui.py --help-auth

# Test with token
python slack-tui.py --token xoxp-your-token --channels
```

### Common Issues

**"No token found"**
- Set: `export SLACK_TUI_TOKEN=xoxp-your-token`
- Or use: `--token xoxp-your-token`

**"Invalid token format"**
- Token must start with: xoxp-, xoxb-, xoxe.xoxp-, xoxe-, or xapp-
- All token types are supported

**"Unrecognized token format"**
- Check token is complete (no truncation)
- Verify it starts with valid prefix

**"Channel not found"**
- Use `--channels` to list available channels
- Include # prefix: `--send "#general" "message"`

## Quick Tips

1. **VIP-only monitoring**: Run `python slack-tui.py --vip` in a loop
2. **Alias for convenience**: `alias st='python slack-tui.py'`
3. **Pipe output**: `python slack-tui.py --show "#logs" -l 100 > logs.txt`
4. **Search and act**: Find message ID, then reference in conversation

## Getting Help

- Full docs: `less README.md`
- Auth help: `python slack-tui.py --help-auth`
- All options: `python slack-tui.py --help`
