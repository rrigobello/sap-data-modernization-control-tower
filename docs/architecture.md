# Architecture and design decisions

## Business problem

An ECC-to-cloud migration can reproduce source records successfully while still
publishing financially incorrect data. The control tower treats financial
reconciliation and source-data quality as release controls, not dashboard-only
checks performed after publication.

## Publication flow

1. Raw SAP-style extracts are loaded without correction.
2. Staging models normalize names and types while preserving source identifiers.
3. Row-level checks identify duplicates, missing headers, missing amounts, and
   unavailable currency conversions.
4. Candidate documents are tested for debit/credit balance.
5. Only valid rows from balanced documents enter the trusted FI fact.
6. Rejected records enter a quarantine fact with actionable reason codes.
7. Trusted FI expenses are reconciled with CO primary costs.
8. Control metrics and exceptions are published to a static dashboard.

## Why quarantine instead of failing the entire load?

Corporate source systems often deliver a small number of problematic records
inside a much larger valid batch. Quarantine preserves availability for healthy
data while explicitly preventing defective records from reaching consumers.
The CI tests still fail if any source row disappears from both the trusted and
quarantine outputs, or appears in both.

## Idempotency

The synthetic generator is deterministic for a given document count and random
seed. `dbt seed --full-refresh` and table materializations produce the same state
when rerun. Incremental watermarking and late-arriving records will be added in
the next milestone.

## Snowflake migration boundary

The source, staging, validation, fact, and reporting layers are separate dbt
relations. Migrating from DuckDB to Snowflake will require a second dbt target
and warehouse-specific operational configuration, while preserving the business
controls and most transformation SQL.
