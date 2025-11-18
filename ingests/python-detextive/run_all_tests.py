#!/usr/bin/env python3
"""
Master test runner for all detextive functionality tests.
Runs all test modules and collects issues for bug reporting.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import importlib.util
from pathlib import Path

def load_and_run_test_module(module_path):
    """Load a test module and run its tests."""
    module_name = module_path.stem
    
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Run the tests
    if hasattr(module, 'run_all_tests'):
        return module.run_all_tests()
    else:
        print(f"⚠️  Module {module_name} has no run_all_tests function")
        return []

def main():
    """Run all test modules and collect results."""
    print("🧪 DETEXTIVE COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print("Testing all public API functionality for bugs and issues...")
    print("=" * 60)
    
    # Find all test modules
    scribbles_dir = Path(__file__).parent
    test_modules = [
        scribbles_dir / "test_charset_detection.py",
        scribbles_dir / "test_mimetype_detection.py", 
        scribbles_dir / "test_inference.py",
        scribbles_dir / "test_validation.py",
        scribbles_dir / "test_line_separators.py",
        scribbles_dir / "test_decode.py",
        scribbles_dir / "test_exceptions.py",
    ]
    
    all_issues = []
    module_results = {}
    
    for module_path in test_modules:
        if module_path.exists():
            print(f"\n🔍 Running {module_path.stem}...")
            print("-" * 40)
            try:
                issues = load_and_run_test_module(module_path)
                module_results[module_path.stem] = issues
                all_issues.extend(issues)
            except Exception as e:
                error_msg = f"Failed to run {module_path.stem}: {str(e)}"
                print(f"❌ {error_msg}")
                all_issues.append(error_msg)
                module_results[module_path.stem] = [error_msg]
        else:
            print(f"⚠️  Test module not found: {module_path}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("🎯 TEST SUITE SUMMARY")
    print("=" * 60)
    
    total_modules = len([m for m in module_results if module_results[m] is not None])
    clean_modules = len([m for m in module_results if not module_results[m]])
    
    print(f"📊 Modules tested: {total_modules}")
    print(f"✅ Clean modules: {clean_modules}")
    print(f"❌ Modules with issues: {total_modules - clean_modules}")
    print(f"🐛 Total issues found: {len(all_issues)}")
    
    if all_issues:
        print(f"\n🔍 DETAILED ISSUE BREAKDOWN:")
        for module_name, issues in module_results.items():
            if issues:
                print(f"\n📋 {module_name}:")
                for issue in issues:
                    print(f"  - {issue}")
    else:
        print(f"\n🎉 ALL TESTS PASSED! No bugs found in public API.")
    
    return all_issues

if __name__ == '__main__':
    issues = main()
    sys.exit(1 if issues else 0)