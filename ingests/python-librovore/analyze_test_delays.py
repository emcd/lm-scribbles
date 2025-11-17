#!/usr/bin/env python3
"""Analyze which tests might be causing delays by looking for unmocked asyncio.sleep calls."""

import re
import pathlib

test_file = pathlib.Path("tests/test_000_librovore/test_110_cacheproxy.py")
content = test_file.read_text()

# Find all test functions
test_functions = re.findall(r'async def (test_\d+_[^(]+)', content)

# Find tests that call functions which might trigger sleep without mocking
function_calls = re.findall(r'await module\.(retrieve_url|probe_url|_apply_request_delay)', content)

# Find tests that mock sleep vs don't mock sleep
lines = content.split('\n')
current_test = None
tests_with_mock_sleep = []
tests_with_function_calls = []

for i, line in enumerate(lines):
    if 'async def test_' in line:
        current_test = re.search(r'async def (test_\d+_[^(]+)', line)
        if current_test:
            current_test = current_test.group(1)
    
    if current_test:
        if 'mock_sleep' in line or 'patch.object.*sleep' in line:
            if current_test not in tests_with_mock_sleep:
                tests_with_mock_sleep.append(current_test)
        
        if 'await module.retrieve_url' in line or 'await module.probe_url' in line:
            if current_test not in tests_with_function_calls:
                tests_with_function_calls.append((current_test, i+1, line.strip()))

print(f"Found {len(test_functions)} test functions")
print(f"Found {len(function_calls)} function calls to retrieve_url/probe_url/_apply_request_delay")
print(f"Found {len(tests_with_mock_sleep)} tests with mocked sleep")
print(f"Found {len(tests_with_function_calls)} tests with function calls")

print("\nTests with retrieve_url/probe_url calls:")
for test, line_num, line in tests_with_function_calls:
    mocked = test in tests_with_mock_sleep
    print(f"  {test} (line {line_num}) - {'MOCKED' if mocked else 'NOT MOCKED'}")
    print(f"    {line}")

print("\nPotentially problematic tests (calls functions but doesn't mock sleep):")
for test, line_num, line in tests_with_function_calls:
    if test not in tests_with_mock_sleep:
        print(f"  {test} (line {line_num})")
        print(f"    {line}")