#!/usr/bin/env python3
"""
Analyze what paths we should actually skip vs allow.
"""

import sys
import site
import sysconfig
from pathlib import Path

def analyze_what_to_skip():
    """Analyze what paths should be skipped vs allowed."""
    
    print("=== What Should Be Skipped ===")
    
    # Standard library paths
    stdlib_path = Path(sysconfig.get_path('stdlib')).resolve()
    print(f"Standard library: {stdlib_path}")
    
    # Platform-specific modules
    platstdlib_path = Path(sysconfig.get_path('platstdlib')).resolve()
    print(f"Platform stdlib: {platstdlib_path}")
    
    # Built-in modules location (usually same as stdlib)
    try:
        builtin_modules = sys.builtin_module_names
        print(f"Built-in modules: {len(builtin_modules)} modules (no file paths)")
    except:
        pass
    
    print("\n=== What Should Be ALLOWED ===")
    
    # Site-packages (third-party packages)
    site_packages = [Path(p).resolve() for p in site.getsitepackages()]
    for sp in site_packages:
        print(f"Site-packages: {sp}")
    
    # User site-packages
    try:
        user_site = Path(site.getusersitepackages()).resolve()
        print(f"User site-packages: {user_site}")
    except:
        pass
    
    print("\n=== Current Problematic Logic ===")
    current_python_location = Path(sys.executable).parent.parent.resolve()
    print(f"Current python_location: {current_python_location}")
    
    print("\n=== Better Logic Would Be ===")
    print("Skip only:")
    print(f"  - Standard library: {stdlib_path}")
    print(f"  - Platform stdlib: {platstdlib_path}")
    print(f"  - Appcore package itself")
    print()
    print("Allow:")
    for sp in site_packages:
        print(f"  - Site-packages: {sp}")
    try:
        print(f"  - User site-packages: {user_site}")
    except:
        pass
    print("  - Any other third-party code")
    
    print("\n=== Demonstrating the Bug ===")
    print("With current logic, if a third-party package 'foo' is installed at:")
    for sp in site_packages:
        example_package = sp / "foo" / "__init__.py"
        is_skipped = example_package.is_relative_to(current_python_location)
        print(f"  {example_package}")
        print(f"    Would be skipped: {is_skipped} {'❌ BUG!' if is_skipped else '✅ OK'}")

if __name__ == "__main__":
    analyze_what_to_skip()