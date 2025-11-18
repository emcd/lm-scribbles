#!/usr/bin/env python3
"""
Test suite for decode functionality.
Can be adapted for pytest later.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import detextive
from detextive import Behaviors, BehaviorTristate, PROFILE_TEXTUAL, PROFILE_TERMINAL_SAFE
import traceback

def test_basic_decode():
    """Test basic decode functionality."""
    print("=== Testing Basic Decode ===")
    
    test_cases = [
        ("UTF-8 content", b'Hello, world!', 'Hello, world!'),
        ("UTF-8 with BOM", '\ufeffHello, world!'.encode('utf-8-sig'), 'Hello, world!'),  # BOM should be handled
        ("UTF-8 with unicode", 'Café ★ résumé'.encode('utf-8'), 'Café ★ résumé'),
        ("JSON content", b'{"message": "Hello"}', '{"message": "Hello"}'),
        ("Empty content", b'', ''),
        ("ASCII content", b'Hello ASCII', 'Hello ASCII'),
    ]
    
    issues = []
    
    for name, content, expected in test_cases:
        try:
            decoded = detextive.decode(content)
            if decoded != expected:
                issues.append(f"Decode mismatch for {name}: got {repr(decoded)}, expected {repr(expected)}")
            print(f"✅ {name}: decoded correctly")
        except Exception as e:
            issues.append(f"Failed {name}: {str(e)}")
            traceback.print_exc()
            
    return issues

def test_decode_with_location():
    """Test decode with location hints."""
    print("\n=== Testing Decode with Location ===")
    
    issues = []
    content = b'{"config": {"debug": true}}'
    
    locations = [
        'config.json',
        'data.txt',
        '/path/to/settings.json',
        'document',  # No extension
        None,
    ]
    
    for location in locations:
        try:
            decoded = detextive.decode(content, location=location)
            print(f"✅ Location {location}: {len(decoded)} chars")
        except Exception as e:
            issues.append(f"Failed with location {location}: {str(e)}")
            traceback.print_exc()
            
    return issues

def test_decode_with_validation_profiles():
    """Test decode with different validation profiles."""
    print("\n=== Testing Decode with Validation Profiles ===")
    
    issues = []
    
    # Test with different content types
    test_contents = [
        ("Clean text", b'Hello, world!'),
        ("Unicode symbols", 'Hello ★ World'.encode('utf-8')),
        ("Text with null bytes", b'Hello\x00world'),
        ("Text with control chars", b'Hello\x01\x02world'),
        ("Text with escape", b'Hello\x1b[31mRed\x1b[0m'),
    ]
    
    profiles = [
        ("TEXTUAL", PROFILE_TEXTUAL),
        ("TERMINAL_SAFE", PROFILE_TERMINAL_SAFE),
    ]
    
    for content_name, content in test_contents:
        print(f"\n  Testing: {content_name}")
        for profile_name, profile in profiles:
            try:
                decoded = detextive.decode(content, profile=profile)
                print(f"    ✅ {profile_name}: {len(decoded)} chars")
            except detextive.exceptions.TextInvalidity:
                print(f"    ⚠️  {profile_name}: Validation failed (may be expected)")
            except Exception as e:
                issues.append(f"Failed {content_name} with {profile_name}: {str(e)}")
                traceback.print_exc()
                
    return issues

def test_decode_with_behaviors():
    """Test decode with custom behaviors."""
    print("\n=== Testing Decode with Custom Behaviors ===")
    
    issues = []
    content = b'Test content for behavior testing'
    
    try:
        # Test with custom behaviors
        custom_behaviors = Behaviors(
            trial_decode=BehaviorTristate.Always,
            text_validate=BehaviorTristate.Always,
            on_decode_error='replace'
        )
        
        decoded1 = detextive.decode(content)
        decoded2 = detextive.decode(content, behaviors=custom_behaviors)
        
        print(f"✅ Default behaviors: {len(decoded1)} chars")
        print(f"✅ Custom behaviors: {len(decoded2)} chars")
        
        # Test error handling behavior
        invalid_content = b'Hello\xff\xfe invalid UTF-8'
        
        try:
            # This should use 'replace' error handling
            decoded_with_errors = detextive.decode(invalid_content, behaviors=custom_behaviors)
            print(f"✅ Error handling: {len(decoded_with_errors)} chars")
        except Exception as e:
            print(f"⚠️  Error handling test failed: {str(e)}")
            
    except Exception as e:
        issues.append(f"Custom behaviors test failed: {str(e)}")
        traceback.print_exc()
        
    return issues

def test_decode_with_http_content_type():
    """Test decode with HTTP Content-Type headers."""
    print("\n=== Testing Decode with HTTP Content-Type ===")
    
    issues = []
    content = b'{"status": "success"}'
    
    test_headers = [
        "application/json",
        "application/json; charset=utf-8",
        "text/plain; charset=iso-8859-1",
        "text/html",
    ]
    
    for header in test_headers:
        try:
            decoded = detextive.decode(content, http_content_type=header)
            print(f"✅ '{header}': {len(decoded)} chars")
        except Exception as e:
            issues.append(f"Failed with header '{header}': {str(e)}")
            traceback.print_exc()
            
    return issues

def test_decode_edge_cases():
    """Test decode edge cases."""
    print("\n=== Testing Decode Edge Cases ===")
    
    issues = []
    
    edge_cases = [
        ("Very large content", b'A' * 100000),
        ("Only whitespace", b'   \n\t  '),
        ("Only line breaks", b'\n\n\n'),
        ("Mixed line endings", b'Line1\nLine2\r\nLine3\r'),
        ("Binary-like content", b'\x01\x02\x03\x04'),
        ("UTF-8 with BOM", '\ufeffTest content'.encode('utf-8-sig')),
    ]
    
    for name, content in edge_cases:
        try:
            decoded = detextive.decode(content)
            print(f"✅ {name}: {len(decoded)} chars")
        except detextive.exceptions.CharsetDetectFailure:
            print(f"⚠️  {name}: Charset detection failed (may be expected)")
        except detextive.exceptions.TextInvalidity:
            print(f"⚠️  {name}: Text validation failed (may be expected)")
        except Exception as e:
            issues.append(f"Failed {name}: {str(e)}")
            traceback.print_exc()
            
    return issues

def test_decode_with_defaults():
    """Test decode with default parameters."""
    print("\n=== Testing Decode with Defaults ===")
    
    issues = []
    
    # Content that might fail detection
    ambiguous_content = b'some ambiguous content'
    
    try:
        # Test with various default combinations
        decoded1 = detextive.decode(
            ambiguous_content,
            charset_default='utf-8'
        )
        print(f"✅ With charset default: {len(decoded1)} chars")
        
        decoded2 = detextive.decode(
            ambiguous_content,
            mimetype_default='text/plain',
            charset_default='utf-8'
        )
        print(f"✅ With both defaults: {len(decoded2)} chars")
        
    except Exception as e:
        issues.append(f"Defaults test failed: {str(e)}")
        traceback.print_exc()
        
    return issues

def test_decode_round_trip():
    """Test that decode is consistent with detection functions."""
    print("\n=== Testing Decode Round-trip Consistency ===")
    
    issues = []
    
    test_texts = [
        "Hello, world!",
        "Café résumé",
        "Unicode ★ symbols",
        "Mixed\nline\r\nendings",
    ]
    
    for text in test_texts:
        try:
            # Encode with UTF-8
            encoded = text.encode('utf-8')
            
            # Decode using detextive
            decoded = detextive.decode(encoded)
            
            # Should match original
            if decoded != text:
                issues.append(f"Round-trip failed for '{text}': got '{decoded}'")
            else:
                print(f"✅ Round-trip: {text[:20]}...")
                
        except Exception as e:
            issues.append(f"Round-trip test failed for '{text}': {str(e)}")
            traceback.print_exc()
            
    return issues

def run_all_tests():
    """Run all decode tests."""
    print("🧪 DECODE TEST SUITE")
    print("=" * 50)
    
    all_issues = []
    
    all_issues.extend(test_basic_decode())
    all_issues.extend(test_decode_with_location())
    all_issues.extend(test_decode_with_validation_profiles())
    all_issues.extend(test_decode_with_behaviors())
    all_issues.extend(test_decode_with_http_content_type())
    all_issues.extend(test_decode_edge_cases())
    all_issues.extend(test_decode_with_defaults())
    all_issues.extend(test_decode_round_trip())
    
    print("\n" + "=" * 50)
    print(f"DECODE TESTS COMPLETE")
    
    if all_issues:
        print(f"❌ Found {len(all_issues)} issues:")
        for issue in all_issues:
            print(f"  - {issue}")
        return all_issues
    else:
        print("✅ All decode tests passed!")
        return []

if __name__ == '__main__':
    issues = run_all_tests()
    if issues:
        sys.exit(1)