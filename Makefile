.PHONY: setup generate seed build test dashboard pipeline clean

setup:
	python -m pip install -r requirements.txt

generate:
	python scripts/generate_sap_data.py --documents 50

seed:
	dbt seed --project-dir dbt --profiles-dir profiles --full-refresh

build:
	dbt build --project-dir dbt --profiles-dir profiles

test:
	pytest
	dbt test --project-dir dbt --profiles-dir profiles

dashboard:
	python scripts/build_dashboard.py

pipeline:
	python scripts/run_pipeline.py --documents 50

clean:
	dbt clean --project-dir dbt --profiles-dir profiles
	python scripts/clean_generated.py
