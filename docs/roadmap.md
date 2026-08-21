# Portfolio roadmap

## Milestone 1 — FI/CO trusted publication

- Synthetic `BKPF`, `BSEG`, `COBK`, and `COEP`
- Row quarantine and document balancing
- FI-to-CO reconciliation
- GitHub CI and static control tower

## Milestone 2 — Incremental ingestion and recovery

- Watermark-based ingestion
- Idempotent merge behavior
- Duplicate delivery handling
- Late-arriving records and backfills
- Pipeline-run audit table

## Milestone 3 — Master-data history

- Customer, vendor, material, and organizational models
- Slowly changing dimensions type 2
- Deleted-record handling
- Referential-integrity quarantine

## Milestone 4 — ECC-to-S/4 modernization

- Simplified Universal Journal target
- `BSEG`/`COEP` to `ACDOCA` mapping concepts
- Source-to-target reconciliation
- Compatibility and semantic change inventory

## Milestone 5 — Snowflake enterprise deployment

- Snowflake dbt target
- Roles, masking, and ownership
- Incremental models and query tuning
- Cost attribution and resource monitors
