#!/usr/bin/env python3

"""
Manual verification of enhanced search functionality
"""

import sys
sys.path.insert(0, 'sources')

from librovore import search, interfaces

# Simple mock object with just the name attribute for search testing
class MockInventoryObject:
    def __init__(self, name):
        self.name = name

# Create sample test objects
sample_objects = [
    MockInventoryObject('create_mutex_group'),
    MockInventoryObject('tyro.conf.mutex_group'),
    MockInventoryObject('example_mutex_14'),
    MockInventoryObject('exact_match'),
]

def test_enhanced_similar_search():
    """Test enhanced similar search with partial_ratio discovery"""
    print("🔍 Testing Enhanced Similar Search...")
    
    search_behaviors = interfaces.SearchBehaviors(
        match_mode=interfaces.MatchMode.Similar,
        fuzzy_threshold=50
    )
    
    results_search = search.filter_by_name(
        sample_objects, 'mutex',
        search_behaviors=search_behaviors
    )
    
    print(f"✅ Found {len(results_search)} matches for 'mutex':")
    for result in results_search:
        print(f"   - {result.inventory_object.name} (score: {result.score:.2f}, reason: {result.match_reasons[0]})")
    
    # Verify we found the expected mutex objects (may find more due to partial matches)
    result_names = [result.inventory_object.name for result in results_search]
    expected = ['create_mutex_group', 'tyro.conf.mutex_group', 'example_mutex_14']
    
    found_expected = 0
    for expected_name in expected:
        if expected_name in result_names:
            print(f"✅ Found expected object: {expected_name}")
            found_expected += 1
        else:
            print(f"❌ Missing expected object: {expected_name}")
    
    # Success if we found all expected objects (may find additional due to enhanced discovery)
    return found_expected == 3

def test_exact_with_contains_term():
    """Test exact mode with contains_term flag"""
    print("\n🎯 Testing Exact Mode with contains_term...")
    
    search_behaviors = interfaces.SearchBehaviors(
        match_mode=interfaces.MatchMode.Exact
    )
    
    # Without contains_term
    results_without = search.filter_by_name(
        sample_objects, 'mutex',
        search_behaviors=search_behaviors,
        contains_term=False
    )
    print(f"✅ Without contains_term: {len(results_without)} matches")
    
    # With contains_term
    results_with = search.filter_by_name(
        sample_objects, 'mutex',
        search_behaviors=search_behaviors,
        contains_term=True
    )
    print(f"✅ With contains_term: {len(results_with)} matches")
    
    return len(results_without) == 0 and len(results_with) == 3

def test_case_sensitivity():
    """Test case sensitivity control"""
    print("\n🔤 Testing Case Sensitivity...")
    
    search_behaviors = interfaces.SearchBehaviors(
        match_mode=interfaces.MatchMode.Exact
    )
    
    # Case insensitive (default)
    results_insensitive = search.filter_by_name(
        sample_objects, 'MUTEX',
        search_behaviors=search_behaviors,
        contains_term=True,
        case_sensitive=False
    )
    print(f"✅ Case insensitive 'MUTEX': {len(results_insensitive)} matches")
    
    # Case sensitive
    results_sensitive = search.filter_by_name(
        sample_objects, 'MUTEX',
        search_behaviors=search_behaviors,
        contains_term=True,
        case_sensitive=True
    )
    print(f"✅ Case sensitive 'MUTEX': {len(results_sensitive)} matches")
    
    return len(results_insensitive) == 3 and len(results_sensitive) == 0

if __name__ == '__main__':
    print("🚀 Manual Enhanced Search Functionality Test\n")
    
    test1 = test_enhanced_similar_search()
    test2 = test_exact_with_contains_term()  
    test3 = test_case_sensitivity()
    
    print(f"\n📋 Test Results:")
    print(f"   Enhanced Similar Search: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"   Exact with contains_term: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"   Case Sensitivity: {'✅ PASS' if test3 else '❌ FAIL'}")
    
    if all([test1, test2, test3]):
        print("\n🎉 All enhanced search functionality tests PASSED!")
        sys.exit(0)
    else:
        print("\n💥 Some tests FAILED!")
        sys.exit(1)