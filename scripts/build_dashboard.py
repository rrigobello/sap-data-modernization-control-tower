"""Build a dependency-light static HTML control tower from DuckDB results."""

from __future__ import annotations

import html
import os
from datetime import UTC, datetime
from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = Path(
    os.environ.get("CONTROL_TOWER_DB_PATH", PROJECT_ROOT / "data" / "control_tower.duckdb")
)
SITE_DIR = PROJECT_ROOT / "site"


def render_rows(rows: list[tuple[object, ...]]) -> str:
    return "\n".join(
        "<tr>" + "".join(f"<td>{html.escape(str(value))}</td>" for value in row) + "</tr>"
        for row in rows
    )


def render_cards(metrics: list[tuple[str, int]]) -> str:
    cards = []
    for label, value in metrics:
        css_class = "card warning" if "exception" in label.lower() or "quarantined" in label.lower() else "card"
        cards.append(
            f'<section class="{css_class}"><span>{html.escape(label)}</span>'
            f"<strong>{value:,}</strong></section>"
        )
    return "\n".join(cards)


def main() -> None:
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}. Run the dbt pipeline first.")

    connection = duckdb.connect(str(DATABASE_PATH), read_only=True)
    metrics = connection.execute(
        "SELECT metric, metric_value FROM marts.rpt_control_tower_summary ORDER BY metric"
    ).fetchall()
    reasons = connection.execute(
        """
        SELECT quarantine_reason, COUNT(*) AS rejected_rows
        FROM marts.quarantine_fi_line_items
        GROUP BY quarantine_reason
        ORDER BY rejected_rows DESC, quarantine_reason
        """
    ).fetchall()
    exceptions = connection.execute(
        """
        SELECT
            accounting_document,
            fiscal_year,
            fi_expense_amount,
            co_primary_cost_amount,
            difference_amount,
            reconciliation_status
        FROM marts.rpt_fi_co_reconciliation
        WHERE reconciliation_status <> 'MATCH'
        ORDER BY accounting_document
        """
    ).fetchall()
    connection.close()

    generated_at = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    dashboard = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SAP Data Modernization Control Tower</title>
  <style>
    :root {{ color-scheme: dark; --bg:#07111f; --panel:#101f33; --line:#253b55;
            --text:#edf4ff; --muted:#91a5bd; --accent:#37c9a5; --warn:#ffb44c; }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; font:15px/1.5 Inter,Segoe UI,sans-serif; background:var(--bg); color:var(--text); }}
    main {{ width:min(1180px,92vw); margin:48px auto 80px; }}
    h1 {{ margin:0; font-size:clamp(2rem,5vw,3.5rem); letter-spacing:-.04em; }}
    .subtitle {{ color:var(--muted); max-width:760px; margin:8px 0 32px; }}
    .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(175px,1fr)); gap:14px; }}
    .card {{ background:linear-gradient(145deg,#12263d,#0d1a2c); border:1px solid var(--line);
             border-radius:14px; padding:20px; }}
    .card span {{ color:var(--muted); display:block; min-height:44px; }}
    .card strong {{ color:var(--accent); display:block; font-size:2rem; margin-top:8px; }}
    .card.warning strong {{ color:var(--warn); }}
    .grid {{ display:grid; grid-template-columns:1fr 2fr; gap:18px; margin-top:26px; }}
    .panel {{ background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:20px; overflow:auto; }}
    h2 {{ margin:0 0 14px; font-size:1.05rem; }}
    table {{ width:100%; border-collapse:collapse; white-space:nowrap; }}
    th,td {{ text-align:left; padding:10px 12px; border-bottom:1px solid var(--line); }}
    th {{ color:var(--muted); font-size:.75rem; text-transform:uppercase; letter-spacing:.08em; }}
    footer {{ color:var(--muted); margin-top:20px; font-size:.8rem; }}
    @media (max-width:800px) {{ .grid {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body>
<main>
  <h1>SAP Data Modernization Control Tower</h1>
  <p class="subtitle">Trusted FI/CO publication with automated quarantine, document balancing,
    and financial reconciliation. All records shown are synthetic.</p>
  <div class="cards">{render_cards(metrics)}</div>
  <div class="grid">
    <section class="panel">
      <h2>Quarantine reasons</h2>
      <table><thead><tr><th>Reason</th><th>Rows</th></tr></thead>
        <tbody>{render_rows(reasons)}</tbody></table>
    </section>
    <section class="panel">
      <h2>FI–CO reconciliation exceptions</h2>
      <table><thead><tr><th>FI document</th><th>Year</th><th>FI</th><th>CO</th><th>Difference</th><th>Status</th></tr></thead>
        <tbody>{render_rows(exceptions)}</tbody></table>
    </section>
  </div>
  <footer>Generated {generated_at} · DuckDB + dbt · Portfolio demonstration</footer>
</main>
</body>
</html>
"""

    SITE_DIR.mkdir(parents=True, exist_ok=True)
    (SITE_DIR / "index.html").write_text(dashboard, encoding="utf-8")
    print(f"dashboard written to {SITE_DIR / 'index.html'}")


if __name__ == "__main__":
    main()
