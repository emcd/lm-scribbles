#!/usr/bin/env python3
"""
Script to examine the downloaded inventory files and understand
their structure for MkDocs sites with mkdocstrings.
"""

import sphobjinv
from pathlib import Path
import json


def analyze_inventory(inv_file_path: Path) -> dict:
    """Analyze a Sphinx inventory file."""
    try:
        inventory = sphobjinv.Inventory(fname_zlib=str(inv_file_path))
        
        analysis = {
            'file': str(inv_file_path),
            'project': inventory.project,
            'version': inventory.version,
            'object_count': len(inventory.objects),
            'domains': {},
            'roles': {},
            'sample_objects': []
        }
        
        # Analyze domains and roles
        for obj in inventory.objects:
            domain = obj.domain
            role = obj.role
            
            if domain not in analysis['domains']:
                analysis['domains'][domain] = 0
            analysis['domains'][domain] += 1
            
            if role not in analysis['roles']:
                analysis['roles'][role] = 0
            analysis['roles'][role] += 1
        
        # Get sample objects from each domain/role combination
        seen_combinations = set()
        for obj in inventory.objects:
            combination = (obj.domain, obj.role)
            if combination not in seen_combinations and len(analysis['sample_objects']) < 20:
                analysis['sample_objects'].append({
                    'name': obj.name,
                    'domain': obj.domain,
                    'role': obj.role,
                    'priority': obj.priority,
                    'uri': obj.uri,
                    'uri_expanded': obj.uri_expanded
                })
                seen_combinations.add(combination)
        
        return analysis
        
    except Exception as e:
        return {'error': str(e), 'file': str(inv_file_path)}


def main():
    """Analyze all downloaded inventory files."""
    scribbles_dir = Path(__file__).parent
    
    print("Analyzing downloaded inventory files...\n")
    
    all_analyses = {}
    
    for inv_file in scribbles_dir.glob('objects_*.inv'):
        print(f"Analyzing {inv_file.name}...")
        analysis = analyze_inventory(inv_file)
        
        if 'error' not in analysis:
            print(f"  Project: {analysis['project']}")
            print(f"  Version: {analysis['version']}")
            print(f"  Objects: {analysis['object_count']}")
            print(f"  Domains: {list(analysis['domains'].keys())}")
            print(f"  Roles: {list(analysis['roles'].keys())}")
            
            # Show some sample objects
            print("  Sample objects:")
            for obj in analysis['sample_objects'][:5]:
                print(f"    {obj['domain']}.{obj['role']}: {obj['name']} -> {obj['uri']}")
        else:
            print(f"  Error: {analysis['error']}")
        
        all_analyses[inv_file.name] = analysis
        print()
    
    # Save detailed analysis
    output_file = scribbles_dir / 'inventory_analysis.json'
    with output_file.open('w') as f:
        json.dump(all_analyses, f, indent=2)
    
    print(f"Detailed analysis saved to {output_file}")


if __name__ == '__main__':
    main()