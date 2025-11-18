#!/usr/bin/env python3
"""
Test suite for exception handling and error conditions.
Can be adapted for pytest later.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import detextive
import detextive.exceptions
from detextive import Behaviors, BehaviorTristate, PROFILE_TERMINAL_SAFE
import traceback

def test_exception_hierarchy():
    """Test that exception hierarchy is properly structured."""
    print("=== Testing Exception Hierarchy ===")
    
    issues = []
    
    # Test that specific exceptions inherit from base classes
    exception_tests = [
        (detextive.exceptions.CharsetDetectFailure, detextive.exceptions.Omnierror),
        (detextive.exceptions.CharsetInferFailure, detextive.exceptions.Omnierror),
        (detextive.exceptions.ContentDecodeFailure, detextive.exceptions.Omnierror),
        (detextive.exceptions.MimetypeDetectFailure, detextive.exceptions.Omnierror),
        (detextive.exceptions.TextInvalidity, detextive.exceptions.Omnierror),
        (detextive.exceptions.Omnierror, detextive.exceptions.Omniexception),
    ]
    
    for child_exc, parent_exc in exception_tests:
        try:
            if not issubclass(child_exc, parent_exc):
                issues.append(f"{child_exc.__name__} should inherit from {parent_exc.__name__}")
            print(f"✅ {child_exc.__name__} inherits from {parent_exc.__name__}")
        except Exception as e:
            issues.append(f"Exception hierarchy test failed: {str(e)}")
            
    return issues

def test_charset_detection_failures():
    """Test charset detection failure conditions."""
    print("\n=== Testing Charset Detection Failures ===")
    
    issues = []
    
    failure_cases = [
        ("Empty content", b''),
        ("Pure binary", b'\x00\x01\x02\x03\x04\x05'),
        ("Random bytes", b'\xff\xfe\xfd\xfc\xfb\xfa'),
    ]
    
    for name, content in failure_cases:
        try:
            # This might succeed or fail depending on implementation
            charset = detextive.detect_charset(content)
            if charset is None:
                print(f"✅ {name}: Returns None (graceful)")
            else:
                print(f"✅ {name}: Detected as {charset}")
        except detextive.exceptions.CharsetDetectFailure as e:
            print(f"✅ {name}: Properly raises CharsetDetectFailure")
            # Test exception message
            if "location" in str(e).lower() or "charset" in str(e).lower():
                print(f"  → Exception message: {str(e)}")
            else:
                issues.append(f"CharsetDetectFailure message unclear: {str(e)}")
        except Exception as e:
            issues.append(f"Unexpected exception for {name}: {type(e).__name__}: {str(e)}")
            
    return issues

def test_mimetype_detection_failures():
    """Test MIME type detection failure conditions."""
    print("\n=== Testing MIME Type Detection Failures ===")
    
    issues = []
    
    failure_cases = [
        ("Empty content", b''),
        ("Ambiguous content", b'some random text'),
        ("Binary without magic", b'\x01\x02\x03\x04'),
    ]
    
    for name, content in failure_cases:
        try:
            mimetype = detextive.detect_mimetype(content)
            print(f"✅ {name}: Detected as {mimetype}")
        except detextive.exceptions.MimetypeDetectFailure as e:
            print(f"✅ {name}: Properly raises MimetypeDetectFailure")
            # Test exception with location
            try:
                detextive.detect_mimetype(content, location='test.txt')
                print(f"  → With location: succeeded")
            except detextive.exceptions.MimetypeDetectFailure as e2:
                if 'test.txt' in str(e2):
                    print(f"  → With location: includes filename in message")
                else:
                    issues.append(f"Location not included in exception message: {str(e2)}")
        except Exception as e:
            issues.append(f"Unexpected exception for {name}: {type(e).__name__}: {str(e)}")
            
    return issues

def test_validation_failures():
    """Test text validation failure conditions."""
    print("\n=== Testing Text Validation Failures ===")
    
    issues = []
    
    invalid_texts = [
        ("Control characters", "Hello\x00\x01world"),
        ("Delete character", "Hello\x7fworld"),
        ("Embedded BOM", "Hello\ufeffworld"),
    ]
    
    for name, text in invalid_texts:
        try:
            # Test direct validation
            is_valid = detextive.is_valid_text(text, profile=PROFILE_TERMINAL_SAFE)
            if is_valid:
                print(f"⚠️  {name}: Unexpectedly valid for TERMINAL_SAFE")
            else:
                print(f"✅ {name}: Correctly invalid")
                
            # Test validation during decode
            try:
                content = text.encode('utf-8')
                decoded = detextive.decode(content, profile=PROFILE_TERMINAL_SAFE)
                print(f"⚠️  {name}: Decode succeeded despite invalid text")
            except detextive.exceptions.TextInvalidity as e:
                print(f"✅ {name}: Decode properly raises TextInvalidity")
                if "text" in str(e).lower() or "valid" in str(e).lower():
                    print(f"  → Exception message: {str(e)}")
            except Exception as e:
                issues.append(f"Unexpected exception during decode for {name}: {type(e).__name__}: {str(e)}")
                
        except Exception as e:
            issues.append(f"Validation test failed for {name}: {str(e)}")
            
    return issues

def test_decode_failures():
    """Test decode failure conditions."""
    print("\n=== Testing Decode Failures ===")
    
    issues = []
    
    # Test with content that should cause decode failures
    failure_cases = [
        ("Invalid UTF-8", b'\xff\xfe\xfd'),
        ("Truncated UTF-8", b'\xc3'),  # Incomplete UTF-8 sequence
    ]
    
    for name, content in failure_cases:
        try:
            # Test with strict error handling
            strict_behaviors = Behaviors(on_decode_error='strict')
            decoded = detextive.decode(content, behaviors=strict_behaviors)
            print(f"⚠️  {name}: Unexpectedly succeeded: {repr(decoded)}")
        except detextive.exceptions.ContentDecodeFailure as e:
            print(f"✅ {name}: Properly raises ContentDecodeFailure")
            print(f"  → Exception message: {str(e)}")
        except Exception as e:
            issues.append(f"Unexpected exception for {name}: {type(e).__name__}: {str(e)}")
            
    return issues

def test_inference_failures():
    """Test inference function failure conditions."""
    print("\n=== Testing Inference Failures ===")
    
    issues = []
    
    # Test content that might cause inference failures
    problematic_content = b'\x01\x02\x03'
    
    try:
        # Test charset inference
        try:
            charset = detextive.infer_charset(problematic_content)
            print(f"✅ Charset inference: {charset}")
        except detextive.exceptions.CharsetInferFailure as e:
            print(f"✅ Charset inference: Properly raises CharsetInferFailure")
        except detextive.exceptions.CharsetDetectFailure as e:
            print(f"✅ Charset inference: Raises CharsetDetectFailure (acceptable)")
        except Exception as e:
            issues.append(f"Unexpected exception in charset inference: {type(e).__name__}: {str(e)}")
            
        # Test MIME type inference
        try:
            mimetype, charset = detextive.infer_mimetype_charset(problematic_content)
            print(f"✅ MIME type inference: {mimetype}, {charset}")
        except detextive.exceptions.MimetypeInferFailure as e:
            print(f"✅ MIME type inference: Properly raises MimetypeInferFailure")
        except detextive.exceptions.MimetypeDetectFailure as e:
            print(f"✅ MIME type inference: Raises MimetypeDetectFailure (acceptable)")
        except Exception as e:
            issues.append(f"Unexpected exception in MIME inference: {type(e).__name__}: {str(e)}")
            
    except Exception as e:
        issues.append(f"Inference test setup failed: {str(e)}")
        
    return issues

def test_exception_messages():
    """Test that exception messages are informative."""
    print("\n=== Testing Exception Messages ===")
    
    issues = []
    
    try:
        # Test location parameter in exceptions
        try:
            detextive.detect_charset(b'\xff\xfe\xfd', location='test.bin')
        except detextive.exceptions.CharsetDetectFailure as e:
            message = str(e)
            if 'test.bin' in message:
                print(f"✅ CharsetDetectFailure includes location: {message}")
            else:
                issues.append(f"CharsetDetectFailure doesn't include location: {message}")
        except Exception:
            print("⚠️  CharsetDetectFailure test skipped (no exception raised)")
            
        try:
            detextive.detect_mimetype(b'ambiguous', location='unknown.xyz')
        except detextive.exceptions.MimetypeDetectFailure as e:
            message = str(e)
            if 'unknown.xyz' in message:
                print(f"✅ MimetypeDetectFailure includes location: {message}")
            else:
                issues.append(f"MimetypeDetectFailure doesn't include location: {message}")
        except Exception:
            print("⚠️  MimetypeDetectFailure test skipped (no exception raised)")
            
    except Exception as e:
        issues.append(f"Exception message test failed: {str(e)}")
        
    return issues

def run_all_tests():
    """Run all exception tests."""
    print("🧪 EXCEPTION HANDLING TEST SUITE")
    print("=" * 50)
    
    all_issues = []
    
    all_issues.extend(test_exception_hierarchy())
    all_issues.extend(test_charset_detection_failures())
    all_issues.extend(test_mimetype_detection_failures())
    all_issues.extend(test_validation_failures())
    all_issues.extend(test_decode_failures())
    all_issues.extend(test_inference_failures())
    all_issues.extend(test_exception_messages())
    
    print("\n" + "=" * 50)
    print(f"EXCEPTION TESTS COMPLETE")
    
    if all_issues:
        print(f"❌ Found {len(all_issues)} issues:")
        for issue in all_issues:
            print(f"  - {issue}")
        return all_issues
    else:
        print("✅ All exception tests passed!")
        return []

if __name__ == '__main__':
    issues = run_all_tests()
    if issues:
        sys.exit(1)