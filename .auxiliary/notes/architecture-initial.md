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

**IngestCommand** (Primary focus)
- Copy files from source to target directory
- Screen each file for secrets
- Detect duplicates via content hashing
- Handle naming conflicts (interactive or heuristic)
- Emit warnings for secrets and duplicates

**ClassifyCommand**
- Tag scribbles with labels
- Update catalog database
- Support bulk classification operations

**SearchCommand**
- Query scribbles by labels, dates, content
- Support full-text search

**RefinementsCommand**
- Manage the "refinements" workflow
- Mark scribbles as candidates for refinement
- Track refinement status

**ConfigureCommand**
- Manage configuration settings
- Configure secret detection rules
- Set default behaviors (interactive vs. automated)

#### 2. Directory Structure

```
scribbles/               # Raw archived scribbles
  ├── YYYY-MM/          # Organized by month
  │   ├── original-name-1.ext
  │   ├── original-name-2.ext
  │   └── duplicates/   # Renamed duplicates
  │       └── original-name-hash.ext

refinements/            # Extracted gems
  ├── YYYY-MM/
  │   ├── refined-item-1.ext
  │   └── metadata/     # Refinement notes
```

#### 3. Catalog System

**Storage Options** (to be decided):
1. **SQLite database** - Good for queries, structured data
2. **YAML/JSON files** - Good for git tracking, human readability
3. **Hybrid** - Index in SQLite, metadata in YAML

**Catalog Schema** (preliminary):
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

**Label Categories** (examples):
- **Source**: `debug`, `exploration`, `proof-of-concept`, `investigation`
- **Quality**: `gem`, `interesting`, `routine`, `noise`
- **Topic**: `architecture`, `bug-fix`, `algorithm`, `api-design`
- **Language**: `python`, `rust`, `typescript`, etc.
- **Project**: Custom project tags

#### 4. Secret Detection

**Options** (research needed):
1. **Existing packages**:
   - `detect-secrets` (Yelp) - Widely used, extensible
   - `truffleHog` - Git-focused but adaptable
   - `gitleaks` - Fast, configurable

2. **Bespoke solution**:
   - Regex patterns for common secrets
   - Entropy analysis for random strings
   - Path-based exclusions (e.g., `.env` patterns)

**Recommendation**: Start with `detect-secrets` for proven reliability, with option to customize.

#### 5. Duplicate Detection

**Strategy**:
1. Compute content hash (SHA-256) on ingest
2. Check against catalog for existing hash
3. If duplicate:
   - **Same content, same name**: Skip silently (idempotent)
   - **Same content, different name**: Warn, optionally link
   - **Same name, different content**:
     - Interactive: Prompt user for action
     - Automated: Append hash suffix to filename

**Heuristic Renaming Pattern**:
```
original-name.ext          # First version
original-name-a1b2c3.ext   # Collision, first 6 chars of hash
```

#### 6. Data Models

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path

class ScribbleStatus(Enum):
    RAW = "raw"
    CLASSIFIED = "classified"
    REFINED = "refined"
    ARCHIVED = "archived"

class DuplicateStrategy(Enum):
    SKIP = "skip"
    RENAME = "rename"
    INTERACTIVE = "interactive"

@dataclass
class IngestOptions:
    source_paths: list[Path]
    target_base: Path
    check_secrets: bool = True
    duplicate_strategy: DuplicateStrategy = DuplicateStrategy.INTERACTIVE
    organize_by_month: bool = True
    dry_run: bool = False

@dataclass
class SecretDetectionResult:
    file_path: Path
    has_secrets: bool
    findings: list[str]  # Description of what was found

@dataclass
class IngestResult:
    succeeded: list[Path]
    skipped: list[Path]
    failed: list[tuple[Path, str]]  # (path, reason)
    warnings: list[str]
