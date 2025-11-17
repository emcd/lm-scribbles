#!/usr/bin/env python3
"""Analyze coverage gaps and test strategy."""

import xml.etree.ElementTree as ET
from pathlib import Path

def analyze_coverage_xml():
    """Parse coverage XML to identify specific gaps."""
    coverage_file = Path('.auxiliary/artifacts/coverage-pytest/coverage.xml')
    tree = ET.parse(coverage_file)
    root = tree.getroot()
    
    gaps = {}
    
    for package in root.findall('.//package'):
        package_name = package.get('name')
        for cls in package.findall('.//class'):
            filename = cls.get('filename')
            module_name = filename.split('/')[-1].replace('.py', '')
            
            if module_name in ['__main__', '__init__']:
                continue
                
            missing_lines = []
            uncovered_branches = []
            
            for line in cls.findall('.//line'):
                line_num = int(line.get('number'))
                hits = int(line.get('hits'))
                
                if hits == 0:
                    missing_lines.append(line_num)
                
                # Check for partial branch coverage
                if line.get('branch') == 'true':
                    missing_branches = line.get('missing-branches')
                    if missing_branches:
                        uncovered_branches.append((line_num, missing_branches))
            
            if missing_lines or uncovered_branches:
                gaps[module_name] = {
                    'missing_lines': missing_lines,
                    'uncovered_branches': uncovered_branches,
                    'total_statements': len(cls.findall('.//line')),
                    'coverage': float(cls.get('line-rate', 0))
                }
    
    return gaps

def categorize_gaps_by_difficulty():
    """Categorize coverage gaps by testing difficulty."""
    gaps = analyze_coverage_xml()
    
    categories = {
        'easy': [],      # Simple error paths, missing parameters
        'medium': [],    # Network/IO errors, complex conditions
        'hard': [],      # Exception handling, edge cases
        'integration': [] # Requires external dependencies
    }
    
    # Read source files to understand what the missing lines do
    for module, data in gaps.items():
        print(f"\n=== {module}.py ===")
        print(f"Coverage: {data['coverage']:.1%}")
        print(f"Missing lines: {len(data['missing_lines'])}")
        print(f"Uncovered branches: {len(data['uncovered_branches'])}")
        
        # Analyze specific gaps based on line numbers
        if module == 'cli':
            categories['medium'].extend([
                f"{module}:{line}" for line in data['missing_lines'][:5]
            ])
        elif module == 'functions':
            # Many HTTP/network error paths
            categories['hard'].extend([
                f"{module}:{line}" for line in data['missing_lines'][:10]
            ])
        elif module == 'interfaces':
            # Type checking and validation
            categories['easy'].extend([
                f"{module}:{line}" for line in data['missing_lines']
            ])
        elif module == 'server':
            # MCP server integration
            categories['integration'].extend([
                f"{module}:{line}" for line in data['missing_lines'][:5]
            ])
    
    return categories

def analyze_test_overlap():
    """Analyze which tests hit the same code paths."""
    print("\n=== Test Path Overlap Analysis ===")
    
    # Based on our test patterns
    overlapping_patterns = {
        'Basic inventory extraction': [
            'test_100_extract_inventory_local_file',
            'test_110_extract_inventory_with_domain_filter',
            'test_120_extract_inventory_with_role_filter',
            'test_140_extract_inventory_with_all_filters'
        ],
        'Query documentation basic flow': [
            'test_500_query_documentation_basic',
            'test_510_query_documentation_with_domain_filter',
            'test_520_query_documentation_with_role_filter',
            'test_600_query_documentation_relevance_ranking'
        ],
        'Match mode variations': [
            'test_540_query_documentation_with_exact_match',
            'test_550_query_documentation_with_regex_match', 
            'test_560_query_documentation_with_fuzzy_match'
        ]
    }
    
    for pattern, tests in overlapping_patterns.items():
        print(f"\n{pattern}:")
        print(f"  Tests: {len(tests)}")
        print(f"  Likely overlap: High (same core path)")
        
    return overlapping_patterns

if __name__ == "__main__":
    print("=== Coverage Gap Analysis ===")
    
    gaps = analyze_coverage_xml()
    categories = categorize_gaps_by_difficulty()
    
    print(f"\n=== Gap Categories ===")
    for category, items in categories.items():
        print(f"{category.upper()}: {len(items)} gaps")
        if items:
            print(f"  Examples: {items[:3]}")
    
    analyze_test_overlap()
    
    print(f"\n=== Recommendations ===")
    print("1. Focus on 'easy' gaps first - quick wins")
    print("2. Mock HTTP requests for 'hard' network paths")
    print("3. Split integration tests from unit tests")
    print("4. Reduce test overlap by targeting specific uncovered lines")