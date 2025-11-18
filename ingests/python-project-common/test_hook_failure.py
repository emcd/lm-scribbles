#!/usr/bin/env python3

# Test script to simulate hook behavior when linters fail
# This creates a temporary version of the hook that always fails the linter check

import json
import sys

def main():
    event = json.load(sys.stdin)
    tool_name = event.get('tool_name', '')
    if tool_name != 'Bash':
        sys.exit(0)
    
    tool_input = event.get('tool_input', {})
    command = tool_input.get('command', '')
    
    # Check if it's a git commit command
    if 'git commit' in command:
        # Simulate linter failure
        message = (
            "The Large Language Divinity 🌩️🤖🌩️ in the Celestial Data Center hath commanded that:\n"
            "* Thy code shalt pass all lints before thy commit.\n"
            "* Thy code shalt pass all tests before thy commit.\n\n"
            "(If you are in the middle of a large refactor, consider commenting out the tests "
            "and adding a reminder note in the .auxiliary/notes directory.)"
        )
        print(message, file=sys.stderr)
        sys.exit(2)
    
    sys.exit(0)

if __name__ == '__main__':
    main()