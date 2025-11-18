#!/usr/bin/env python3
"""
Debug the path relationships to understand the issue.
"""

import sys
import site
import sysconfig
from pathlib import Path

def debug_paths():
    """Debug path relationships."""
    
    stdlib_path = Path(sysconfig.get_path('stdlib')).resolve()
    platstdlib_path = Path(sysconfig.get_path('platstdlib')).resolve()
    site_packages = [Path(p).resolve() for p in site.getsitepackages()]
    
    print("=== Path Analysis ===")
    print(f"stdlib: {stdlib_path}")
    print(f"platstdlib: {platstdlib_path}")
    print(f"site-packages: {site_packages}")
    
    print(f"\n=== Are they the same? ===")
    print(f"stdlib == platstdlib: {stdlib_path == platstdlib_path}")
    
    for sp in site_packages:
        print(f"site-packages {sp}")
        print(f"  is_relative_to stdlib: {sp.is_relative_to(stdlib_path)}")
        print(f"  is_relative_to platstdlib: {sp.is_relative_to(platstdlib_path)}")
        print(f"  stdlib is_relative_to site-packages: {stdlib_path.is_relative_to(sp)}")
        
        # Check parent relationships
        print(f"  site-packages parent: {sp.parent}")
        print(f"  stdlib parent: {stdlib_path.parent}")
        print(f"  are parents equal: {sp.parent == stdlib_path.parent}")

if __name__ == "__main__":
    debug_paths()