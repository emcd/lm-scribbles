#!/usr/bin/env python3
"""
Terminal Detection Script for Git Bash/Mintty Compatibility

This script examines various environment variables and system properties
to help identify Git Bash/Mintty terminals that might have Unicode issues.
"""

import os
import sys
import locale
import platform

def detect_terminal_environment():
    """Collect terminal environment information."""

    print("=== Terminal Detection Report ===")
    print()

    # Basic platform info
    print(f"Platform: {sys.platform}")
    print(f"OS: {platform.system()} {platform.release()}")
    print()

    # Environment variables that might indicate Git Bash/Mintty
    env_vars = [
        'TERM',           # Terminal type
        'SHELL',          # Shell being used
        'MSYSTEM',        # MSYS2/Git Bash indicator
        'MSYS',           # MSYS indicator
        'MINTTY',         # Mintty terminal indicator
        'SESSIONNAME',    # Windows session name
        'USERDOMAIN',     # Windows domain
        'TERM_PROGRAM',   # Terminal program name
        'TERM_PROGRAM_VERSION',  # Terminal version
        'COLORTERM',      # Color terminal support
        'SSH_TTY',        # SSH session indicator
    ]

    print("Environment Variables:")
    for var in env_vars:
        value = os.environ.get(var, '<not set>')
        print(f"  {var}: {value}")
    print()

    # Encoding information
    print("Encoding Information:")
    print(f"  Default encoding: {sys.getdefaultencoding()}")
    print(f"  Filesystem encoding: {sys.getfilesystemencoding()}")
    print(f"  Locale encoding: {locale.getpreferredencoding()}")
    print(f"  Stdout encoding: {getattr(sys.stdout, 'encoding', 'unknown')}")
    print(f"  Stderr encoding: {getattr(sys.stderr, 'encoding', 'unknown')}")
    print()

    # TTY information
    print("TTY Information:")
    print(f"  stdout.isatty(): {sys.stdout.isatty()}")
    print(f"  stderr.isatty(): {sys.stderr.isatty()}")
    print(f"  stdin.isatty(): {sys.stdin.isatty()}")
    print()

    # Test Unicode output capability
    print("Unicode Test:")
    try:
        # Try to print some Unicode characters that Tyro uses
        test_chars = "╭─╮│╰─╯"  # Box drawing characters
        print(f"  Box characters: {test_chars}")
        print("  Unicode test: ✓ Success")
    except UnicodeEncodeError as e:
        print(f"  Unicode test: Failed - {e}")
    except Exception as e:
        print(f"  Unicode test: Error - {e}")
    print()

    # Proposed detection logic
    print("=== Detection Logic Tests ===")

    # Current logic
    is_problematic_1 = (sys.platform == 'win32' and
                       os.environ.get('TERM', '').lower() in ('', 'dumb'))
    print(f"Current logic (TERM check): {'SKIP' if is_problematic_1 else 'RUN'}")

    # Alternative: Check for Git Bash specifically
    is_git_bash = (sys.platform == 'win32' and
                   os.environ.get('MSYSTEM') is not None)
    print(f"Git Bash check (MSYSTEM): {'SKIP' if is_git_bash else 'RUN'}")

    # Alternative: Check for Mintty
    is_mintty = (sys.platform == 'win32' and
                'mintty' in os.environ.get('TERM_PROGRAM', '').lower())
    print(f"Mintty check (TERM_PROGRAM): {'SKIP' if is_mintty else 'RUN'}")

    # Encoding-based check
    encoding_problematic = (sys.platform == 'win32' and
                           getattr(sys.stdout, 'encoding', '').lower() in ('cp1252', 'ascii'))
    print(f"Encoding check (cp1252/ascii): {'SKIP' if encoding_problematic else 'RUN'}")

    print()
    print("Run this script in different terminals to compare results!")

if __name__ == '__main__':
    detect_terminal_environment()
