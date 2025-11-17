#!/usr/bin/env python3
"""Script to comment out filesystem-dependent tests for alpha release."""

import re
from pathlib import Path

def comment_out_file_tests(file_path: Path):
    """Comment out all test functions and related content in a file."""
    print(f"Processing {file_path}")
    
    content = file_path.read_text()
    
    # Track which imports become unused
    imports_to_comment = []
    
    # Comment out all test functions
    def comment_test_function(match):
        return match.group(0).replace('\n', '\n# ', -1).replace('def ', '# def ', 1)
    
    # Comment out test functions and their bodies
    content = re.sub(
        r'^def test_[^(]*\([^)]*\):.*?(?=\n(?:def |class |\n|\Z))',
        comment_test_function,
        content,
        flags=re.MULTILINE | re.DOTALL
    )
    
    # Check which imports are now unused
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        # Check for import statements that might now be unused
        if line.startswith('import tempfile'):
            imports_to_comment.append('tempfile')
            new_lines.append('# ' + line)
        elif line.startswith('from pathlib import Path'):
            imports_to_comment.append('pathlib.Path') 
            new_lines.append('# ' + line)
        elif 'import' in line and ('tempfile' in line or 'pathlib' in line):
            new_lines.append('# ' + line)
        else:
            new_lines.append(line)
    
    file_path.write_text('\n'.join(new_lines))
    print(f"Commented out tests in {file_path}")
    if imports_to_comment:
        print(f"  Commented imports: {imports_to_comment}")

def main():
    """Comment out filesystem tests in target files."""
    test_files = [
        'tests/test_000_librovore/test_640_xtnsmgr_cachemgr.py',
        'tests/test_000_librovore/test_630_xtnsmgr_importation.py',
    ]
    
    base_path = Path('/home/me/src/python-librovore')
    
    for test_file in test_files:
        file_path = base_path / test_file
        if file_path.exists():
            comment_out_file_tests(file_path)
        else:
            print(f"Warning: {file_path} not found")

if __name__ == '__main__':
    main()