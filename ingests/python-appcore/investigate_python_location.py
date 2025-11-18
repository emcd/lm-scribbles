#!/usr/bin/env python3
"""
Investigate the python_location calculation bug.
"""

import sys
import site
from pathlib import Path

def analyze_paths():
    """Analyze different path calculations and their implications."""
    
    # Current buggy calculation
    python_location_buggy = Path(sys.executable).parent.parent.resolve()
    
    # Alternative approaches
    sys_prefix = Path(sys.prefix).resolve()
    site_packages = [Path(p).resolve() for p in site.getsitepackages()]
    
    print("=== Current Implementation Analysis ===")
    print(f"sys.executable: {sys.executable}")
    print(f"Buggy python_location (.parent.parent): {python_location_buggy}")
    print(f"sys.prefix: {sys_prefix}")
    print(f"site.getsitepackages(): {site_packages}")
    
    print("\n=== Testing Site-Packages Relationship ===")
    for sp in site_packages:
        is_under_buggy = sp.is_relative_to(python_location_buggy)
        is_under_prefix = sp.is_relative_to(sys_prefix)
        print(f"Site-packages: {sp}")
        print(f"  Under buggy python_location: {is_under_buggy}")
        print(f"  Under sys.prefix: {is_under_prefix}")
    
    print("\n=== Problem Analysis ===")
    print("Current logic skips frames if location.is_relative_to(python_location)")
    print("This means:")
    
    for sp in site_packages:
        if sp.is_relative_to(python_location_buggy):
            print(f"  ❌ PROBLEM: Third-party packages in {sp} will be wrongly skipped!")
        else:
            print(f"  ✅ OK: Third-party packages in {sp} will not be skipped")
    
    print("\n=== Suggested Fix ===")
    print("Instead of skipping everything under python_location, we should:")
    print("1. Skip the standard library specifically")
    print("2. Allow site-packages to be detected as calling packages")
    print("3. Consider using sys.prefix and stdlib paths more precisely")

if __name__ == "__main__":
    analyze_paths()