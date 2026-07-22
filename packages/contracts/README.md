# Tendy Spider contracts

The JSON Schema 2020-12 files in `schemas/` are the canonical, portable
contracts. The Pydantic models in `src/tendy_spider_contracts/` enforce
cross-field semantics that JSON Schema cannot express conveniently, including
timestamp ordering, explicit adjustment modes, restatement lineage, and
raw/normalized/derived lineage rules.

Contract version `1.0.0` is additive within major version 1. Consumers must
reject unknown major versions and may ignore additive optional fields from a
newer minor version only when their JSON parser is configured to do so.

Run the offline contract suite from the repository root:

```bash
UV_CACHE_DIR=/tmp/tendy-spider-uv-cache uv run \
  --project packages/contracts --extra test \
  python -m unittest discover -s packages/contracts/tests -v
```
