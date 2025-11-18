#!/usr/bin/env python3
"""
Analyze the _detect_mimetype_from_charset false positive problem.
"""
import sys
sys.path.insert(0, 'sources')
import detextive

# Test cases that would cause false positives
false_positive_cases = [
    (b'\x00\x01\x02', "Binary data that UTF-8 can decode"),
    (b'\x00' * 100, "Null bytes that UTF-8 accepts"),
    (b'\xff\xfe\xfd', "High bytes that might decode"),
    (b'\x80\x81\x82\x83', "Invalid UTF-8 sequences"),
]

print("=== FALSE POSITIVE ANALYSIS ===")
for content, description in false_positive_cases:
    print(f"\nCase: {description}")
    print(f"Content: {content.hex()[:20]}...")

    # Can UTF-8 decode it?
    try:
        decoded = content.decode('utf-8-sig')
        print(f"  UTF-8 decode: SUCCESS -> {repr(decoded[:20])}")

        # Would text validation catch it?
        is_valid = detextive.validation.is_valid_text(decoded)
        print(f"  Text validation: {'PASS' if is_valid else 'REJECT'}")

        # What about different profiles?
        profiles = [
            ('TEXTUAL', detextive.PROFILE_TEXTUAL),
            ('TERMINAL_SAFE', detextive.PROFILE_TERMINAL_SAFE),
        ]
        for name, profile in profiles:
            is_valid_profile = profile(decoded)
            print(f"  {name} profile: {'PASS' if is_valid_profile else 'REJECT'}")

    except UnicodeDecodeError as e:
        print(f"  UTF-8 decode: FAILED ({e})")

print("\n=== CONTENT THAT SHOULD BE TEXT/PLAIN ===")
legitimate_cases = [
    (b'Hello, world!', "Basic ASCII"),
    (b'Caf\xc3\xa9 \xe2\x98\x85', "UTF-8 with Unicode"),
    (b'   \n\t  \n', "Whitespace only"),
]

for content, description in legitimate_cases:
    print(f"\nCase: {description}")
    try:
        decoded = content.decode('utf-8-sig')
        is_valid = detextive.validation.is_valid_text(decoded)
        print(f"  Decoded: {repr(decoded)}")
        print(f"  Text validation: {'PASS' if is_valid else 'REJECT'}")
    except UnicodeDecodeError as e:
        print(f"  UTF-8 decode: FAILED ({e})")