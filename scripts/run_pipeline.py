"""Run the complete local/GitHub demonstration pipeline."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], env: dict[str, str]) -> None:
    print(f"\n> {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=PROJECT_ROOT, env=env, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--documents", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    (PROJECT_ROOT / "data").mkdir(exist_ok=True)
    env = os.environ.copy()
    env.setdefault("CONTROL_TOWER_DB_PATH", str(PROJECT_ROOT / "data" / "control_tower.duckdb"))

    run(
        [
            sys.executable,
            "scripts/generate_sap_data.py",
            "--documents",
            str(args.documents),
            "--seed",
            str(args.seed),
        ],
        env,
    )
    run(
        [
            "dbt",
            "seed",
            "--project-dir",
            "dbt",
            "--profiles-dir",
            "profiles",
            "--full-refresh",
        ],
        env,
    )
    run(["dbt", "build", "--project-dir", "dbt", "--profiles-dir", "profiles"], env)
    run([sys.executable, "scripts/build_dashboard.py"], env)
    print("\nPipeline succeeded. Open site/index.html to inspect the control tower.")


if __name__ == "__main__":
    main()
