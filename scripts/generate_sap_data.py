"""Generate deterministic synthetic SAP FI/CO extracts for the portfolio project."""

from __future__ import annotations

import argparse
import csv
import random
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SEED_DIR = PROJECT_ROOT / "dbt" / "seeds"

FIELDNAMES = {
    "bkpf.csv": [
        "mandt",
        "bukrs",
        "belnr",
        "gjahr",
        "blart",
        "budat",
        "waers",
        "cpudt",
        "cputm",
    ],
    "bseg.csv": [
        "source_row_id",
        "mandt",
        "bukrs",
        "belnr",
        "gjahr",
        "buzei",
        "hkont",
        "shkzg",
        "dmbtr",
        "wrbtr",
        "kostl",
        "aufnr",
        "sgtxt",
    ],
    "cobk.csv": [
        "mandt",
        "kokrs",
        "bukrs",
        "belnr",
        "gjahr",
        "vrgng",
        "budat",
        "waers",
        "refbn",
        "refgj",
    ],
    "coep.csv": [
        "source_row_id",
        "mandt",
        "kokrs",
        "belnr",
        "gjahr",
        "buzei",
        "objnr",
        "kstar",
        "wrttp",
        "wkgbtr",
        "wrbtr",
        "parob",
    ],
    "tcurr.csv": ["from_currency", "to_currency", "valid_from", "valid_to", "rate"],
    "gl_accounts.csv": ["hkont", "account_name", "account_category"],
}


def money(value: Decimal) -> str:
    """Return a stable two-decimal representation for CSV output."""
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def write_csv(filename: str, rows: list[dict[str, object]]) -> None:
    SEED_DIR.mkdir(parents=True, exist_ok=True)
    destination = SEED_DIR / filename
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES[filename])
        writer.writeheader()
        writer.writerows(rows)


def generate(documents: int, seed: int) -> dict[str, int]:
    """Create SAP-style seed files and return generated row counts."""
    if documents < 8:
        raise ValueError("At least 8 documents are required to inject all failure scenarios.")

    rng = random.Random(seed)
    fiscal_year = 2026
    base_date = date(2026, 1, 2)

    headers: list[dict[str, object]] = []
    lines: list[dict[str, object]] = []
    co_headers: list[dict[str, object]] = []
    co_lines: list[dict[str, object]] = []

    local_rates = {
        "USD": Decimal("1.00"),
        "EUR": Decimal("1.08"),
        "GBP": Decimal("1.25"),
    }
    currencies = ["USD", "EUR", "USD", "EUR"]
    row_number = 1

    for index in range(1, documents + 1):
        fi_document = f"19{index:08d}"
        co_document = f"20{index:08d}"
        posting_date = base_date + timedelta(days=index % 27)
        currency = "GBP" if index == 6 else currencies[index % len(currencies)]
        usd_amount = Decimal(rng.randrange(125, 5000))
        document_amount = usd_amount / local_rates[currency]

        headers.append(
            {
                "mandt": "100",
                "bukrs": "1000",
                "belnr": fi_document,
                "gjahr": fiscal_year,
                "blart": "KR",
                "budat": posting_date.isoformat(),
                "waers": currency,
                "cpudt": posting_date.isoformat(),
                "cputm": f"08{index % 60:02d}00",
            }
        )

        debit_line = {
            "source_row_id": f"FI{row_number:08d}",
            "mandt": "100",
            "bukrs": "1000",
            "belnr": fi_document,
            "gjahr": fiscal_year,
            "buzei": "001",
            "hkont": "500000" if index % 2 else "500100",
            "shkzg": "S",
            "dmbtr": money(usd_amount),
            "wrbtr": money(document_amount),
            "kostl": "CC1000" if index % 2 else "CC2000",
            "aufnr": "",
            "sgtxt": "Synthetic operating expense",
        }
        row_number += 1

        credit_amount = usd_amount - Decimal("10.00") if index == 5 else usd_amount
        credit_line = {
            "source_row_id": f"FI{row_number:08d}",
            "mandt": "100",
            "bukrs": "1000",
            "belnr": fi_document,
            "gjahr": fiscal_year,
            "buzei": "002",
            "hkont": "200000",
            "shkzg": "H",
            "dmbtr": money(credit_amount),
            "wrbtr": money(credit_amount / local_rates[currency]),
            "kostl": "",
            "aufnr": "",
            "sgtxt": "Synthetic vendor payable",
        }
        row_number += 1
        lines.extend([debit_line, credit_line])

        # The third document contains one duplicate business key. One copy remains valid.
        if index == 3:
            duplicate = dict(debit_line)
            duplicate["source_row_id"] = f"FI{row_number:08d}"
            duplicate["sgtxt"] = "Injected duplicate source record"
            row_number += 1
            lines.append(duplicate)

        # Documents rejected as a whole do not produce trusted CO records.
        # Document 3 remains publishable after only its duplicate row is quarantined.
        if index in {5, 6}:
            continue

        co_headers.append(
            {
                "mandt": "100",
                "kokrs": "A000",
                "bukrs": "1000",
                "belnr": co_document,
                "gjahr": fiscal_year,
                "vrgng": "RKP1",
                "budat": posting_date.isoformat(),
                "waers": "USD",
                "refbn": fi_document,
                "refgj": fiscal_year,
            }
        )

        co_amount = usd_amount + Decimal("25.00") if index == 7 else usd_amount
        co_lines.append(
            {
                "source_row_id": f"CO{index:08d}",
                "mandt": "100",
                "kokrs": "A000",
                "belnr": co_document,
                "gjahr": fiscal_year,
                "buzei": "001",
                "objnr": "KSCC1000" if index % 2 else "KSCC2000",
                "kstar": debit_line["hkont"],
                "wrttp": "04",
                "wkgbtr": money(co_amount),
                "wrbtr": money(co_amount),
                "parob": "",
            }
        )

    # One orphan line has no corresponding BKPF header.
    lines.append(
        {
            "source_row_id": f"FI{row_number:08d}",
            "mandt": "100",
            "bukrs": "1000",
            "belnr": "1999999999",
            "gjahr": fiscal_year,
            "buzei": "001",
            "hkont": "500000",
            "shkzg": "S",
            "dmbtr": "100.00",
            "wrbtr": "100.00",
            "kostl": "CC1000",
            "aufnr": "",
            "sgtxt": "Injected orphan line",
        }
    )

    exchange_rates = [
        {
            "from_currency": "USD",
            "to_currency": "USD",
            "valid_from": "2026-01-01",
            "valid_to": "2026-12-31",
            "rate": "1.00",
        },
        {
            "from_currency": "EUR",
            "to_currency": "USD",
            "valid_from": "2026-01-01",
            "valid_to": "2026-12-31",
            "rate": "1.08",
        },
    ]
    accounts = [
        {"hkont": "200000", "account_name": "Trade payables", "account_category": "LIABILITY"},
        {"hkont": "500000", "account_name": "Maintenance expense", "account_category": "EXPENSE"},
        {"hkont": "500100", "account_name": "IT services expense", "account_category": "EXPENSE"},
    ]

    datasets = {
        "bkpf.csv": headers,
        "bseg.csv": lines,
        "cobk.csv": co_headers,
        "coep.csv": co_lines,
        "tcurr.csv": exchange_rates,
        "gl_accounts.csv": accounts,
    }
    for filename, rows in datasets.items():
        write_csv(filename, rows)

    return {filename: len(rows) for filename, rows in datasets.items()}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--documents", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    counts = generate(args.documents, args.seed)
    for name, count in counts.items():
        print(f"generated {name}: {count} rows")
