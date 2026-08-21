from __future__ import annotations

import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.generate_sap_data import SEED_DIR, generate  # noqa: E402


def read_rows(filename: str) -> list[dict[str, str]]:
    with (SEED_DIR / filename).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_generator_is_deterministic_and_injects_expected_defects() -> None:
    first_counts = generate(documents=12, seed=42)
    first_bseg = read_rows("bseg.csv")

    second_counts = generate(documents=12, seed=42)
    second_bseg = read_rows("bseg.csv")

    assert first_counts == second_counts
    assert first_bseg == second_bseg
    assert len(first_bseg) == 26

    business_keys = [
        (row["mandt"], row["bukrs"], row["belnr"], row["gjahr"], row["buzei"])
        for row in first_bseg
    ]
    assert len(business_keys) > len(set(business_keys))
    assert any(row["belnr"] == "1999999999" for row in first_bseg)


def test_generator_requires_enough_documents_for_all_scenarios() -> None:
    try:
        generate(documents=7, seed=42)
    except ValueError as exc:
        assert "At least 8 documents" in str(exc)
    else:
        raise AssertionError("Expected generation to reject an undersized scenario set")
