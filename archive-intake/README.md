# Archive Intake

A portable agent workflow for safely unpacking archives from connected storage
without making the user manually download and unzip them.

## Why

Many agent environments can read a file from Google Drive, a conversation, or a
library but do not expose an "Extract" button. The correct abstraction is not UI
automation. It is:

1. fetch/materialize raw bytes
2. preflight the archive
3. extract in a disposable workspace
4. verify with hashes
5. optionally persist the verified tree

## Works with

- ChatGPT file/library and connected-drive workflows
- Hermes or other agents with filesystem + Python access
- Claude/Cowork-style environments with a local workspace
- MCP/custom integrations that can hand raw files to a runtime

## Files

- `SKILL.md` — agent behavior and safety contract
- `scripts/safe_extract.py` — standard-library ZIP/TAR extractor
- `tests/test_safe_extract.py` — deterministic safety and structure tests

## Example

```bash
python3 scripts/safe_extract.py bundle.zip /tmp/bundle
```

The command creates `_extraction_manifest.json` in the destination with SHA-256
checksums for the source archive and every extracted file.

## Design rules

- preserve original folder structure
- no path traversal
- no archive links or special files
- no automatic execution of extracted content
- no trust based on email attachment ordering
- persistence back to cloud storage is optional and separate from extraction
