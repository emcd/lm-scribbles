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

See `.auxiliary/notes/issues.md` for current issue tracking.

## Real Scribbles Analysis (python-librovore)

**Date**: 2025-11-17
**Source**: `ingests/python-librovore/` (190 files ingested)

### File Distribution

**By Type**:
- Python scripts: 143 (75%)
- HTML files: 36 (19%) - Documentation samples from Sphinx themes
- JSON files: 7 (4%) - Structured data from inventory analysis
- Markdown files: 3 (2%) - Architecture analysis documents
- Shell scripts: 1 (<1%)

**Python Script Categories**:
- Test POCs (`test_*.py`): 76 files (53% of Python)
- Debug scripts (`debug_*.py`): 27 files (19% of Python)
- Analysis/comparison scripts: ~15 files (10% of Python)
- Utility/conversion scripts: ~25 files (17% of Python)

### Scribble Patterns Observed

#### 1. Test/Proof-of-Concept Scripts
**Examples**: `test_mkdocs_reg.py`, `test_cache_bypass.py`, `test_import_availability.py`

**Characteristics**:
- Small, focused scripts (typically <100 LOC)
- Often test new features or validate API behavior
- Mix of pytest-style tests and standalone execution
- Frequently use `#!/usr/bin/env python3` shebang

**Typical Content**:
```python
#!/usr/bin/env python3
import librovore.module
print('Before:', state)
result = module.function()
print('After:', state)
```

**Value**: High for understanding feature exploration and validation patterns

#### 2. Debug/Investigation Scripts
**Examples**: `debug_extraction.py`, `debug_pytest.py`, `debug_remote_extraction.py`

**Characteristics**:
- Longer scripts investigating specific issues
- Often include detailed print/logging statements
- Web scraping/HTML parsing for documentation analysis
- BeautifulSoup, urllib usage for live testing

**Typical Content**:
- URL fetching and HTML analysis
- Selector experimentation
- Data structure exploration
- Step-by-step problem diagnosis

**Value**: Very high - capture problem-solving thought process

#### 3. Analysis Documents
**Examples**: `cache_config_analysis.md`, `robots_fix_analysis.md`

**Characteristics**:
- Markdown format with tables and code examples
- Compare alternative architectural approaches
- Document design trade-offs
- Often include "Options" sections with pros/cons

**Typical Content**:
- Configuration pattern analysis
- Alternative architecture proposals
- Field usage comparison tables
- Recommendations for refactoring

**Value**: Extremely high - capture architectural thinking and decisions

#### 4. Data Samples/Artifacts
**Examples**: HTML files (Sphinx theme samples), JSON files (inventory analysis)

**Characteristics**:
- Reference material from external sources
- Sphinx theme HTML samples (furo, rtd, pydata, etc.)
- JSON output from analysis scripts
- Used for comparison and pattern extraction

**Typical Files**:
- `pydata-sphinx-theme-structure.html` (25KB)
- `inventory_analysis.json` (structured inventory data)
- `mkdocs_search_results.json` (API response samples)

**Value**: Generally low - data files are usually uninteresting except when they contain synthetic test data. These samples are reference material for understanding patterns, which is moderately valuable

#### 5. Batch Conversion/Refactoring Scripts
**Examples**: `batch_convert_remaining_tests.py`, `update_query_tests.py`

**Characteristics**:
- Regex-based code transformation
- Automated refactoring utilities
- Migration helpers for API changes
- Often one-time use scripts

**Typical Content**:
- Pattern matching for code elements
- Replacement logic with multiple conversion patterns
- File reading/writing operations

**Value**: Medium - useful for understanding refactoring strategies

#### 6. Comprehensive Analysis/Summary Scripts
**Examples**: `comprehensive_summary.py`, `compare_formats.py`, `compare_schemas.py`

**Characteristics**:
- Aggregate data from multiple sources
- Generate comparative reports
- Cross-theme or cross-format analysis
- Often produce formatted output (tables, charts)

**Typical Content**:
- Data loading from JSON files
- Pattern aggregation across samples
- Consistency checking
- Report generation with emojis/formatting

**Value**: High - demonstrate analytical approaches

### Classification Insights

Based on the real scribbles, here are refined categorization recommendations:

#### Recommended Label Additions

**Purpose-Based Labels** (new category):
- `purpose:test-poc` - Testing/proof-of-concept (replaces generic `source:poc`)
- `purpose:debug` - Debug/investigation scripts (replaces `source:debug`)
- `purpose:analysis` - Analysis documents and scripts
- `purpose:refactor` - Refactoring/migration utilities
- `purpose:reference` - Reference material/samples (HTML, JSON data)

**Content Type Labels** (new category):
- `format:script` - Executable Python scripts
- `format:document` - Markdown/text documents
- `format:data` - JSON/structured data
- `format:sample` - HTML/external samples

