from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any, cast

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
from referencing import Registry, Resource

from tendy_spider_contracts import validate_contract

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PACKAGE_ROOT.parents[1]
SCHEMA_DIR = PACKAGE_ROOT / "schemas"
FIXTURE_DIR = REPOSITORY_ROOT / "tests" / "fixtures" / "contracts"

SCHEMAS = {
    path.name: json.loads(path.read_text()) for path in sorted(SCHEMA_DIR.glob("*.schema.json"))
}
CATALOG = cast(dict[str, Any], json.loads((PACKAGE_ROOT / "catalog.json").read_text()))


def load_fixture(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((FIXTURE_DIR / name).read_text()))


def build_registry() -> Registry:
    registry = Registry()
    for schema in SCHEMAS.values():
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return registry


class ContractSchemaTests(unittest.TestCase):
    registry: Registry

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = build_registry()
        for schema in SCHEMAS.values():
            Draft202012Validator.check_schema(schema)

    def assert_valid(self, fixture: str, schema: str) -> None:
        payload = load_fixture(fixture)
        Draft202012Validator(SCHEMAS[schema], registry=self.registry).validate(payload)
        record = validate_contract(payload)
        self.assertEqual(
            record,
            validate_contract(record.model_dump(mode="json")),
            f"{fixture} must be stable across the canonical JSON boundary",
        )

    def assert_invalid(self, fixture: str, schema: str) -> None:
        payload = load_fixture(fixture)
        schema_failed = False
        model_failed = False
        try:
            Draft202012Validator(SCHEMAS[schema], registry=self.registry).validate(payload)
        except Exception:
            schema_failed = True
        try:
            validate_contract(payload)
        except Exception:
            model_failed = True
        self.assertTrue(schema_failed or model_failed, fixture)

    def test_all_schemas_are_valid_draft_2020_12(self) -> None:
        self.assertGreaterEqual(len(SCHEMAS), 12)
        catalog_paths = cast(dict[str, str], CATALOG["schemas"])
        catalog_schema_names = {Path(path).name for path in catalog_paths.values()}
        self.assertEqual(catalog_schema_names, set(SCHEMAS) - {"common.schema.json"})

    def test_valid_temporal_and_point_in_time_cases(self) -> None:
        cases = [
            ("valid_renamed_symbol_mapping.json", "symbol-mapping.schema.json"),
            ("valid_split_adjusted_bar.json", "price-bar.schema.json"),
            ("valid_restatement_fact.json", "fundamental-fact.schema.json"),
            ("valid_stale_macro_observation.json", "macro-observation.schema.json"),
            ("valid_quote.json", "quote.schema.json"),
            ("valid_filing_amendment.json", "filing.schema.json"),
            ("valid_document.json", "document.schema.json"),
            ("valid_evidence_item.json", "evidence-item.schema.json"),
            ("valid_short_volume.json", "market-statistic.schema.json"),
            ("valid_corporate_action_split.json", "corporate-action.schema.json"),
            ("valid_instrument_identity.json", "instrument-identity.schema.json"),
        ]
        for fixture, schema in cases:
            with self.subTest(fixture=fixture):
                self.assert_valid(fixture, schema)

    def test_rejects_ambiguous_or_incomplete_records(self) -> None:
        cases = [
            ("invalid_naive_timestamp_bar.json", "price-bar.schema.json"),
            ("invalid_missing_source_bar.json", "price-bar.schema.json"),
            ("invalid_silent_adjustment_bar.json", "price-bar.schema.json"),
            (
                "invalid_restatement_without_predecessor_fact.json",
                "fundamental-fact.schema.json",
            ),
        ]
        for fixture, schema in cases:
            with self.subTest(fixture=fixture):
                self.assert_invalid(fixture, schema)


if __name__ == "__main__":
    unittest.main()
