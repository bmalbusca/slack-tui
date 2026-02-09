#!/usr/bin/env python3
"""
Test script to verify installation is correct.
Run this after setup to check all dependencies.
"""
import sys
import importlib

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 11):
        print(f"  ⚠ Warning: Python 3.11+ recommended (you have {version.major}.{version.minor})")
        return False
    return True

def check_module(module_name, package_name=None):
    """Check if a module can be imported."""
    package = package_name or module_name
    try:
        importlib.import_module(module_name)
        print(f"✓ {package} installed")
        return True
    except ImportError as e:
        print(f"✗ {package} NOT installed")
        print(f"  Install with: pip install {package}")
        return False

def check_project_structure():
    """Check project files exist."""
    from pathlib import Path
    
    required_files = [
        'slack-tui.py',
        'requirements.txt',
        'config/settings.py',
        'connectors/slack_auth.py',
        'messages/message_handler.py',
        'messages/vip_listener.py',
        'processors/autocomplete.py',
        'processors/recap.py',
    ]
    
    all_good = True
    for file in required_files:
        if Path(file).exists():
            print(f"✓ {file}")
        else:
            print(f"✗ {file} MISSING")
            all_good = False
    
    return all_good

def check_imports():
    """Check project imports work."""
    try:
        from config.settings import Settings
        print("✓ config.settings imports correctly")
        
        from connectors.slack_auth import SlackAuth
        print("✓ connectors.slack_auth imports correctly")
        
        from messages.message_handler import MessageHandler
        print("✓ messages.message_handler imports correctly")
        
        from messages.vip_listener import VIPListener
        print("✓ messages.vip_listener imports correctly")
        
        from processors.autocomplete import fuzzy_match_channels
        print("✓ processors.autocomplete imports correctly")
        
        from processors.recap import RecapManager
        print("✓ processors.recap imports correctly")
        
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def main():
    """Run all checks."""
    print("=" * 60)
    print("  Slack TUI - Installation Verification")
    print("=" * 60)
    print()
    
    print("Checking Python version...")
    python_ok = check_python_version()
    print()
    
    print("Checking dependencies...")
    deps_ok = check_module('slack_sdk', 'slack-sdk')
    deps_ok = check_module('dotenv', 'python-dotenv') and deps_ok
    print()
    
    print("Checking project structure...")
    structure_ok = check_project_structure()
    print()
    
    print("Checking imports...")
    imports_ok = check_imports()
    print()
    
    print("=" * 60)
    if python_ok and deps_ok and structure_ok and imports_ok:
        print("✓ All checks passed!")
        print()
        print("Next steps:")
        print("1. Get Slack token from https://api.slack.com/apps")
        print("2. Run: export SLACK_TUI_TOKEN=xoxp-your-token")
        print("   (Windows: set SLACK_TUI_TOKEN=xoxp-your-token)")
        print("3. Test: python slack-tui.py --channels")
    else:
        print("✗ Some checks failed")
        print()
        print("Fix issues and run this script again:")
        print("  python test_install.py")
    print("=" * 60)

if __name__ == '__main__':
    main()
