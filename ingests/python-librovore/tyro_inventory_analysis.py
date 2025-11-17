#!/usr/bin/env python3
"""
Script to analyze Tyro documentation inventory for mutex-related objects.

This script will:
1. Query the complete inventory from the Tyro site
2. Search for any objects containing 'mutex' in their names
3. Display all matches with detailed object information
4. Provide summary statistics about the inventory
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the librovore source to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "sources"))

from librovore import functions as _functions
from librovore import state as _state
from librovore import interfaces as _interfaces


async def analyze_tyro_inventory():
    """Analyze the complete Tyro inventory for mutex references."""
    
    # Initialize librovore state
    auxdata = _state.Globals()
    
    location = "https://brentyi.github.io/tyro/"
    
    print("=" * 60)
    print("TYRO INVENTORY ANALYSIS")
    print("=" * 60)
    print(f"Location: {location}")
    print()
    
    try:
        # Query with empty string to get ALL inventory objects
        result = await _functions.query_inventory(
            auxdata=auxdata,
            location=location,
            term="",  # Empty term should return all objects
            results_max=10000  # High limit to get complete inventory
        )
        
        print(f"Total inventory objects found: {len(result.objects)}")
        print()
        
        # Search for mutex-related objects
        mutex_objects = []
        for obj in result.objects:
            if 'mutex' in obj.name.lower():
                mutex_objects.append(obj)
        
        print(f"Objects containing 'mutex': {len(mutex_objects)}")
        print()
        
        if mutex_objects:
            print("MUTEX-RELATED OBJECTS:")
            print("-" * 40)
            for obj in mutex_objects:
                print(f"Name: {obj.name}")
                print(f"URI: {obj.uri}")
                print(f"Role: {obj.role}")
                print(f"Domain: {obj.domain}")
                print(f"Display Name: {obj.display_name}")
                print(f"Effective Display Name: {obj.effective_display_name}")
                print()
        else:
            print("No objects containing 'mutex' found in inventory.")
            print()
        
        # Also search for objects containing 'exclusive' or 'group'
        print("SEARCHING FOR RELATED TERMS:")
        print("-" * 30)
        
        related_terms = ['exclusive', 'group', 'argument']
        for term in related_terms:
            matching_objects = [
                obj for obj in result.objects 
                if term in obj.name.lower()
            ]
            print(f"Objects containing '{term}': {len(matching_objects)}")
            if matching_objects and len(matching_objects) <= 10:
                for obj in matching_objects[:10]:
                    print(f"  - {obj.name}")
        
        print()
        print("INVENTORY SUMMARY:")
        print("-" * 20)
        print(f"Total objects: {len(result.objects)}")
        print(f"Inventory type: {result.inventory_locations[0].inventory_type}")
        print(f"Processor: {result.inventory_locations[0].processor_name}")
        print(f"Object count per location: {result.inventory_locations[0].object_count}")
        
        # Save full inventory to file for further analysis
        inventory_file = Path(__file__).parent / "tyro_full_inventory.json"
        inventory_data = {
            "location": result.location,
            "query": result.query,
            "total_objects": len(result.objects),
            "objects": [
                {
                    "name": obj.name,
                    "uri": obj.uri,
                    "role": obj.role,
                    "domain": obj.domain,
                    "display_name": obj.display_name,
                    "effective_display_name": obj.effective_display_name,
                }
                for obj in result.objects
            ]
        }
        
        with open(inventory_file, 'w') as f:
            json.dump(inventory_data, f, indent=2)
        
        print(f"\nFull inventory saved to: {inventory_file}")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(analyze_tyro_inventory())