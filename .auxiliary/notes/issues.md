# Issues Tracking

## Active Issues

### Issue #1: IngestCommand Does Not Preserve Source Directory Hierarchy

**Status**: Open
**Priority**: High
**Discovered**: 2025-11-17 (during python-librovore ingestion)
**Affects**: IngestCommand in sources/lmscribbles/cli.py

**Description**:
The IngestCommand flattens the source directory structure when copying files to the target location. All files from nested source directories are copied into a flat target directory structure, which causes:

1. **False positive duplicate detection**: Files with the same name from different source subdirectories are treated as duplicates
2. **Loss of organizational context**: Source directory structure provides valuable context about file relationships and organization
3. **Potential name collisions**: Increased likelihood of filename conflicts when flattening hierarchical structures

**Example**:
```
# Source structure
.auxiliary/scribbles/
  ├── sphinx-samples/
  │   ├── furo-theme.html
  │   └── rtd-theme.html
  └── test-fixtures/
      └── furo-theme.html

# Current behavior (incorrect - flattened)
ingests/python-librovore/
  ├── furo-theme.html        # From sphinx-samples/
  └── furo-theme-a1b2c3.html # From test-fixtures/ (renamed due to collision)

# Expected behavior (preserve hierarchy)
ingests/python-librovore/
  ├── sphinx-samples/
  │   ├── furo-theme.html
  │   └── rtd-theme.html
  └── test-fixtures/
      └── furo-theme.html
```

**Impact**:
- **Immediate**: Ingestion of python-librovore encountered false duplicate warnings
- **Long-term**: Makes it difficult to understand original file organization and relationships

**Proposed Fix**:
Modify the file copying logic in IngestCommand to:
1. Preserve relative path structure from source base directory
2. Create target subdirectories as needed
3. Only detect duplicates when files have the same relative path (not just filename)

**Related Code Locations**:
- sources/lmscribbles/cli.py - IngestCommand implementation
- File discovery and path handling logic

**Test Cases Needed**:
- Copy files from nested source structure, verify hierarchy preserved
- Verify same filename in different subdirectories doesn't trigger false duplicates
- Verify actual duplicate detection still works (same relative path, different content)

---

### Issue #2: Tyro CLI Requires Prefix for Subcommand Arguments

**Status**: Open
**Priority**: Medium
**Discovered**: 2025-11-17
**Affects**: CLI argument parsing in sources/lmscribbles/cli.py

**Description**:
When using tyro for CLI argument parsing, subcommand arguments require the `--command.argument` prefix pattern instead of the more user-friendly `--argument` pattern.

**Example**:
```bash
# Current behavior (verbose)
lmscribbles ingest --ingest.source-paths ./files --ingest.project-name myproject

# Desired behavior (clean)
lmscribbles ingest --source-paths ./files --project-name myproject
```

**Root Cause**:
Tyro's default behavior prefixes subcommand arguments with the command name to avoid namespace collisions between different subcommands.

**Proposed Fix**:
Use `__.tyro.conf.arg(prefix_name=False)` decorator on subcommand dataclass fields to disable the prefix requirement.

**Example Implementation**:
```python
from typing import Annotated
from __ import tyro

@dataclass
class IngestCommand:
    source_paths: Annotated[
        list[Path],
        tyro.conf.arg(prefix_name=False),
        Doc("Source files or directories to ingest")
    ]
    project_name: Annotated[
        str,
        tyro.conf.arg(prefix_name=False),
        Doc("Target project name")
    ]
```

**Impact**:
- User experience: More intuitive CLI interface
- Documentation: Simpler examples in help text and documentation
- Compatibility: Existing scripts using prefixed args would break (but likely none exist yet)

**Related Code Locations**:
- sources/lmscribbles/cli.py - All Command dataclasses
- Specifically: IngestCommand, ClassifyCommand, SearchCommand

**Test Cases Needed**:
- Verify arguments work without prefix
- Update CLI tests to use unprefixed argument style
- Test help text rendering shows clean argument names

---

## Resolved Issues

None yet.

---

## Issue Template

When adding new issues, use this template:

```markdown
### Issue #N: Brief Title

**Status**: Open | In Progress | Resolved
**Priority**: Low | Medium | High | Critical
**Discovered**: YYYY-MM-DD
**Affects**: Component/file path

**Description**:
Clear description of the issue, including symptoms and impact.

**Example** (if applicable):
Code or command examples demonstrating the issue.

**Root Cause** (if known):
Technical explanation of why the issue occurs.

**Proposed Fix**:
Suggested approach to resolve the issue.

**Impact**:
How this affects users and the system.

**Related Code Locations**:
- file:line references

**Test Cases Needed**:
- List of test scenarios to verify fix

**Related Issues**:
Links to related issues if applicable.
```

---

## Notes

- This file tracks implementation issues and bugs discovered during development
- For feature requests and enhancements, see documentation/prd.rst
- For architectural decisions, see documentation/architecture/decisions/
- For general TODOs, see .auxiliary/notes/todo.md (if it exists)
