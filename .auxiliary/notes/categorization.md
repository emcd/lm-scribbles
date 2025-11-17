# Classification System - Planning and Questions

## Session Context

**Date**: 2025-11-17
**Session ID**: claude/setup-and-planning-01FtbaWkiDaXjuA9rXF5GaTq
**Previous Session Handoff**: Phase 1 (IngestCommand) complete and tested, ready for validation and Phase 2

## Current State Assessment

### Completed (Phase 1)
- IngestCommand fully implemented with:
  - Project-based file organization (`ingests/project-name/`)
  - SHA-256 content hashing for duplicate detection
  - Automated duplicate renaming (hash-suffix pattern)
  - Secret detection via `detect-secrets` (warnings only)
  - Self-rendering result objects (text/JSON output)
  - Dry-run mode support
- All quality gates passed (linters, type checker, vulture, tests)
- Manual testing validated all features

### Known Issues
- CLI interface hangs when invoked via `python -m lmscribbles ingest ...`
- Direct instantiation works perfectly
- Suspected tyro parsing issue with Annotated types

## Next Steps Recommendations (from Handoff)

### 1. Validate with Real Scribbles (Immediate Priority)
**Objective**: Import actual scribbles from existing repositories to validate end-to-end workflow.

**Questions**:
- Which repository should we start with for validation? (python-librovore mentioned in git status)
- Should we create a test ingestion workflow before importing production scribbles?
- Do we need to fix the CLI hang issue before validation, or can we use programmatic testing?
- Should validation include stress testing with large scribble collections?

**Proposed Approach**:
1. First, investigate and fix the CLI hang issue to ensure proper user workflow
2. Select a small, representative scribble collection for initial validation
3. Document validation results and any edge cases discovered
4. Use findings to inform Phase 2 design decisions

### 2. Classification System (Phase 2a)
**Objective**: Build file-based metadata/tagging system with LLM-assisted classification.

#### Metadata Storage Strategy

**Questions**:
- Should metadata files be sidecar files (`.metadata.yaml` alongside each scribble)?
- Or centralized index file per project (`ingests/project-name/.index.yaml`)?
- How do we handle metadata for selections (symlinks to ingests)?
- Should we version metadata schema for future evolution?

**Proposed Metadata Schema** (preliminary):
```yaml
# Example: ingests/lm-scribbles/.index.yaml or per-file sidecar
scribbles:
  file-1.ext:
    content_hash: "sha256:abc123..."
    ingested_at: "2025-11-17T21:00:00Z"
    size_bytes: 1024
    source_path: "/original/path/file-1.ext"
    labels:
      - topic:architecture
      - quality:gem
      - language:python
    notes: "Interesting approach to async CLI patterns"
    classification_method: "manual|llm-assisted|auto"
    llm_confidence: 0.85  # If LLM-classified
```

**Alternative: Lightweight JSON Lines Format**:
```jsonl
{"file": "file-1.ext", "hash": "abc123", "labels": ["topic:architecture"], "notes": "..."}
{"file": "file-2.ext", "hash": "def456", "labels": ["topic:testing"], "notes": "..."}
```

#### Label Taxonomy

**Questions**:
- Should we use namespaced labels (`topic:architecture`) or flat tags?
- Pre-defined taxonomy vs. free-form tagging?
- How to handle label evolution (renaming, merging, deprecation)?

**Proposed Taxonomy** (from architecture notes, with extensions):

**Source Context**:
- `source:debug` - Debugging session output
- `source:exploration` - Exploratory coding/research
- `source:poc` - Proof of concept implementation
- `source:investigation` - Problem investigation notes

**Quality Assessment**:
- `quality:gem` - High-value insight, definitely keep
- `quality:interesting` - Worth reviewing, potential value
- `quality:routine` - Standard work, reference value
- `quality:noise` - Low value, candidate for cleanup

