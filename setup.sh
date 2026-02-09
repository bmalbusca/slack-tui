#!/bin/bash
#
# Slack TUI - Setup and Installation Script
# This script will guide you through setting up Slack TUI on a clean machine
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    Slack TUI Setup                            ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Python version
echo -e "${BLUE}[1/5] Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found${NC}"
    echo "Please install Python 3.11 or higher first."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.11"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" 2>/dev/null; then
    echo -e "${RED}✗ Python ${PYTHON_VERSION} found, but 3.11+ required${NC}"
    echo "Please upgrade Python to 3.11 or higher."
    exit 1
fi

echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"

# Create virtual environment
echo -e "\n${BLUE}[2/5] Setting up virtual environment...${NC}"
if [ -d ".venv" ]; then
    echo -e "${YELLOW}  Virtual environment already exists${NC}"
    read -p "  Remove and recreate? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf .venv
    fi
fi

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Using existing virtual environment${NC}"
fi

# Activate virtual environment
source .venv/bin/activate || { echo -e "${RED}✗ Failed to activate venv${NC}"; exit 1; }

# Upgrade pip
echo -e "\n${BLUE}[3/5] Upgrading pip...${NC}"
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ pip upgraded${NC}"

# Install package
echo -e "\n${BLUE}[4/5] Installing Slack TUI...${NC}"
if pip install -e ".[dev]" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Package installed${NC}"
else
    echo -e "${RED}✗ Installation failed${NC}"
    echo "Try running: pip install -e ."
    exit 1
fi

# Setup configuration
echo -e "\n${BLUE}[5/5] Configuration setup...${NC}"

CONFIG_DIR="$HOME/.config/slack-tui"
mkdir -p "$CONFIG_DIR"
echo -e "${GREEN}✓ Config directory created: ${CONFIG_DIR}${NC}"

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "\n${YELLOW}No .env file found.${NC}"
    read -p "Create .env file now? (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        cp .env.example .env
        echo -e "${GREEN}✓ Created .env file from template${NC}"
        echo -e "${YELLOW}⚠ Please edit .env and add your Slack token${NC}"
    fi
fi

# Success message
echo -e "\n${GREEN}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                  Installation Complete! ✓                     ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check for token
if [ -f ".env" ]; then
    if grep -q "xoxp-your-token-here" .env 2>/dev/null; then
        echo -e "${YELLOW}⚠ You need to add your Slack token to .env${NC}"
        TOKEN_SET=false
    else
        TOKEN_SET=true
    fi
else
    TOKEN_SET=false
fi

# Next steps
echo -e "\n${BLUE}Next Steps:${NC}"
echo ""

if [ "$TOKEN_SET" = false ]; then
    echo "1. Get your Slack token:"
    echo "   ${BLUE}→ Visit: https://api.slack.com/apps${NC}"
    echo "   → Create a new app (or select existing)"
    echo "   → Go to 'OAuth & Permissions'"
    echo "   → Add required User Token Scopes (see README.md)"
    echo "   → Install to workspace"
    echo "   → Copy the User OAuth Token (starts with xoxp-)"
    echo ""
    echo "2. Add token to .env file:"
    echo "   ${BLUE}→ Edit: .env${NC}"
    echo "   → Set: SLACK_TUI_SLACK_USER_TOKEN=xoxp-your-token"
    echo ""
    echo "3. Activate virtual environment:"
    echo "   ${BLUE}→ Run: source .venv/bin/activate${NC}"
    echo ""
    echo "4. Launch the app:"
    echo "   ${BLUE}→ Run: slack-tui${NC}"
else
    echo "1. Activate virtual environment:"
    echo "   ${BLUE}→ Run: source .venv/bin/activate${NC}"
    echo ""
    echo "2. Launch the app:"
    echo "   ${BLUE}→ Run: slack-tui${NC}"
fi

echo ""
echo "For help:"
echo "  ${BLUE}→ Authentication: slack-tui --help-auth${NC}"
echo "  ${BLUE}→ CLI options: slack-tui --help${NC}"
echo "  ${BLUE}→ README: less README.md${NC}"
echo ""

# Offer to run tests
if [ "$TOKEN_SET" = true ]; then
    read -p "Run tests to verify installation? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "\n${BLUE}Running tests...${NC}"
        if pytest tests/ -v; then
            echo -e "${GREEN}✓ All tests passed${NC}"
        else
            echo -e "${YELLOW}⚠ Some tests failed (this is OK if you don't have a test workspace)${NC}"
        fi
    fi
fi

echo -e "\n${GREEN}Happy Slacking! 🚀${NC}\n"
