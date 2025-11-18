#!/usr/bin/env python3
"""Improved package detection based on user's insights."""

import sys
import inspect

def improved_discover_invoker_location():
    """
    Improved version of _discover_invoker_location based on user insights:
    1. Don't check __module__ (never present in frame globals)
    2. Use __name__ directly (always available)
    3. Use sys.modules to find actual package boundaries (handles namespace packages)
    """
    import site
    import sysconfig
    
    package_location = __.Path(__file__).parent.resolve()
    stdlib_locations = {
        __.Path(sysconfig.get_path('stdlib')).resolve(),
        __.Path(sysconfig.get_path('platstdlib')).resolve(),
    }
    sp_locations: set[__.Path] = set()
    for path in site.getsitepackages():
        sp_locations.add(__.Path(path).resolve())
    with __.ctxl.suppress(AttributeError):
        sp_locations.add(__.Path(site.getusersitepackages()).resolve())
    
    frame = inspect.currentframe()
    if frame is None: 
        return __.absent, __.Path.cwd()
    
    # Walk up the call stack to find frame outside of this package
    while True:
        frame = frame.f_back
        if frame is None: 
            break
        
        location = __.Path(frame.f_code.co_filename).resolve()
        
        # Skip frames within this package
        if location.is_relative_to(package_location):
            continue
            
        # Allow site-packages even if they're under stdlib paths
        in_site_packages = any(
            location.is_relative_to(sp_location)
            for sp_location in sp_locations
        )
        
        # Skip standard library paths (unless in site-packages)
        if not in_site_packages and any(
            location.is_relative_to(stdlib_location)
            for stdlib_location in stdlib_locations
        ):
            continue
        
        # Get __name__ from frame globals (always available)
        name_val = frame.f_globals.get('__name__')
        if not name_val or name_val == '__main__':
            continue
            
        # Find actual package boundary using sys.modules
        package_name = find_package_boundary(name_val)
        if package_name:
            return package_name, location.parent
        else:
            continue
    
    # Fallback location is current working directory
    return __.absent, __.Path.cwd()

def find_package_boundary(full_name):
    """
    Find the actual package boundary using sys.modules.
    Works backwards through dotted name to find the deepest package.
    """
    if not full_name or full_name == '__main__':
        return None
    
    components = full_name.split('.')
    
    # Work backwards through the dotted name
    for i in range(len(components), 0, -1):
        candidate = '.'.join(components[:i])
        
        if candidate in sys.modules:
            module = sys.modules[candidate]
            
            # Check if it's a package (has __path__)
            if hasattr(module, '__path__'):
                return candidate
            else:
                # Continue searching for containing package
                continue
    
    # If no package found, return the first component
    # (fallback for edge cases)
    return components[0]

def test_improved_detection():
    """Test the improved detection with various scenarios."""
    
    print("=== Testing Improved Detection Algorithm ===")
    
    # Test the package boundary finder directly
    test_cases = [
        "os",
        "pathlib",
        "collections.abc", 
        "importlib.metadata",
        "__main__",
        "nonexistent.package.module"
    ]
    
    print("\\nPackage boundary detection:")
    for test_case in test_cases:
        result = find_package_boundary(test_case)
        print(f"  {test_case:<25} -> {result}")

def create_comprehensive_test():
    """Create a comprehensive test with namespace packages."""
    
    import tempfile
    import subprocess
    from pathlib import Path
    
    temp_dir = Path(tempfile.mkdtemp())
    
    try:
        # Create test structure
        namespace_dir = temp_dir / "mynamespace"
        namespace_dir.mkdir()
        
        subpkg_dir = namespace_dir / "subpkg"
        subpkg_dir.mkdir()
        (subpkg_dir / "__init__.py").write_text('# namespace subpackage')
        (subpkg_dir / "module.py").write_text('''
def test_detection():
    """Test detection from within namespace package."""
    import sys
    import inspect
    
    def find_package_boundary(full_name):
        if not full_name or full_name == '__main__':
            return None
        
        components = full_name.split('.')
        
        for i in range(len(components), 0, -1):
            candidate = '.'.join(components[:i])
            
            if candidate in sys.modules:
                module = sys.modules[candidate]
                if hasattr(module, '__path__'):
                    return candidate
                else:
                    continue
        
        return components[0]
    
    frame = inspect.currentframe()
    name_val = frame.f_globals.get('__name__')
    
    print(f"Current __name__: {name_val}")
    print(f"Detected package: {find_package_boundary(name_val)}")
    
    return find_package_boundary(name_val)

test_detection()
''')
        
        # Create test script
        test_script = temp_dir / "test_comprehensive.py"
        test_script.write_text(f'''
import sys
sys.path.insert(0, "{temp_dir}")

print("=== Comprehensive Test ===")

import mynamespace.subpkg.module

result = mynamespace.subpkg.module.test_detection()
print("Final result: {{}}".format(result))

# What we expect: mynamespace.subpkg (the actual package with __init__.py)
# Not: mynamespace (the namespace root)
''')
        
        result = subprocess.run(
            [sys.executable, str(test_script)],
            capture_output=True,
            text=True,
            cwd=temp_dir
        )
        
        print("\\n=== Comprehensive Test Results ===")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
    finally:
        import shutil
        shutil.rmtree(temp_dir)

# Mock the __ module for testing
class MockUnderscore:
    class Path:
        @staticmethod
        def cwd():
            from pathlib import Path
            return Path.cwd()
            
        def __init__(self, path):
            from pathlib import Path
            self._path = Path(path)
            
        def parent(self):
            return self._path.parent
            
        def resolve(self):
            return self._path.resolve()
            
        def is_relative_to(self, other):
            return self._path.is_relative_to(other)
    
    class ctxl:
        @staticmethod
        def suppress(*args):
            from contextlib import suppress
            return suppress(*args)
    
    absent = "ABSENT_SENTINEL"

# Global mock for testing
__ = MockUnderscore()

if __name__ == "__main__":
    test_improved_detection()
    create_comprehensive_test()