```

## Questions and Decisions Needed

### 1. Secret Detection Strategy
- **Q**: Use existing package or build custom solution?
- **Recommendation**: Start with `detect-secrets` for reliability
- **Follow-up**: Do you have specific secret patterns we need to catch beyond common ones (API keys, passwords, tokens)?

### 2. Duplicate Handling
- **Q**: Default to interactive or automated renaming?
- **Options**:
  - Interactive: Safer, user reviews each conflict
  - Automated: Faster, uses heuristic renaming
- **Recommendation**: Interactive by default, with `--auto-rename` flag for batch operations

### 3. Catalog Implementation
- **Q**: Database (SQLite) vs. file-based (YAML/JSON) vs. hybrid?
- **Tradeoffs**:
  - SQLite: Fast queries, complex searches, but binary format
  - YAML: Human-readable, git-friendly, but slower for large datasets
  - Hybrid: Best of both, more complexity
- **Recommendation**: Start with SQLite for simplicity, add YAML export for git tracking later

### 4. Refinements Workflow
- **Q**: How should the refinements process work?
- **Considerations**:
  - Manual selection from catalog?
  - Automated suggestions based on labels/quality?
  - Integration with editor/viewer?
- **Need**: More details on your typical refinement workflow

### 5. File Organization
- **Q**: Organize by date, project, type, or combination?
- **Current proposal**: `YYYY-MM/` subdirectories
- **Alternatives**:
  - Project-based: `project-name/YYYY-MM/`
  - Type-based: `code/`, `docs/`, `diagrams/`
  - Flat with metadata: All files in one dir, catalog for organization

### 6. Import/Export
- **Q**: Should we support exporting catalogs or collections?
- **Use cases**: Sharing gems, backing up refined content, integration with other tools
- **Format**: Markdown reports? JSON exports? Git bundle?

### 7. Search and Query Interface
- **Q**: CLI-only or also web interface?
- **Considerations**:
  - CLI: Fits project style, scriptable
  - Web: Better for browsing, visualization
- **Recommendation**: CLI first, web as future enhancement

## Technical Considerations

### Performance
- **Hashing**: Use `hashlib.sha256()` with buffered reads for large files
- **Parallel processing**: Use `asyncio` for concurrent file operations
- **Catalog indexing**: SQLite with indexes on common query fields (labels, dates, hashes)

### Testing Strategy
- Unit tests for core logic (hashing, duplicate detection)
- Integration tests for CLI commands
- Fixtures with sample scribbles (safe, synthetic data)
- Mock secret detection for deterministic tests

### Error Handling
- Graceful degradation (skip unreadable files, log errors)
- Dry-run mode for testing operations
- Rollback capability for batch operations (transaction log)
- Clear error messages with suggested fixes

### Security
- Secrets file handling: Never copy files with detected secrets by default
- Quarantine option: Move flagged files to review directory
- Audit log: Track all ingest operations for review

### Extensibility
- Plugin system for custom secret detectors
- Custom label taxonomies
- Configurable file filters (by extension, size, pattern)
- Export formats (custom renderers)

## Implementation Phases

### Phase 1: Core Ingest (MVP)
1. IngestCommand with basic file copying
2. Content hashing and duplicate detection
3. Simple interactive duplicate handling
4. Basic secret detection (using `detect-secrets`)
5. SQLite catalog for metadata
6. Warning system for secrets/duplicates

### Phase 2: Classification & Catalog
1. ClassifyCommand for labeling
2. SearchCommand for querying
3. Enhanced catalog schema with labels
4. Bulk operations support
5. Export catalog to YAML/JSON

### Phase 3: Refinements Workflow
1. RefinementsCommand suite
2. Refinement tracking in catalog
3. Integration with refinements directory
4. Metadata for refinement notes

### Phase 4: Polish & Features
1. Configuration management
2. Advanced search (full-text, regex)
3. Statistics and reporting
4. Dry-run and simulation modes
5. Comprehensive testing

## Next Steps

1. **Finalize decisions** on open questions (see above)
2. **Research secret detection packages** - Quick evaluation of `detect-secrets`
3. **Create data models** - Implement core dataclasses
4. **Prototype IngestCommand** - Basic file copying with duplicate detection
5. **Design catalog schema** - SQLite tables and indexes
6. **Write tests** - Start with duplicate detection logic

## References

- CLI patterns: `vibelinter/cli.py`, `appcore/cli.py`
- Dependencies: `tyro`, `emcd-appcore[cli]`, `absence`, `frigid`, `dynadoc`
- Potential additions: `detect-secrets`, `rich`, `questionary` (for interactive prompts)

## Open Questions for Collaboration

1. What secret patterns are most important to detect in your scribbles?
2. How do you currently organize your scribbles manually?
3. What makes a scribble a "gem" vs. routine content?
4. How often do you expect to ingest scribbles? (Daily, weekly, per-project?)
5. Do you have existing scribbles to test with, or should we create fixtures?
6. Are there specific export formats you need for refined content?
7. Should the system support watching directories for auto-ingest?
8. Do you want version tracking for refined scribbles (git integration)?
