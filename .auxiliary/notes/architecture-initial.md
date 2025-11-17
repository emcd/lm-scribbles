# LM Scribbles Archive - Initial Architecture Notes

## Setup Completed

Successfully configured the Claude Code (Web) development environment:

- GitHub CLI v2.83.1 installed
- Core Python tools: hatch, copier, emcd-agents
- Project agents populated from `github:emcd/agents-common@master#defaults`
- Go environment configured with GOPATH
- Language servers installed: mcp-language-server, pyright, ruff
- bash-tool-bypass wrapper configured

All tools verified and operational.

## Project Overview

### Purpose
Archive and classify "scribbles" (LLM-generated content) from various projects, with the ability to:
- Screen for secrets before archiving
- Detect and handle duplicates
- Extract and refine valuable insights ("diamonds in the rough")
- Catalog and classify processed scribbles

### Current State
- Basic CLI scaffolding exists using `tyro` and async patterns
- Follows conventions from `emcd-appcore[cli]` library
- Empty `.auxiliary/scribbles/` directory ready for data

### Three-Bin Workflow
The system implements a three-tier LLM-driven curation workflow:
1. **Ingests**: Raw scribbles organized by project (aggregated from various machines)
2. **Selections**: Curated subset identified as valuable (LLM-assisted selection)
3. **Refinements**: Polished gems ready for reuse (LLM-assisted refinement)

## Reference CLI Architecture Analysis

### Key Patterns from `vibelinter` and `appcore.cli`

1. **Command Structure**
   - Hierarchical subcommands using `tyro` for argument parsing
   - Each command as an immutable dataclass with `__call__` method
   - Async-first architecture with `AsyncExitStack` for resource management
   - Default command pattern for convenience

2. **Configuration**
   - Protocol-based classes: `Command` and `Application`
   - `DisplayOptions` for output control (format, colorization, routing)
   - `InscriptionControl` for logging management
   - Type aliases for standardizing common parameters

3. **Output Handling**
   - Self-rendering result classes with dual methods: `render_as_json()`, `render_as_text()`
   - Centralized output dispatch pattern
   - Respects `NO_COLOR` environment variables and TTY capabilities

4. **Integration Points**
   - `tyro` for CLI parsing and help generation
   - Rich library for terminal formatting
   - `inscription` module for structured logging
   - `state.Globals` for application context

## Proposed Architecture

### Core Components

#### 1. CLI Commands

**IngestCommand** (Primary focus - Phase 1)
- Copy files from source to target directory with project-based organization
- Screen each file for secrets (warnings only, no file quarantine)
- Detect duplicate names in target directory via content hashing
- Automatically handle naming conflicts with hash-based renaming
- Emit warnings for secrets and duplicate name conflicts

**ClassifyCommand** (Stub only - Phase 2+)
- Tag scribbles with labels
- Update catalog database
- Support bulk classification operations
- LLM-assisted classification

**SearchCommand** (Stub only - Phase 2+)
- Query scribbles by labels, dates, content
- Support full-text search

**Note**: Configuration will be file-based via `appcore` configuration system. No dedicated ConfigureCommand needed.

#### 2. Directory Structure

```
ingests/                      # Raw scribbles (renamed from "scribbles")
  ├── lm-scribbles/          # Organized by project name
  │   ├── file-1.ext
  │   ├── file-2.ext
  │   └── file-2-a1b2c3.ext  # Duplicate name, different content (hash suffix)
  ├── python-dynadoc/
  │   └── ...
  └── ...

selections/                   # Curated subset (LLM-selected)
  ├── lm-scribbles/          # Project-based organization
  │   └── file-1.ext -> ../../ingests/lm-scribbles/file-1.ext  # Symlinks
  └── ...

refinements/                  # Polished gems (LLM-refined)
  ├── refined-item-1.ext     # Possibly flat structure
  ├── refined-item-2.ext
  └── ...
```

**Key Notes**:
- Source directories are typically `.auxiliary/scribbles/` from various project repositories
- Ingests aggregates scribbles from multiple machines over time by project
- Only files with duplicate names AND different content get hash suffixes
- Files with same name and same content are skipped (idempotent ingestion)

#### 3. Catalog System

