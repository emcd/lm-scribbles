#!/usr/bin/env python3
"""
Exploration script for sphobjinv library to understand its API and capabilities.
"""

import sphobjinv

def explore_sphobjinv():
    """Explore sphobjinv module structure and capabilities."""
    print("=== sphobjinv Module Exploration ===\n")
    
    print("Module attributes:")
    for attr in dir(sphobjinv):
        if not attr.startswith('_'):
            obj = getattr(sphobjinv, attr)
            print(f"  {attr}: {type(obj)} - {getattr(obj, '__doc__', 'No docstring')}")
    
    print("\n=== Key Classes/Functions ===\n")
    
    # Check if Inventory class exists
    if hasattr(sphobjinv, 'Inventory'):
        print("Inventory class found:")
        inv_class = sphobjinv.Inventory
        print(f"  Docstring: {inv_class.__doc__}")
        print("  Methods:")
        for method in dir(inv_class):
            if not method.startswith('_'):
                print(f"    {method}")
    
    # Check for utility functions
    for name in ['read_file', 'read_url', 'write_plaintext', 'compress', 'decompress']:
        if hasattr(sphobjinv, name):
            func = getattr(sphobjinv, name)
            print(f"\n{name}:")
            print(f"  {func.__doc__}")

def test_inventory_loading():
    """Test loading an inventory from a real Sphinx site."""
    print("\n=== Testing Inventory Loading ===\n")
    
    # Test with sphobjinv documentation (should be much smaller)
    test_url = "https://sphobjinv.readthedocs.io/en/stable/objects.inv"
    print(f"Attempting to load inventory from: {test_url}")
    
    try:
        # Try different approaches based on API
        if hasattr(sphobjinv, 'Inventory'):
            print("Using Inventory class...")
            inv = sphobjinv.Inventory(url=test_url)
            print(f"Loaded inventory with {len(inv.objects)} objects")
            print(f"Project: {inv.project}")
            print(f"Version: {inv.version}")
            
            # Show first few objects
            print("\nFirst 5 objects:")
            for i, obj in enumerate(inv.objects[:5]):
                print(f"  {obj}")
                
            return inv  # Return inventory for further testing
                
        elif hasattr(sphobjinv, 'read_url'):
            print("Using read_url function...")
            inv = sphobjinv.read_url(test_url)
            print(f"Loaded: {type(inv)}")
            return inv
            
    except Exception as e:
        print(f"Error loading inventory: {e}")
        print("This might be expected if we need different parameters")
        return None

def explore_fuzzy_matching():
    """Investigate fuzzy matching capabilities in sphobjinv."""
    print("\n=== Fuzzy Matching Investigation ===\n")
    
    # Check what fuzzy matching dependencies are available
    print("Checking fuzzy matching dependencies:")
    
    try:
        import fuzzywuzzy
        print(f"✓ fuzzywuzzy available: {fuzzywuzzy.__version__}")
        
        # Check if process module exists (main fuzzy matching interface)
        if hasattr(fuzzywuzzy, 'process'):
            print("✓ fuzzywuzzy.process module found")
            process = fuzzywuzzy.process
            print(f"  Available functions: {[f for f in dir(process) if not f.startswith('_')]}")
        
        if hasattr(fuzzywuzzy, 'fuzz'):
            print("✓ fuzzywuzzy.fuzz module found")
            fuzz = fuzzywuzzy.fuzz
            print(f"  Available functions: {[f for f in dir(fuzz) if not f.startswith('_')]}")
            
    except ImportError:
        print("✗ fuzzywuzzy not available")
    
    try:
        import rapidfuzz
        print(f"✓ rapidfuzz available: {rapidfuzz.__version__}")
        print(f"  Available functions: {[f for f in dir(rapidfuzz) if not f.startswith('_')]}")
    except ImportError:
        print("✗ rapidfuzz not available")
    
    # Check if sphobjinv has fuzzy matching built-in
    print("\nChecking sphobjinv for fuzzy matching:")
    
    # Look for fuzzy-related methods in sphobjinv
    fuzzy_attrs = []
    for attr in dir(sphobjinv):
        if 'fuzzy' in attr.lower() or 'match' in attr.lower():
            fuzzy_attrs.append(attr)
    
    if fuzzy_attrs:
        print(f"Found fuzzy-related attributes: {fuzzy_attrs}")
        for attr in fuzzy_attrs:
            obj = getattr(sphobjinv, attr)
            print(f"  {attr}: {type(obj)} - {getattr(obj, '__doc__', 'No docstring')}")
    else:
        print("No obvious fuzzy matching functions found in sphobjinv")
    
    # Check Inventory class for fuzzy methods
    if hasattr(sphobjinv, 'Inventory'):
        inv_class = sphobjinv.Inventory
        fuzzy_methods = []
        for method in dir(inv_class):
            if 'fuzzy' in method.lower() or 'match' in method.lower() or 'search' in method.lower():
                fuzzy_methods.append(method)
        
        if fuzzy_methods:
            print(f"Found fuzzy/search methods in Inventory: {fuzzy_methods}")
            for method in fuzzy_methods:
                method_obj = getattr(inv_class, method)
                print(f"  {method}: {getattr(method_obj, '__doc__', 'No docstring')}")
        else:
            print("No fuzzy/search methods found in Inventory class")