**Scope Labels** (new category):
- `scope:minimal` - Small, focused scripts (<50 LOC)
- `scope:moderate` - Medium scripts (50-200 LOC)
- `scope:comprehensive` - Large analysis/summary scripts (>200 LOC)

**Technology Tags** (refined):
- `tech:web-scraping` - BeautifulSoup, urllib, requests
- `tech:testing` - pytest, test utilities
- `tech:sphinx` - Sphinx documentation system
- `tech:mkdocs` - MkDocs documentation system
- `tech:async` - Asyncio patterns

#### Quality Assessment Heuristics

Based on observed patterns, suggest these quality indicators:

**Likely `quality:gem`**:
- Markdown analysis documents with comparison tables
- Comprehensive summary/analysis scripts
- Scripts with detailed comments explaining approach

**Likely `quality:interesting`**:
- Debug scripts solving non-trivial problems
- Test POCs for new features
- Comparison/validation utilities

**Likely `quality:routine`**:
- Simple test scripts with minimal logic
- One-off conversion utilities (already run)
- Basic validation checks

**Likely `quality:noise`**:
- Duplicate or superseded test scripts
- Temporary debugging scaffolding
- Note: Failed experiments can still have value if they demonstrate novel approaches

### File Naming Patterns

**Observed Conventions**:
- `test_*.py` - Test/POC scripts
- `debug_*.py` - Debug/investigation scripts
- `*_analysis.*` - Analysis documents/scripts
- `compare_*.py` - Comparison utilities
- `*-theme-*.html` - Theme samples (with theme name)
- `batch_*.py` - Batch processing utilities

**Implications for LLM-Driven Classification**:
- File naming provides strong hints for LLMs to infer labels
- Patterns can help LLMs suggest `purpose:*` labels
- Theme names in filenames help LLMs suggest `tech:*` labels
- Note: Classification is LLM-driven, not traditional heuristics/algorithms

### Multi-File Relationships

**Observed Patterns**:
- Analysis script + corresponding JSON output
  - Example: `inventory_analysis.py` + `inventory_analysis.json`
- Multiple HTML samples from same theme
  - Example: `furo-*.html`, `rtd-*.html` files
- Test suite conversions (batch + individual tests)

**Implications**:
- Consider "related files" or "file sets" in metadata
- Group classification might be useful
- Could track derivation (script → output)

### Surprising Findings

1. **High test/debug ratio**: 76 test + 27 debug = 103 files (72% of Python scripts)
   - Suggests heavy emphasis on exploration and validation
   - These are valuable learning artifacts

2. **Architecture analysis documents**: Presence of `.md` files shows conscious documentation of design thinking
   - Extremely valuable for understanding decision-making
   - Should definitely be `quality:gem`

3. **External reference samples**: HTML files are curated samples, not random web pages
   - Serve specific analytical purpose (theme comparison)
   - Moderate to high value depending on analysis results

4. **Minimal duplication**: Despite flattening issue, few actual duplicates
   - Suggests good naming hygiene in source
   - Validates that duplicate detection would be useful but not critical

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

**Approach**: Sibling TOML manifest files
- Metadata stored in `selections/project-name.toml` (sibling to `selections/project-name/` directory)
- Example: `selections/python-librovore.toml` for `selections/python-librovore/` contents
- Do NOT place metadata inside `ingests/` or `selections/` directories
- TOML format for human readability and structured data
- SQLite catalog deferred to later phases

**Schema** (as demonstrated in `selections/python-librovore.toml`):
```toml
[metadata]
project = "python-librovore"
source_directory = "ingests/python-librovore"
selections_created = "2025-11-17T22:38:00Z"

[selections.script_name]
labels = ["purpose:analysis", "quality:gem", "tech:async"]
description = "Brief description of what the script does"
selection_rationale = "Why this was selected, techniques used, value provided"
related_files = ["data.json", "other_script.py"]
loc = 176
```

#### Label Taxonomy

**Approach**: Namespaced labels (not flat tags)
- Use `namespace:value` pattern to avoid high cardinality
- Example: `purpose:analysis`, `quality:gem`, `tech:async`
- Supports organized taxonomy evolution
- Pre-defined taxonomy can emerge from LLM usage patterns

**Taxonomy** (from architecture notes and real scribbles analysis):

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

**Purpose**: Assist LLMs in classifying and selecting scribbles
- Command is used BY LLMs, not to assist users with LLM features
- LLMs review scribbles and generate metadata (as demonstrated with python-librovore selection)
- Command provides structured interface for LLMs to read/write TOML manifests
- May support batch operations for LLM efficiency

