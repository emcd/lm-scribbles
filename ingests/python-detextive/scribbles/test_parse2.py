import detextive

# Test different cases for parse_http_content_type
test_cases = [
    '',           # Empty string
    '   ',        # Whitespace only
    ';',          # Just semicolon (split would give ['', ''])
    ';charset=utf-8',  # Starts with semicolon
]

for case in test_cases:
    print(f'Input: {repr(case)}')
    result = detextive.inference.parse_http_content_type(case)
    print(f'  Result: {result}')
    print(f'  First is absent: {detextive.__.is_absent(result[0])}')
    print(f'  Split result: {case.split(";")}')
    print()