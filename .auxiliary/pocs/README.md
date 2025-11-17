# Proof of Concept Files

This directory contains example files demonstrating the IngestCommand functionality.

## Duplicate Detection and Renaming

- `test_utils.py` - Original file demonstrating basic Python utilities
- `test_utils-6881f5.py` - Same filename but different content, automatically renamed with hash suffix to avoid collision

These files demonstrate how the ingestion command:
1. Detects files with the same name
2. Compares content hashes
3. Renames files with different content using a 6-character hash suffix
4. Skips files with identical content (idempotent behavior)

## Secret Detection

- `config_with_secrets.py.base64` - Base64-encoded Python file containing test secrets

This file is Base64-encoded to prevent triggering security scanners on public repositories.
It contains 8 intentionally embedded test secrets to validate the detect-secrets integration.

To decode and view:
```bash
base64 -d config_with_secrets.py.base64
```

**Note:** The "secrets" in this file are fictional test data for validation purposes only.
