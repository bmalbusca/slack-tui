# Slack TUI - Complete File Tree

```
slack-tui/
│
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions CI/CD pipeline
│
├── .gitignore                        # Git ignore patterns
│
├── docs/
│   └── screenshots/
│       ├── PLACEHOLDER.md            # Placeholder for screenshots
│       └── README.md                 # Screenshot generation guide
│
├── src/
│   └── slack_tui/
│       ├── __init__.py               # Package initialization
│       ├── auth.py                   # Authentication module (200 lines)
│       ├── client.py                 # Slack API client (350 lines)
│       ├── config.py                 # Configuration management (80 lines)
│       ├── main.py                   # CLI entry point (280 lines)
│       └── tui.py                    # Textual TUI application (350 lines)
│
├── tests/
│   ├── __init__.py                   # Tests package init
│   ├── conftest.py                   # Pytest configuration
│   └── test_auth.py                  # Authentication tests
│
├── CHANGELOG.md                      # Version history
├── CONTRIBUTING.md                   # Contribution guidelines
├── INSTALL.md                        # Installation instructions
├── LICENSE                           # MIT License
├── MANIFEST.in                       # Package data files
├── pyproject.toml                    # Project configuration and dependencies
└── README.md                         # Main documentation

Total: 19 files
```

## File Descriptions

### Root Configuration Files

#### `pyproject.toml`
Project metadata, dependencies, build configuration, and tool settings.
- Build system: hatchling
- Python version: >=3.11
- Dependencies: textual, slack-sdk, httpx, pydantic, etc.
- Dev dependencies: pytest, black, ruff, mypy
- Scripts: `slack-tui` command entry point

#### `.gitignore`
Ignore patterns for:
- Python bytecode and caches
- Virtual environments
- IDE configurations
- Log files
- Secrets and tokens
- Build artifacts

#### `MANIFEST.in`
Specifies which non-Python files to include in distribution package.

### Documentation Files

#### `README.md` (Main Documentation)
- Project overview and features
- Screenshots (placeholders)
- Installation instructions
- Quick start guide
- Usage examples (TUI and CLI)
- Configuration options
- Troubleshooting
- Contributing information
- License

#### `INSTALL.md`
Step-by-step installation instructions:
- Requirements
- Python installation
- Package installation (pip/pipx/source)
- Slack token generation
- First run
- Troubleshooting

#### `CONTRIBUTING.md`
Developer guidelines:
- Getting started with development
- Code style and testing
- Pull request process
- Project structure
- Common development tasks

#### `CHANGELOG.md`
Version history and release notes.

#### `LICENSE`
MIT License text.

### Source Code Files

#### `src/slack_tui/__init__.py`
Package initialization:
- Version information
- Public API exports
- Module imports

#### `src/slack_tui/config.py`
Configuration management using Pydantic Settings:
- Environment variable loading
- Token storage/retrieval
- Settings persistence
- Path management

**Key Classes:**
- `Settings`: Main settings class with validators

**Key Features:**
- Loads from .env files
- Supports environment variables with `SLACK_TUI_` prefix
- Secure token storage (0600 permissions)
- Configuration file paths

#### `src/slack_tui/auth.py`
Authentication handling with comprehensive error messages:
- OAuth 2.0 flow
- Token validation
- Scope checking
- Error handling

**Key Classes:**
- `AuthError`: Custom exception with user-friendly messages
- `SlackAuth`: Authentication manager

**Key Methods:**
- `authenticate()`: Main authentication method (async)
- `get_client()`: Returns authenticated WebClient
- `logout()`: Clears authentication
- `open_oauth_url()`: Opens browser to Slack app page

**Error Handling:**
- Invalid token format detection
- Missing scopes reporting
- Expired token guidance
- Network error handling

#### `src/slack_tui/client.py`
High-level Slack API client:
- Message operations
- Channel management
- User management
- VIP filtering
- Message caching

**Key Classes:**
- `SlackClient`: Main API wrapper

**Key Methods:**
- Message Operations:
  - `get_messages()`: Fetch channel messages
  - `send_message()`: Send messages
  - `get_thread_replies()`: Fetch thread
  - `search_messages()`: Search across workspace
  - `upload_file()`: File uploads
  
- Channel Operations:
  - `get_channels()`: List all channels
  - `get_channel()`: Get channel details
  - `resolve_channel()`: Name/ID resolution
  
- User Operations:
  - `get_users()`: List all users
  - `get_user()`: Get user details
  - `resolve_user()`: Name/ID resolution
  
- VIP Management:
  - `add_vip_user()`: Add to VIP list
  - `remove_vip_user()`: Remove from VIP list
  - `is_vip()`: Check VIP status
  - `get_vip_messages()`: Fetch VIP messages
  
