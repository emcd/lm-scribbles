#!/usr/bin/env python3
"""Benchmark inventory parsing performance."""

import sys
import time
from pathlib import Path

# Add tests to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'tests'))

import sphinxmcps.functions as module
from test_000_sphinxmcps.fixtures import get_test_inventory_path

def benchmark_single_extraction():
    """Time a single inventory extraction."""
    inventory_path = get_test_inventory_path('sphobjinv')
    start = time.time()
    result = module.extract_inventory(inventory_path)
    end = time.time()
    
    print(f"Single extraction: {result['object_count']} objects in {(end-start)*1000:.1f}ms")
    return end - start

def benchmark_multiple_extractions():
    """Time multiple extractions to see caching effects."""
    inventory_path = get_test_inventory_path('sphobjinv')
    times = []
    
    for i in range(5):
        start = time.time()
        result = module.extract_inventory(inventory_path)
        end = time.time()
        times.append(end - start)
        print(f"Extraction {i+1}: {(end-start)*1000:.1f}ms")
    
    avg_time = sum(times) / len(times)
    print(f"Average: {avg_time*1000:.1f}ms")
    return times

if __name__ == "__main__":
    print("=== Inventory Parsing Performance ===")
    
    print("\n1. Single extraction:")
    single_time = benchmark_single_extraction()
    
    print("\n2. Multiple extractions:")
    multiple_times = benchmark_multiple_extractions()
    
    print(f"\nAnalysis:")
    print(f"- Single extraction: {single_time*1000:.1f}ms")
    print(f"- Variation: {min(multiple_times)*1000:.1f}ms - {max(multiple_times)*1000:.1f}ms")