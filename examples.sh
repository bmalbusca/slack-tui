#!/bin/bash
# Slack TUI - Usage Examples

echo "Slack TUI - Usage Examples"
echo "=========================="
echo ""

# Example 1: Daily standup
example_daily_standup() {
    echo "Example 1: Send daily standup to #team"
    echo "---------------------------------------"
    echo 'python slack-tui.py --send "#team" "Daily Update:
- Yesterday: Completed feature X
- Today: Working on feature Y
- Blockers: None"'
    echo ""
}

# Example 2: Check VIP messages
example_check_vip() {
    echo "Example 2: Check VIP messages"
    echo "------------------------------"
    echo "python slack-tui.py --vip"
    echo ""
}

# Example 3: Search and report
example_search() {
    echo "Example 3: Search for project updates"
    echo "--------------------------------------"
    echo 'python slack-tui.py --search "project alpha" > search_results.txt'
    echo "cat search_results.txt"
    echo ""
}

# Example 4: Monitor channel
example_monitor() {
    echo "Example 4: Monitor #alerts channel"
    echo "-----------------------------------"
    echo 'watch -n 60 "python slack-tui.py --show #alerts -l 5"'
    echo ""
}

# Example 5: Batch send
example_batch() {
    echo "Example 5: Send message to multiple channels"
    echo "---------------------------------------------"
    echo 'for channel in team general dev; do'
    echo '  python slack-tui.py --send "#$channel" "Deployment complete!"'
    echo '  sleep 1'
    echo 'done'
    echo ""
}

# Example 6: VIP setup
example_vip_setup() {
    echo "Example 6: Setup VIP users"
    echo "--------------------------"
    echo "python slack-tui.py --vip-add @boss"
    echo "python slack-tui.py --vip-add @client"
    echo "python slack-tui.py --vip-add @tech-lead"
    echo "python slack-tui.py --vip-list"
    echo ""
}

# Example 7: Channel recap
example_recap() {
    echo "Example 7: Interactive channel recap"
    echo "-------------------------------------"
    echo "python slack-tui.py --recap"
    echo "# Use Q and E keys to navigate, X to exit"
    echo ""
}

# Example 8: Git commit notification
example_git_commit() {
    echo "Example 8: Send git commit notification"
    echo "----------------------------------------"
    echo 'MESSAGE="New commits:\\n$(git log --oneline -5)"'
    echo 'python slack-tui.py --send "#commits" "$MESSAGE"'
    echo ""
}

# Example 9: Error alert script
example_error_alert() {
    echo "Example 9: Alert on script failure"
    echo "-----------------------------------"
    cat << 'EOFSCRIPT'
#!/bin/bash
if ! ./important_script.sh 2>&1 | tee output.log; then
    ERROR=$(tail -20 output.log)
    python slack-tui.py --send "#alerts" "Script failed: $ERROR"
fi
EOFSCRIPT
    echo ""
}

# Example 10: Cron job for VIP monitoring
example_cron() {
    echo "Example 10: Cron job to check VIP messages"
    echo "-------------------------------------------"
    echo "# Add to crontab (crontab -e):"
    echo "*/5 * * * * cd /path/to/slack-tui-app && python slack-tui.py --vip > ~/vip_messages.txt"
    echo ""
}

# Show all examples
show_all_examples() {
    example_daily_standup
    example_check_vip
    example_search
    example_monitor
    example_batch
    example_vip_setup
    example_recap
    example_git_commit
    example_error_alert
    example_cron
}

# Main menu
if [ "$1" = "" ]; then
    show_all_examples
else
    case $1 in
        1) example_daily_standup ;;
        2) example_check_vip ;;
        3) example_search ;;
        4) example_monitor ;;
        5) example_batch ;;
        6) example_vip_setup ;;
        7) example_recap ;;
        8) example_git_commit ;;
        9) example_error_alert ;;
        10) example_cron ;;
        *) echo "Unknown example number. Use 1-10 or leave blank for all." ;;
    esac
fi