- Message ID System:
  - `generate_message_id()`: Create 8-char ID
  - `get_message_by_id()`: Retrieve by ID
  
- Formatting:
  - `format_message()`: Display formatting

**Caching:**
- Message cache (ID → channel/ts mapping)
- Channel cache (ID/name → info)
- User cache (ID/name → info)

#### `src/slack_tui/tui.py`
Textual-based TUI application:
- Async message handling
- Interactive navigation
- Keyboard shortcuts
- Real-time updates

**Key Classes:**
- `SlackTUI`: Main application
- `MessageItem`: Message list item
- `ChannelRecap`: Recap display widget

**UI Components:**
- Header: App title
- Sidebar: Channel list
- Content: Message display
- Input: Message composition
- Status bar: Operation feedback
- Footer: Keyboard shortcuts

**Keyboard Bindings:**
- `Ctrl+C`: Quit
- `Ctrl+R`: Toggle recap
- `Ctrl+V`: Show VIP messages
- `Ctrl+S`: Search (planned)
- `Q`/`E`: Navigate recap

**Key Methods:**
- `authenticate()`: Initial auth (async)
- `load_channels()`: Fetch channel list
- `load_messages()`: Fetch messages
- `send_message()`: Send message
- `action_show_vip()`: VIP view
- `action_toggle_recap()`: Recap mode

#### `src/slack_tui/main.py`
CLI entry point and argument parsing:
- Command-line interface
- Quick actions (non-TUI)
- Help text generation

**Key Functions:**
- `main()`: Entry point
- `show_auth_help()`: Detailed auth help
- `handle_quick_action()`: CLI mode actions

**CLI Arguments:**
- Authentication:
  - `--token`: Provide token
  - `--help-auth`: Auth help
  
- Quick Actions:
  - `--send CHANNEL MESSAGE`: Send message
  - `--vip`: Show VIP messages
  - `--list-channels`: List channels
  
- VIP Management:
  - `--vip-add USER`: Add VIP
  - `--vip-remove USER`: Remove VIP
  - `--vip-list`: List VIPs

### Test Files

#### `tests/conftest.py`
Pytest configuration:
- Fixtures for temp config directories
- Mock token generation
- Test utilities

#### `tests/test_auth.py`
Authentication module tests:
- Successful authentication
- Invalid token handling
- Missing token errors
- API error handling
- Logout functionality

**Test Coverage:**
- Happy path authentication
- Error cases
- Token validation
- Scope checking

### CI/CD Files

#### `.github/workflows/ci.yml`
GitHub Actions workflow:
- Multi-OS testing (Ubuntu, macOS, Windows)
- Multi-Python version (3.11, 3.12)
- Code quality checks (ruff, black, mypy)
- Test execution with coverage
- Package building
- Artifact storage

## File Statistics

### Lines of Code

```
Source Code:
  config.py:     ~80 lines
  auth.py:      ~200 lines
  client.py:    ~350 lines
  tui.py:       ~350 lines
  main.py:      ~280 lines
  __init__.py:   ~10 lines
  ────────────────────────
  Total:      ~1,270 lines

Tests:
  test_auth.py:  ~100 lines
  conftest.py:    ~30 lines
  ────────────────────────
  Total:        ~130 lines

Documentation:
  README.md:    ~400 lines
  INSTALL.md:   ~200 lines
  CONTRIBUTING: ~300 lines
  ────────────────────────
  Total:        ~900 lines

Grand Total: ~2,300 lines
```

### Dependencies

**Production:**
- textual >=0.47.0 (TUI framework)
- slack-sdk >=3.26.0 (Slack API)
- httpx >=0.25.0 (Async HTTP)
- python-dotenv >=1.0.0 (Environment loading)
- rich >=13.7.0 (Terminal formatting)
- pydantic >=2.5.0 (Data validation)
- pydantic-settings >=2.1.0 (Settings management)
- websockets >=12.0 (WebSocket support)

**Development:**
- pytest >=7.4.0 (Testing)
- pytest-asyncio >=0.21.0 (Async testing)
- black >=23.0.0 (Formatting)
- ruff >=0.1.0 (Linting)
- mypy >=1.7.0 (Type checking)

## Runtime Files (Created on First Run)

```
~/.config/slack-tui/
├── tokens.json        # Encrypted token storage (chmod 0600)
├── vip_users.json     # VIP user IDs
└── settings.json      # User preferences
```

## Build Artifacts (Not in Git)

```
build/                 # Build output
dist/                  # Distribution packages
*.egg-info/            # Package metadata
__pycache__/           # Python bytecode cache
.pytest_cache/         # Pytest cache
.mypy_cache/           # MyPy cache
.coverage              # Coverage data
htmlcov/               # Coverage HTML report
```