**Deferred to Phase 2+**. Initial focus is on core ingestion mechanics.

**Future Storage Options**:
- SQLite database stored via Git LFS in the repository
- Possible YAML export for human readability

**Future Catalog Schema** (preliminary - needs review):
```python
@dataclass
class ScribbleMetadata:
    id: str                          # Unique identifier
    original_path: str               # Source location
    archived_path: str               # Location in archive
    content_hash: str                # SHA-256 or similar
    ingested_at: datetime
    size_bytes: int
    labels: set[str]                 # Flexible tagging
    status: ScribbleStatus           # Enum: raw, classified, refined
    notes: str                       # Free-form notes
    refinement_id: str | None        # Link to refinement if extracted
```

**Label Categories** (good ideas for future):
- **Source**: `debug`, `exploration`, `proof-of-concept`, `investigation`
- **Quality**: `gem`, `interesting`, `routine`, `noise`
- **Topic**: `architecture`, `bug-fix`, `algorithm`, `api-design`
- **Language**: `python`, `rust`, `typescript`, etc.
- **Project**: Custom project tags

#### 4. Secret Detection

**Approach**: Use `detect-secrets` (Yelp package) for proven reliability.

**Behavior**:
- Scan each file before copying
- Issue warnings for detected secrets
- No file quarantine or blocking - just inform the user
- No specific custom secret patterns required initially (common patterns sufficient)

#### 5. Duplicate Detection

**Simplified Strategy**:
1. Check if filename already exists in target directory
2. If yes, compute content hashes for both source and target files
3. Compare hashes:
   - **Same content**: Skip copy (idempotent ingestion)
   - **Different content**: Automatically rename with hash suffix

**Automated Renaming Pattern**:
```
original-name.ext          # First version
original-name-a1b2c3.ext   # Name collision with different content (first 6 chars of hash)
```

**Note**: No need to track files with same content but different names - only handle name conflicts in the target directory.

#### 6. Data Models (Phase 1)

```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class IngestOptions:
    source_paths: list[Path]      # Files or directories to ingest
    target_base: Path              # Base directory (e.g., "ingests/")
    project_name: str              # Target subdirectory name
    check_secrets: bool = True     # Enable secret detection
    dry_run: bool = False          # Preview without copying

@dataclass
class SecretDetectionResult:
    file_path: Path
    has_secrets: bool
    findings: list[str]            # Description of detected secrets

@dataclass
class IngestResult:
    copied: list[Path]             # Successfully copied files
    skipped: list[Path]            # Skipped (same content)
    renamed: list[tuple[Path, Path]]  # Renamed (name conflict, different content)
    failed: list[tuple[Path, str]]    # Failed with reason
    warnings: list[str]            # Warnings (secrets, errors, etc.)
```

## Decisions Made (from PR review)

### 1. Secret Detection Strategy
- **Decision**: Use `detect-secrets` (Yelp) package
- **Behavior**: Issue warnings only, no file blocking or quarantine
- **Patterns**: Common patterns sufficient (API keys, passwords, tokens) - no custom patterns needed

### 2. Duplicate Handling
- **Decision**: Automated renaming for Phase 1
- **Strategy**: Only check for duplicate names in target directory, compare hashes if name exists
- **Rationale**: Allows automated testing without interactive prompts; can add interactive mode later if needed

### 3. Catalog Implementation
- **Decision**: Defer to Phase 2+
- **Future**: Likely SQLite with Git LFS storage
- **Rationale**: Focus Phase 1 on core ingestion mechanics

### 4. Refinements Workflow
- **Decision**: Three-bin system (ingests → selections → refinements)
- **Details**: LLM-driven selection and refinement process
- **Structure**: Selections use symlinks to ingests; refinements possibly flat

### 5. File Organization
- **Decision**: Project-based organization (not date-based)
- **Structure**: `ingests/project-name/`, `selections/project-name/`
- **Rationale**: Aggregate scribbles by project over time across multiple machines

### 6. Import/Export
- **Decision**: Defer until after core ingestion is working
- **Future**: May add catalog export features

### 7. Search and Query Interface
- **Decision**: Defer design until later phases
- **Future**: CLI-based initially

### 8. Configuration
- **Decision**: File-based via `appcore` configuration system
- **Rationale**: No need for dedicated ConfigureCommand

