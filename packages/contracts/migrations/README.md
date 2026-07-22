# Contract migrations

`1.0.0` is the baseline and has no predecessor or data migration.

Compatibility rules:

- additive optional fields increment the minor version;
- clarifications that do not change accepted payloads increment the patch;
- removed or renamed fields, enum narrowing, changed meanings, or newly
  required fields increment the major version and require a deterministic
  migration or dual-read compatibility window;
- persisted records retain their original `contract_version`; migrations write
  a new lineage record and never mutate raw observations in place;
- adapters must not introduce provider-specific fields into core records.

Future migrations belong in a versioned subdirectory with a fixture for the
old payload, expected migrated payload, rollback/compatibility notes, and an
offline test.
