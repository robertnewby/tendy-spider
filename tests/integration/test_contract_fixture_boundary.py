"""Offline cross-package checks for the public contract validation boundary."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest
from tendy_spider_contracts import validate_contract

pytestmark = pytest.mark.integration

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = REPOSITORY_ROOT / "tests" / "fixtures" / "contracts"


def valid_fixture_paths() -> list[Path]:
    return sorted(FIXTURE_DIR.glob("valid_*.json"))


def load_fixture(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


@pytest.mark.parametrize("fixture_path", valid_fixture_paths(), ids=lambda path: path.stem)
def test_valid_fixture_round_trips_through_the_public_contract_boundary(
    fixture_path: Path,
) -> None:
    """Fixtures must be deterministic and retain required evidence metadata."""

    payload = load_fixture(fixture_path)
    record = validate_contract(payload)
    replayed_record = validate_contract(record.model_dump(mode="json"))

    assert replayed_record == record
    assert record.provenance.source.source_record_id or record.provenance.source.source_url
    assert record.provenance.times.knowable_at <= record.provenance.times.retrieved_at
    assert record.provenance.freshness.determined_at.tzinfo is not None
