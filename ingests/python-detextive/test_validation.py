#!/usr/bin/env python3
"""
Test suite for text validation functionality.
Can be adapted for pytest later.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import detextive
from detextive import PROFILE_TEXTUAL, PROFILE_TERMINAL_SAFE, PROFILE_PRINTER_SAFE, PROFILE_TERMINAL_SAFE_ANSI
import traceback

def test_basic_text_validation():
    """Test basic text validation with default profile."""
    print("=== Testing Basic Text Validation ===")
    
    test_cases = [
        ("Plain ASCII", "Hello, world!", True),
        ("Unicode characters", "Café ★ résumé 中文", True),
        ("Empty string", "", True),
        ("Whitespace only", "   \n\t  ", True),
        ("Normal punctuation", "Hello! How are you? I'm fine.", True),
        ("Numbers and symbols", "Price: $19.99 (20% off)", True),
        ("Control characters", "Hello\x00\x01world", False),
        ("BOM at start", "\ufeffHello world", True),
        ("BOM in middle", "Hello\ufeff world", False),  # BOM should only be at start
        ("Delete character", "Hello\x7fworld", False),
    ]
    
    issues = []
    
    for name, text, expected in test_cases:
        try:
            is_valid = detextive.is_valid_text(text)
            if is_valid != expected:
                issues.append(f"Validation mismatch for '{name}': got {is_valid}, expected {expected}")
            print(f"✅ {name}: {is_valid} (expected {expected})")
        except Exception as e:
            issues.append(f"Failed {name}: {str(e)}")
            traceback.print_exc()
            
    return issues

def test_validation_profiles():
    """Test different validation profiles."""
    print("\n=== Testing Validation Profiles ===")
    
    issues = []
    
    test_texts = [
        ("Plain text", "Hello, world!"),
        ("Unicode symbols", "★ ♥ ♦ ♣ ♠"),
        ("Escape sequence", "Hello\x1b[31mRed\x1b[0m"),
        ("Bell character", "Alert\x07"),
        ("Various spaces", "Hello\u00a0world\u2003test"),  # Non-breaking space, em space
        ("Directional marks", "Hello\u200eworld\u200f"),  # LTR/RTL marks
    ]
    
    profiles = [
        ("TEXTUAL", PROFILE_TEXTUAL),
        ("TERMINAL_SAFE", PROFILE_TERMINAL_SAFE),
        ("PRINTER_SAFE", PROFILE_PRINTER_SAFE),
        ("TERMINAL_SAFE_ANSI", PROFILE_TERMINAL_SAFE_ANSI),
    ]
    
    for text_name, text in test_texts:
        print(f"\n  Testing: {text_name}")
        for profile_name, profile in profiles:
            try:
                is_valid = detextive.is_valid_text(text, profile=profile)
                print(f"    ✅ {profile_name}: {is_valid}")
            except Exception as e:
                issues.append(f"Failed {text_name} with {profile_name}: {str(e)}")
                traceback.print_exc()
                
    return issues

def test_validation_edge_cases():
    """Test validation edge cases."""
    print("\n=== Testing Validation Edge Cases ===")
    
    issues = []
    
    edge_cases = [
        ("Very long text", "A" * 10000),
        ("Only newlines", "\n\n\n"),
        ("Only spaces", "   "),
        ("Mixed line endings", "Line1\nLine2\r\nLine3\r"),
        ("Unicode normalization", "café" + "\u0301"),  # e + combining acute accent
        ("Zero-width chars", "Hello\u200bzero\u200cwidth\u200djoiners"),
        ("Emoji", "Hello 👋 World 🌍"),
        ("Right-to-left", "Hello العالم"),
    ]
    
    for name, text in edge_cases:
        try:
            is_valid = detextive.is_valid_text(text)
            print(f"✅ {name}: {is_valid}")
        except Exception as e:
            issues.append(f"Failed {name}: {str(e)}")
            traceback.print_exc()
            
    return issues

def test_validation_performance():
    """Test validation with large text."""
    print("\n=== Testing Validation Performance ===")
    
    issues = []
    
    try:
        # Create progressively larger text samples
        base_text = "The quick brown fox jumps over the lazy dog. " * 100
        
        sizes = [1000, 10000, 100000]
        
        for size in sizes:
            large_text = (base_text * (size // len(base_text) + 1))[:size]
            is_valid = detextive.is_valid_text(large_text)
            print(f"✅ Text size {size}: {is_valid}")
            
    except Exception as e:
        issues.append(f"Performance test failed: {str(e)}")
        traceback.print_exc()
        
    return issues

def test_profile_attributes():
    """Test validation profile attributes and behavior."""
    print("\n=== Testing Profile Attributes ===")
    
    issues = []
    
    try:
        # Test that profiles have expected attributes
        profiles = [PROFILE_TEXTUAL, PROFILE_TERMINAL_SAFE, PROFILE_PRINTER_SAFE, PROFILE_TERMINAL_SAFE_ANSI]
        
        for i, profile in enumerate(profiles):
            profile_name = ["TEXTUAL", "TERMINAL_SAFE", "PRINTER_SAFE", "TERMINAL_SAFE_ANSI"][i]
            
            # Check that profile has expected attributes
            attrs = ['acceptable_characters', 'check_bom', 'printables_ratio_min', 
                    'rejectable_characters', 'rejectable_families', 'rejectables_ratio_max']
            
            for attr in attrs:
                if not hasattr(profile, attr):
                    issues.append(f"Profile {profile_name} missing attribute: {attr}")
                else:
                    print(f"✅ {profile_name}.{attr}: {getattr(profile, attr)}")
                    
    except Exception as e:
        issues.append(f"Profile attributes test failed: {str(e)}")
        traceback.print_exc()
        
    return issues

def run_all_tests():
    """Run all validation tests."""
    print("🧪 VALIDATION TEST SUITE")
    print("=" * 50)
    
    all_issues = []
    
    all_issues.extend(test_basic_text_validation())
    all_issues.extend(test_validation_profiles())
    all_issues.extend(test_validation_edge_cases())
    all_issues.extend(test_validation_performance())
    all_issues.extend(test_profile_attributes())
    
    print("\n" + "=" * 50)
    print(f"VALIDATION TESTS COMPLETE")
    
    if all_issues:
        print(f"❌ Found {len(all_issues)} issues:")
        for issue in all_issues:
            print(f"  - {issue}")
        return all_issues
    else:
        print("✅ All validation tests passed!")
        return []

if __name__ == '__main__':
    issues = run_all_tests()
    if issues:
        sys.exit(1)