**Topic Categories**:
- `topic:architecture` - System design, patterns
- `topic:algorithm` - Algorithm development, optimization
- `topic:api-design` - API interface design
- `topic:bug-fix` - Bug investigation and fixes
- `topic:testing` - Test development, strategies
- `topic:documentation` - Documentation approaches

**Language/Tech**:
- `lang:python`, `lang:rust`, `lang:typescript`, etc.
- `tech:async`, `tech:cli`, `tech:web`, etc.

**Project Tags**:
- `project:lm-scribbles`, `project:python-librovore`, etc.

#### ClassifyCommand Design

**Questions**:
- Interactive mode (one file at a time with prompts)?
- Batch mode (apply same labels to multiple files)?
- LLM-assisted mode (suggest labels, user confirms)?
- Support for bulk operations (e.g., "tag all Python files in project X")?

**Proposed Interface Ideas**:
```bash
# Interactive single-file classification
lmscribbles classify ingests/project-name/file.ext

# Batch classification
lmscribbles classify ingests/project-name/*.py --labels "lang:python,source:exploration"

# LLM-assisted classification (suggest labels from content)
lmscribbles classify ingests/project-name/file.ext --llm-assist

# Review/update existing classifications
lmscribbles classify --review --filter "quality:interesting"
```

**Implementation Considerations**:
- Use `rich` prompts for interactive classification
- LLM integration: Which model/API? (OpenAI, Anthropic, local?)
- Prompt engineering: How to extract meaningful labels from scribble content?
- Confidence scoring: How to indicate LLM classification confidence?

### 3. Selection Workflow (Phase 2b)
**Objective**: Tools to promote files from `ingests/` → `selections/`.

**Questions**:
- Should selection be based on classification labels (e.g., "select all quality:gem")?
- Interactive review mode with preview?
- Preserve directory structure vs. flatten selections?
- Handle selections metadata separately from ingests metadata?

**Proposed SelectCommand Interface**:
```bash
# Select by label query
lmscribbles select --filter "quality:gem AND topic:architecture"

# Interactive review mode
lmscribbles select --interactive --filter "quality:interesting"

# Preview without creating symlinks
lmscribbles select --dry-run --filter "lang:python"
```

**Implementation Considerations**:
- Symlink management (create, verify, cleanup broken links)
- Metadata handling: Copy/reference ingests metadata?
- Provenance tracking: Record why/when file was selected

### 4. Search/Query (Phase 2c)
**Objective**: Query scribbles by content and metadata.

**Questions**:
- Should search be hybrid (content + metadata)?
- Use external tools (ripgrep, ag) or implement in Python?
- Support for complex queries (boolean logic, regex)?
- Output format: List files, show snippets, full content?

**Proposed SearchCommand Interface**:
```bash
# Content search
lmscribbles search "async.*await" --type python

# Metadata search
lmscribbles search --labels "quality:gem" --project lm-scribbles

# Hybrid search
lmscribbles search "CLI patterns" --labels "topic:architecture"

# Date range filtering
lmscribbles search --after 2025-11-01 --before 2025-11-30
```

**Implementation Considerations**:
- Index content for faster search? (maybe defer to Phase 3+)
- Integration with external tools vs. pure Python implementation
- Result ranking/relevance scoring

### 5. Configuration System
**Objective**: Externalize settings via `appcore` config.

**Questions**:
- What settings should be configurable?
- Configuration file location/format (YAML, TOML)?
- Environment variable overrides?

**Proposed Configuration Settings**:
```yaml
# ~/.config/lm-scribbles/config.yaml or project-local config

directories:
  ingests: "./ingests"
  selections: "./selections"
  refinements: "./refinements"

secrets:
  check_enabled: true
  plugins:
    - Base64HighEntropyString
    - KeywordDetector

classification:
  default_labels: []
  llm_provider: "anthropic"  # or "openai", "local"
  llm_model: "claude-sonnet-4"
  llm_confidence_threshold: 0.7

search:
  default_output_format: "text"  # or "json"
  max_results: 100
```