### 9. Source Directories
- **Context**: Typically `.auxiliary/scribbles/` from various project repositories
- **Usage Pattern**: Aperiodic ingestion per-project as scribbles accumulate

## Technical Considerations (Phase 1 Focus)

### Performance
- **Hashing**: Use `hashlib.sha256()` with buffered reads for large files
- **Parallel processing**: Use `asyncio` for concurrent file operations
- **Optimization**: Defer until needed - prioritize correctness first

### Testing Strategy
- **Initial**: Manual testing using test fixtures in `.auxiliary/scribbles`
- **Self-hosting**: Test ingest command by ingesting its own test fixtures
- **Future**: Formal test suite with unit and integration tests

### Error Handling
- Graceful degradation (skip unreadable files, log errors)
- Dry-run mode for testing operations
- Clear error messages with suggested fixes
- Result objects track successes, failures, warnings separately

### Security
- Secrets detection: Warn user but continue with copy
- No file blocking or quarantine needed

## Implementation Phases (Updated)

### Phase 1: Core Ingest (MVP) - CURRENT FOCUS
**Goal**: Get basic file ingestion working to enable LLM-based classification.

**Deliverables**:
1. **IngestCommand** - Full implementation:
   - Project-based file copying (`ingests/project-name/`)
   - Content hashing (SHA-256) for duplicate detection
   - Automated duplicate name handling (hash-based renaming)
   - Secret detection using `detect-secrets` (warnings only)
   - Self-rendering result objects (text and JSON output)
   - Dry-run mode
2. **ClassifyCommand** - Stub only (placeholder for Phase 2)
3. **SearchCommand** - Stub only (placeholder for Phase 2)
4. **Test fixtures** - Create sample scribbles in `.auxiliary/scribbles`
5. **Manual testing** - Verify ingestion works correctly

**Not included in Phase 1**:
- SQLite catalog (deferred to Phase 2+)
- Interactive duplicate handling (automated only for now)
- ConfigureCommand (use file-based config via appcore)

### Phase 2: Classification & Catalog (Future)
1. SQLite catalog with Git LFS storage
2. ClassifyCommand full implementation with LLM integration
3. SearchCommand for querying catalog
4. Label taxonomy and bulk operations
5. Export catalog to YAML/JSON

### Phase 3: Selections & Refinements Workflow (Future)
1. Selections directory with symlink management
2. LLM-driven selection workflow
3. Refinements directory and workflow
4. LLM-assisted refinement process

### Phase 4: Polish & Features (Future)
1. Interactive duplicate handling (optional)
2. Advanced search (full-text, regex)
3. Statistics and reporting
4. Comprehensive test suite
5. Performance optimizations

## Next Steps (Phase 1 Implementation)

1. ✅ **Update architecture notes** based on PR feedback
2. **Add `detect-secrets` dependency** to `pyproject.toml`
3. **Implement IngestCommand**:
   - Command dataclass with CLI argument parsing
   - File discovery and validation
   - Content hashing logic
   - Duplicate detection and automated renaming
   - Secret detection integration
   - Result objects with self-rendering (text/JSON)
   - Exception classes for error handling
4. **Create test fixtures** in `.auxiliary/scribbles`:
   - Sample files (some with secrets for POC testing)
   - Duplicate name scenarios
5. **Manual testing**:
   - Test ingestion with fixtures
   - Verify duplicate handling
   - Validate secret detection warnings
   - Test dry-run mode
6. **Stub commands**: Create ClassifyCommand and SearchCommand placeholders

## References

- CLI patterns: `vibelinter/cli.py`, `appcore/cli.py`
- Current dependencies: `tyro`, `emcd-appcore[cli]`, `absence`, `frigid`, `dynadoc`
- New dependency: `detect-secrets`

## Summary

Architecture has been refined based on PR review feedback. Key simplifications for Phase 1:
- Project-based organization (not date-based)
- Automated duplicate handling (not interactive)
- Warnings-only for secrets (no blocking)
- No catalog in Phase 1 (focus on ingestion mechanics)
- Three-bin workflow (ingests → selections → refinements) for future phases

Ready to proceed with IngestCommand implementation following `vibelinter` patterns.
