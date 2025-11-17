#!/usr/bin/env python3
"""
Analysis script to understand robots.txt access failure handling.
"""

import sys
import traceback
from pathlib import Path

# Add the source directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "sources"))

import librovore.exceptions as exc
import appcore.generics as generics

def analyze_error_handling():
    """Analyze how RobotsTxtAccessFailure is handled in cached responses."""

    print("=== Analysis of RobotsTxtAccessFailure Handling ===\n")

    # Create a sample RobotsTxtAccessFailure
    domain = "https://docs.pytest.org"
    cause = Exception("Client error '403 Forbidden' for url 'https://docs.pytest.org/robots.txt'")
    robots_failure = exc.RobotsTxtAccessFailure(domain, cause)

    print("1. RobotsTxtAccessFailure exception created:")
    print(f"   Domain: {robots_failure.domain}")
    print(f"   Cause: {robots_failure.cause}")
    print(f"   Message: {robots_failure}")
    print()

    # Create an Error generic containing the failure
    error_result = generics.Error(robots_failure)

    print("2. Error generic wrapping the failure:")
    print(f"   Is value: {error_result.is_value()}")
    print(f"   Is error: {error_result.is_error()}")
    print()

    # Test what happens when we try to extract from the error
    print("3. Attempting to extract from Error generic:")
    try:
        extracted = error_result.extract()
        print(f"   Extract returned: {extracted}")
    except Exception as e:
        print(f"   Extract raised exception: {type(e).__name__}: {e}")
        print(f"   This is the source of the issue!")
    print()

    # Show the JSON representation for comparison
    print("4. JSON representation of the failure:")
    json_repr = robots_failure.render_as_json()
    print(f"   {json_repr}")
    print()

    print("=== Problem Analysis ===")
    print("The issue is that when robots.txt access fails:")
    print("1. The failure is wrapped in an Error generic and cached")
    print("2. When cache.access() is called, it calls result.extract()")
    print("3. Error.extract() re-raises the original exception")
    print("4. This causes the entire processor detection to fail")
    print()
    print("The commit improved error messaging but didn't change the")
    print("fundamental behavior: robots.txt failures still abort processing.")
    print()
    print("The user expects robots.txt failures to be ignored so that")
    print("the system can continue trying to process the site content.")

if __name__ == "__main__":
    analyze_error_handling()