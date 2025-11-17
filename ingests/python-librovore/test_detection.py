#!/usr/bin/env python3
"""Test the detection system with real Sphinx documentation sources."""

import asyncio
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'sources'))

import sphinxmcps
from sphinxmcps import detection


async def test_sphinx_detection():
    """Test Sphinx detection with known sources."""
    
    print("=== Testing Sphinx Detection System ===\n")
    
    # Test cases: known Sphinx documentation sources
    test_sources = [
        "https://docs.python.org/3/objects.inv",
        "https://sphobjinv.readthedocs.io/en/stable/objects.inv",
        "https://httpx.readthedocs.io/en/latest/objects.inv",
        "https://example.com/nonexistent.inv",  # Should fail
    ]
    
    registry = detection.get_registry()
    
    print(f"Registered detectors: {[d.get_name() for d in registry.get_detectors()]}")
    print()
    
    for source in test_sources:
        print(f"Testing source: {source}")
        
        try:
            result = await detection.detect_source(source, cache_ttl=60)
            
            if result:
                print(f"  ✅ Detected by: {result['detector_name']}")
                print(f"  📊 Confidence: {result['confidence']:.2f}")
                print(f"  📋 Metadata: {result['metadata']}")
            else:
                print(f"  ❌ No detector can handle this source")
                
        except Exception as exc:
            print(f"  💥 Error: {exc}")
        
        print()
    
    # Test caching
    print("=== Testing Cache ===")
    print("Testing cache hit on second request...")
    
    result1 = await detection.detect_source(test_sources[0], cache_ttl=60)
    result2 = await detection.detect_source(test_sources[0], cache_ttl=60)
    
    if result1 and result2:
        print(f"  Cache working: {result1['timestamp'] == result2['timestamp']}")
    
    print()
    
    # Test local file (if available)
    print("=== Testing Local File ===")
    test_data_path = Path(__file__).parent.parent.parent / 'tests' / 'data' / 'inventories' / 'sphobjinv' / 'objects.inv'
    if test_data_path.exists():
        print(f"Testing local file: {test_data_path}")
        result = await detection.detect_source(str(test_data_path), cache_ttl=60)
        
        if result:
            print(f"  ✅ Detected by: {result['detector_name']}")
            print(f"  📊 Confidence: {result['confidence']:.2f}")
            print(f"  📋 Metadata: {result['metadata']}")
        else:
            print(f"  ❌ No detector can handle this source")
    else:
        print(f"  ⚠️  Local test file not found: {test_data_path}")


if __name__ == "__main__":
    asyncio.run(test_sphinx_detection())