## Technical Investigations Needed

### 1. CLI Hang Issue (High Priority)
**Problem**: `python -m lmscribbles ingest ...` hangs, but direct instantiation works.

**Investigation Steps**:
1. Add debug logging to `__main__.py` and `cli.py` entry points
2. Test with minimal tyro example to isolate issue
3. Check tyro version compatibility with Annotated types
4. Review vibelinter for differences in tyro usage
5. Consider alternative CLI frameworks if tyro issues persist

### 2. LLM Integration Strategy
**Questions**:
- Which LLM API to support initially? (Anthropic Claude, OpenAI, both?)
- How to handle API authentication/credentials?
- Prompt engineering: What context to provide for classification?
- Token usage optimization: Full file content vs. snippets?
- Fallback strategy if LLM API unavailable?

**Proposed LLM Prompt Template** (for classification):
```
You are analyzing code scribbles (LLM-generated content) for classification.

File: {filename}
Content preview:
```
{content_preview}
```

Based on this content, suggest appropriate labels from these categories:
- Source: debug, exploration, poc, investigation
- Quality: gem, interesting, routine, noise
- Topic: architecture, algorithm, api-design, bug-fix, testing, documentation
- Language: python, rust, typescript, etc.

Provide:
1. Suggested labels (comma-separated)
2. Confidence score (0-1)
3. Brief reasoning

Format as JSON.
```

### 3. Metadata Storage Performance
**Considerations**:
- File I/O overhead for per-file metadata vs. centralized index
- Concurrent access patterns (multiple classify operations)
- Metadata versioning and migration strategy
- Backup and recovery (metadata in git vs. external storage)

## Immediate Action Items

### Session Priorities
1. Fix CLI hang issue (enables proper user workflow testing)
2. Validate IngestCommand with real scribbles from python-librovore or similar
3. Design metadata schema and storage strategy
4. Prototype ClassifyCommand basic implementation (no LLM initially)
5. Document findings and update architecture notes

### For Next Session
- Results of CLI hang investigation
- Validation results with real scribbles
- Metadata schema proposal (with examples)
- Basic ClassifyCommand implementation
- Updated architecture decisions based on validation findings

## Open Design Questions

1. **Metadata Evolution**: How do we handle schema changes over time without breaking existing classifications?

2. **LLM Provider Abstraction**: Should we abstract LLM interactions to support multiple providers easily?

3. **Offline Mode**: Should classification/search work without LLM access (fallback to manual/keyword-based)?

4. **Multi-user Workflows**: Future consideration for shared scribbles repositories?

5. **Refinements Workflow**: How does the refinement process work? Manual editing, LLM-assisted rewriting, or both?

6. **Export/Import**: Should we support exporting classifications to other formats (JSON, CSV) for analysis?

7. **Statistics/Reporting**: Value in tracking classification stats (most common labels, quality distribution, etc.)?

## Notes for Collaboration

**Strengths of Current Implementation**:
- Clean separation of concerns (CLI, commands, results)
- Strong typing with comprehensive type annotations
- Self-rendering result objects (excellent pattern)
- Robust error handling and reporting
- Good testing foundation

**Areas to Explore**:
- LLM integration patterns (new territory for this codebase)
- Metadata management best practices
- Interactive CLI workflows (prompts, confirmations)
- Performance optimization for large scribble collections

**Questions for Project Owner**:
1. Is there a preferred LLM API for classification assistance?
2. What's the typical size of scribble collections to expect?
3. Are there existing classification schemes from other tools we should align with?
4. Priority between fixing CLI hang vs. moving forward with validation?

## Session Handoff Template

For the next Claude Code session, I'll document:
- [ ] CLI hang investigation results
- [ ] Real scribble validation outcomes
- [ ] Metadata schema decisions
- [ ] ClassifyCommand progress
- [ ] Any new architectural decisions or changes
- [ ] Updated test results and quality gate status