**LLM-Driven Workflow** (as demonstrated):
1. LLM reviews scribbles in `ingests/project-name/`
2. LLM selects high-value files based on content analysis
3. LLM creates symlinks in `selections/project-name/`
4. LLM generates `selections/project-name.toml` with metadata
   - Labels, descriptions, selection rationale
   - Related files, techniques, statistics

**Potential Command Interface**:
```bash
# Used by LLM to structure selection workflow
lmscribbles classify --project python-librovore --review

# LLM could batch-update metadata
lmscribbles classify --update selections/python-librovore.toml
```

**Note**: The classify command may be optional - LLMs can directly manipulate files and TOML as demonstrated

### 3. Selection Workflow (Phase 2b)
**Objective**: LLM-driven curation to promote files from `ingests/` → `selections/`.

**LLM-Driven Approach** (as demonstrated):
- LLM reviews all files in ingests directory
- LLM applies judgment to identify high-value scribbles
- LLM creates symlinks for selected files
- LLM generates comprehensive TOML manifest with metadata

**Demonstrated Workflow**:
1. LLM reads scribbles from `ingests/project-name/`
2. LLM analyzes content, patterns, techniques
3. LLM creates `selections/project-name/` directory
4. LLM creates relative symlinks to selected files
5. LLM writes `selections/project-name.toml` with:
   - Per-file labels, descriptions, rationale
   - Statistics, relationships, insights

**Selection Rate**: ~7% (14/190 for python-librovore)
- Quality over quantity
- LLM judgment identifies gems, novel approaches, valuable patterns

### 4. Search/Query and Configuration

**Status**: Deferred until after taxonomy and classification are settled
- Search/query functionality will be designed based on actual usage patterns
- Configuration system will emerge from concrete needs

## LLM Integration Strategy

**Approach**: LLMs work directly with the codebase (as demonstrated)

**What LLMs Do**:
1. Read scribbles from `ingests/project-name/`
2. Analyze content using their training (no special API integration needed)
3. Apply judgment to identify valuable patterns, novel approaches, insights
4. Create symlinks in `selections/project-name/`
5. Write comprehensive TOML manifests with metadata

**Demonstrated Workflow** (python-librovore selection):
- LLM reviewed 190 files (143 Python scripts, 36 HTML, 7 JSON, 3 MD)
- Selected 14 high-value files (~7% selection rate)
- Created relative symlinks preserving original content
- Generated detailed TOML with:
  - Namespaced labels (purpose, quality, tech, scope)
  - Selection rationale explaining value
  - Related files, techniques, LOC statistics
  - Summary statistics and insights
  - Recommendations for future classifications

**No Special API Integration Needed**:
- LLMs use their standard capabilities (reading, analyzing, writing)
- TOML format is human-readable and LLM-friendly
- Selection is conversational: human asks, LLM curates
- No prompt templates or confidence scoring required

**Benefits**:
- Flexible: LLMs adapt approach based on scribble characteristics
- Comprehensive: LLMs provide rich context and rationale
- Evolving: Taxonomy emerges from actual usage patterns
- Simple: No API keys, no special infrastructure

## Completed Validations

### Session Accomplishments
1. ✅ Validated IngestCommand with real scribbles (python-librovore: 190 files)
2. ✅ Designed and demonstrated metadata schema (TOML sibling manifests)
3. ✅ Demonstrated LLM-driven selection workflow (~7% selection rate)
4. ✅ Generated comprehensive metadata with labels, rationale, insights
5. ✅ Documented findings and updated architecture understanding

### Key Learnings
- LLM-driven selection is practical and produces rich metadata
- Sibling TOML manifests work well for structured metadata
- Namespaced labels provide organized taxonomy
- Selection quality over quantity (14/190 = 7.4%)
- Real scribbles reveal valuable patterns for classification design

## Open Design Questions

1. **Metadata Evolution**: How to handle schema changes over time without breaking existing classifications?

2. **Refinements Workflow**: How does refinement work? Manual editing, LLM-assisted rewriting, or both?

3. **Multi-project Relationships**: How to track relationships across scribbles from different projects?

4. **Label Consolidation**: As taxonomy emerges, how to consolidate similar labels?

## Next Phase Priorities

Based on validated approach:

1. **Fix IngestCommand Issues**:
   - Preserve source directory hierarchy (Issue #1)
   - Add `prefix_name=False` to tyro arguments (Issue #2)

2. **Refine Classification Taxonomy**:
   - Evolve labels based on more project selections
   - Document label meanings and usage guidelines
   - Consider cross-project label consistency

3. **Iterate on Selection Workflow**:
   - Apply to more projects to validate approach
   - Refine TOML schema based on actual needs
   - Document selection patterns and heuristics

4. **Explore Refinements**:
   - Design refinement workflow (LLM-assisted)
   - Consider how refined scribbles differ from selections
   - Determine refinement metadata needs
