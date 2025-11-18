#!/usr/bin/env python3
"""
Specific test to find charset detection inconsistencies between methods.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import detextive
from detextive.core import BEHAVIORS_DEFAULT

def test_detection_method_consistency():
    """Compare detect_charset vs infer_charset for various content."""
    print("=== Charset Detection Method Consistency ===")

    # Test cases that might show inconsistencies
    test_cases = [
        ("Empty content", b''),
        ("ASCII", b'Hello world'),
        ("UTF-8 simple", 'Café'.encode('utf-8')),
        ("UTF-8 complex", 'Unicode ★ symbols'.encode('utf-8')),
        ("Binary-like", b'\x01\x02\x03\x04'),
        ("Mixed content", b'Hello\x00World'),
        ("Windows-1252 content", 'Smart "quotes"'.encode('windows-1252')),
        ("ISO-8859-1 content", 'Café résumé'.encode('iso-8859-1')),
        ("Long ASCII", b'A' * 1000),
        ("Short Unicode", '★'.encode('utf-8')),
        ("Medium content", 'This is a longer text with some üñíčódé characters'.encode('utf-8')),
    ]

    inconsistencies = []

    for name, content in test_cases:
        print(f"\\n{name}: {content[:20]}...")

        try:
            # Method 1: detect_charset
            charset1 = detextive.detect_charset(content)
            charset_conf1 = detextive.detect_charset_confidence(content)

            # Method 2: infer_charset
            charset2 = detextive.infer_charset(content)
            charset_conf2 = detextive.infer_charset_confidence(content)

            print(f"  detect_charset(): {charset1}")
            print(f"  infer_charset(): {charset2}")

            if charset_conf1:
                print(f"  detect_charset_confidence(): {charset_conf1.value} (conf: {charset_conf1.confidence:.3f})")
            else:
                print(f"  detect_charset_confidence(): None")

            if charset_conf2:
                print(f"  infer_charset_confidence(): {charset_conf2.value} (conf: {charset_conf2.confidence:.3f})")
            else:
                print(f"  infer_charset_confidence(): None")

            # Check for inconsistencies
            if charset1 != charset2:
                print(f"  *** INCONSISTENCY: charset values differ ***")
                inconsistencies.append({
                    'name': name,
                    'detect_charset': charset1,
                    'infer_charset': charset2,
                    'type': 'charset_value'
                })

            if charset_conf1 and charset_conf2:
                if charset_conf1.value != charset_conf2.value:
                    print(f"  *** INCONSISTENCY: confidence charset values differ ***")
                    inconsistencies.append({
                        'name': name,
                        'detect_charset_conf': charset_conf1.value,
                        'infer_charset_conf': charset_conf2.value,
                        'type': 'confidence_charset'
                    })

                if abs(charset_conf1.confidence - charset_conf2.confidence) > 0.001:
                    print(f"  *** INCONSISTENCY: confidence levels differ ***")
                    inconsistencies.append({
                        'name': name,
                        'detect_conf': charset_conf1.confidence,
                        'infer_conf': charset_conf2.confidence,
                        'type': 'confidence_level'
                    })

        except Exception as e:
            print(f"  ERROR: {e}")
            inconsistencies.append({
                'name': name,
                'error': str(e),
                'type': 'exception'
            })

    return inconsistencies

def test_with_different_contexts():
    """Test charset detection with different context parameters."""
    print("\\n\\n=== Context-Dependent Detection ===")

    test_content = 'Hello ★ world'.encode('utf-8')

    print(f"Content: {test_content}")

    contexts = [
        ("No context", {}),
        ("With mimetype", {'mimetype': 'text/plain'}),
        ("With location", {'location': 'test.txt'}),
        ("With both", {'mimetype': 'text/plain', 'location': 'test.txt'}),
        ("With HTTP header", {'http_content_type': 'text/plain; charset=utf-8'}),
        ("With defaults", {'charset_default': 'utf-8', 'mimetype_default': 'text/plain'}),
    ]

    results = {}

    for name, kwargs in contexts:
        print(f"\\n{name}:")
        try:
            # Only test methods that support these parameters
            if 'http_content_type' in kwargs or 'mimetype_default' in kwargs:
                # infer_charset supports these
                if 'http_content_type' in kwargs:
                    charset = detextive.infer_charset(test_content, http_content_type=kwargs['http_content_type'])
                elif 'mimetype_default' in kwargs and 'charset_default' in kwargs:
                    charset = detextive.infer_charset(
                        test_content,
                        mimetype_default=kwargs['mimetype_default'],
                        charset_default=kwargs['charset_default']
                    )
                else:
                    charset = detextive.infer_charset(test_content)
                print(f"  infer_charset(): {charset}")
            else:
                # Both methods support these basic parameters
                detect_kwargs = {}
                infer_kwargs = {}

                if 'mimetype' in kwargs:
                    detect_kwargs['mimetype'] = kwargs['mimetype']
                if 'location' in kwargs:
                    detect_kwargs['location'] = kwargs['location']
                    infer_kwargs['location'] = kwargs['location']

                charset1 = detextive.detect_charset(test_content, **detect_kwargs)
                charset2 = detextive.infer_charset(test_content, **infer_kwargs)

                print(f"  detect_charset(): {charset1}")
                print(f"  infer_charset(): {charset2}")

                if charset1 != charset2:
                    print(f"  *** CONTEXT-DEPENDENT INCONSISTENCY ***")

        except Exception as e:
            print(f"  ERROR: {e}")

def test_edge_case_inconsistencies():
    """Test specific edge cases that might show inconsistencies."""
    print("\\n\\n=== Edge Case Inconsistency Tests ===")

    edge_cases = [
        ("UTF-8 BOM", '\\ufeffHello'.encode('utf-8-sig')),
        ("Only BOM", '\\ufeff'.encode('utf-8-sig')),
        ("Latin-1 vs Windows-1252", 'café résumé naïve'.encode('latin-1')),
        ("High-confidence wrong detection", 'Unicode ★ symbols'.encode('utf-8')),
        ("Low-confidence detection", bytes([0x80, 0x81, 0x82, 0x83, 0x84])),
        ("ASCII vs UTF-8 promotion", b'Hello world'),
    ]

    for name, content in edge_cases:
        print(f"\\n{name}:")

        try:
            charset1 = detextive.detect_charset(content)
            charset2 = detextive.infer_charset(content)

            conf1 = detextive.detect_charset_confidence(content)
            conf2 = detextive.infer_charset_confidence(content)

            print(f"  detect_charset(): {charset1}")
            print(f"  infer_charset(): {charset2}")

            if conf1:
                print(f"  detect confidence: {conf1.confidence:.3f}")
            if conf2:
                print(f"  infer confidence: {conf2.confidence:.3f}")

            if charset1 != charset2:
                print(f"  *** EDGE CASE INCONSISTENCY ***")

        except Exception as e:
            print(f"  ERROR: {e}")

if __name__ == '__main__':
    inconsistencies = test_detection_method_consistency()
    test_with_different_contexts()
    test_edge_case_inconsistencies()

    print("\\n\\n=== INCONSISTENCY SUMMARY ===")
    if inconsistencies:
        print(f"Found {len(inconsistencies)} inconsistencies:")
        for inc in inconsistencies:
            print(f"  {inc['name']}: {inc['type']}")
            if inc['type'] == 'charset_value':
                print(f"    detect_charset: {inc['detect_charset']}")
                print(f"    infer_charset: {inc['infer_charset']}")
    else:
        print("No inconsistencies found in basic tests")