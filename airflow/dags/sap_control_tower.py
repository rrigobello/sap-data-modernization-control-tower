"""Reference Airflow DAG for the SAP modernization control-tower pipeline."""

from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_ROOT = "/opt/airflow/project"

with DAG(
    dag_id="sap_data_modernization_control_tower",
    description="Generate, validate, reconcile, and publish synthetic SAP FI/CO data.",
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    default_args={
        "owner": "data-platform",
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["sap", "fi-co", "data-quality", "portfolio"],
) as dag:
    generate_extract = BashOperator(
        task_id="generate_synthetic_sap_extract",
        bash_command=f"cd {PROJECT_ROOT} && python scripts/generate_sap_data.py --documents 1000",
    )

    load_seeds = BashOperator(
        task_id="load_raw_extracts",
        bash_command=(
            f"cd {PROJECT_ROOT} && dbt seed --project-dir dbt "
            "--profiles-dir profiles --full-refresh"
        ),
    )

    build_and_test = BashOperator(
        task_id="build_and_test_trusted_models",
        bash_command=f"cd {PROJECT_ROOT} && dbt build --project-dir dbt --profiles-dir profiles",
    )

    publish_control_tower = BashOperator(
        task_id="publish_static_control_tower",
        bash_command=f"cd {PROJECT_ROOT} && python scripts/build_dashboard.py",
    )

    generate_extract >> load_seeds >> build_and_test >> publish_control_tower