def test_sphobjinv_suggest(inv):
    """Test the built-in suggest method in sphobjinv."""
    if not inv:
        print("No inventory available for suggest testing")
        return
    
    print("\n=== Testing sphobjinv.suggest() Method ===\n")
    
    # Test the suggest method
    if hasattr(inv, 'suggest'):
        print("✓ suggest method found on Inventory object")
        print(f"suggest method docstring: {inv.suggest.__doc__}")
        
        # Test with various queries more relevant to sphobjinv
        test_queries = [
            "Inventory",        # exact match
            "inventory",        # case variation  
            "Inventorry",       # typo
            "DataObj",          # partial match
            "suggest",          # method name
            "compress",         # function name
            "nonexistent",      # no match
        ]
        
        print("\nTesting suggest with various queries:")
        for query in test_queries:
            try:
                suggestions = inv.suggest(query)
                print(f"Query '{query}': {suggestions}")
            except Exception as e:
                print(f"Query '{query}': Error - {e}")
                
        # Test with limit parameter if supported
        print("\nTesting suggest with limit parameter:")
        try:
            suggestions = inv.suggest("dict", limit=5)
            print(f"Query 'dict' (limit=5): {suggestions}")
        except Exception as e:
            print(f"Query 'dict' (limit=5): Error - {e}")
            
    else:
        print("✗ suggest method not found on Inventory object")


def explore_priority_values(inv):
    """Investigate priority field values in Sphinx inventory objects."""
    if not inv:
        print("No inventory available for priority exploration")
        return
    
    print("\n=== Priority Field Investigation ===\n")
    
    # Collect all unique priority values
    priorities = set()
    priority_examples = {}
    
    print("Sample objects with their priority values:")
    for i, obj in enumerate(inv.objects[:10]):
        print(f"  {obj.name} (domain={obj.domain}, role={obj.role}, priority={obj.priority})")
        priorities.add(obj.priority)
        
        # Store example for each priority
        if obj.priority not in priority_examples:
            priority_examples[obj.priority] = obj
    
    print(f"\nUnique priority values found: {sorted(priorities)}")
    
    # Group objects by priority to understand distribution
    priority_counts = {}
    for obj in inv.objects:
        priority = obj.priority
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    print("\nPriority distribution:")
    for priority in sorted(priority_counts.keys()):
        count = priority_counts[priority]
        # Find an example for this priority
        example_obj = None
        for obj in inv.objects:
            if obj.priority == priority:
                example_obj = obj
                break
        if example_obj:
            print(f"  Priority {priority}: {count} objects (e.g., {example_obj.domain}:{example_obj.role}:`{example_obj.name}`)")
        else:
            print(f"  Priority {priority}: {count} objects")
    
    print(f"\nTotal objects analyzed: {len(inv.objects)}")
    
    # Explain what priority means in Sphinx context
    print("\n=== Understanding Sphinx Priority ===")
    print("In Sphinx inventories, priority is typically used for:")
    print("- Controlling search result ranking")
    print("- Resolving ambiguous cross-references") 
    print("- Higher numbers = higher priority in search results")
    print("- Default priority is often 1")
    print("- Special objects may have higher priorities (0, -1, etc.)")
    
    return priority_counts


def test_fuzzy_matching():
    """Test fuzzy matching if available."""
    print("\n=== Testing External Fuzzy Matching ===\n")
    
    # Test data - some Python stdlib module names with variations
    test_objects = [
        "collections.OrderedDict",
        "collections.defaultdict", 
        "collections.Counter",
        "itertools.chain",
        "itertools.combinations",
        "os.path.join",
        "os.path.exists",
        "sys.argv",
        "sys.path"
    ]
    
    test_queries = [
        "OrderedDict",      # exact match
        "ordereddict",      # case variation
        "OrderDict",        # typo
        "defaultdic",       # missing char
        "itertool",         # missing s
        "pathexist",        # missing dot
    ]
    
    print("Test objects:", test_objects)
    print("Test queries:", test_queries)
    
    # Test with fuzzywuzzy if available
    try:
        from fuzzywuzzy import process
        print("\n--- Testing with fuzzywuzzy ---")
        
        for query in test_queries:
            matches = process.extract(query, test_objects, limit=3)
            print(f"Query '{query}': {matches}")
            
    except ImportError:
        print("fuzzywuzzy not available for testing")
    
    # Test with rapidfuzz if available
    try:
        from rapidfuzz import process as rf_process
        print("\n--- Testing with rapidfuzz ---")
        
        for query in test_queries:
            matches = rf_process.extract(query, test_objects, limit=3)
            print(f"Query '{query}': {matches}")
            
    except ImportError:
        print("rapidfuzz not available for testing")


if __name__ == "__main__":
    explore_sphobjinv()
    inv = test_inventory_loading()
    explore_fuzzy_matching()
    test_sphobjinv_suggest(inv)
    explore_priority_values(inv)
    test_fuzzy_matching()