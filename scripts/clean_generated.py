"""Remove reproducible local build outputs without touching source files."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

for path in [
    PROJECT_ROOT / "data" / "control_tower.duckdb",
    PROJECT_ROOT / "data" / "control_tower.duckdb.wal",
    PROJECT_ROOT / "site" / "index.html",
]:
    if path.exists():
        path.unlink()
        print(f"removed {path}")
