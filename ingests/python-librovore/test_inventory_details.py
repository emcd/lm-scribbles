#!/usr/bin/env python3
"""
Test sphobjinv inventory loading and data structure details.
"""

import sphobjinv
from pathlib import Path

def analyze_inventory_object(obj):
    """Analyze a single inventory object."""
    print(f"  Object: {obj}")
    print(f"    Type: {type(obj)}")
    print(f"    Name: {obj.name}")
    print(f"    Domain: {obj.domain}")
    print(f"    Role: {obj.role}")
    print(f"    Priority: {obj.priority}")
    print(f"    URI: {obj.uri}")
    print(f"    Display Name: {obj.dispname}")
    return obj

def test_local_file_loading():
    """Test loading from a local file path."""
    print("=== Testing Local File Loading ===\n")
    
    # Let's try loading from our own project's documentation if it exists
    possible_paths = [
        ".auxiliary/artifacts/sphinx-html/objects.inv",
        "documentation/_build/html/objects.inv",
        "docs/_build/html/objects.inv"
    ]
    
    for path_str in possible_paths:
        path = Path(path_str)
        if path.exists():
            print(f"Found local inventory at: {path}")
            try:
                inv = sphobjinv.Inventory(fname_zlib=str(path))
                print(f"Loaded local inventory:")
                print(f"  Project: {inv.project}")
                print(f"  Version: {inv.version}")
                print(f"  Object count: {len(inv.objects)}")
                return inv
            except Exception as e:
                print(f"Error loading local inventory: {e}")
        else:
            print(f"Path not found: {path}")
    
    print("No local inventories found")
    return None

def test_url_variations():
    """Test different ways to load from URLs."""
    print("\n=== Testing URL Variations ===\n")
    
    # Test with a few different documentation sites
    test_urls = [
        "https://docs.python.org/3/objects.inv",
        "https://sphobjinv.readthedocs.io/en/latest/objects.inv",
        # Add file:// URL if we find a local file
    ]
    
    for url in test_urls:
        print(f"Testing URL: {url}")
        try:
            inv = sphobjinv.Inventory(url=url)
            print(f"  Success! Project: {inv.project}, Objects: {len(inv.objects)}")
            
            # Analyze a few objects
            print("  Sample objects:")
            for obj in inv.objects[:3]:
                analyze_inventory_object(obj)
                print()
            break  # Stop after first successful load
            
        except Exception as e:
            print(f"  Failed: {e}")

def test_data_extraction():
    """Test extracting useful data from inventory."""
    print("\n=== Testing Data Extraction ===\n")
    
    try:
        # Load Python docs
        inv = sphobjinv.Inventory(url="https://docs.python.org/3/objects.inv")
        
        # Group by domain
        domains = {}
        for obj in inv.objects:
            domain = obj.domain
            if domain not in domains:
                domains[domain] = []
            domains[domain].append(obj)
        
        print("Domains found:")
        for domain, objs in domains.items():
            print(f"  {domain}: {len(objs)} objects")
        
        # Look at Python-specific objects
        if 'py' in domains:
            py_roles = {}
            for obj in domains['py']:
                role = obj.role
                if role not in py_roles:
                    py_roles[role] = []
                py_roles[role].append(obj)
            
            print("\nPython domain roles:")
            for role, objs in py_roles.items():
                print(f"  {role}: {len(objs)} objects")
                # Show first example
                if objs:
                    print(f"    Example: {objs[0].name}")
        
    except Exception as e:
        print(f"Error in data extraction: {e}")

if __name__ == "__main__":
    test_local_file_loading()
    test_url_variations()
    test_data_extraction()