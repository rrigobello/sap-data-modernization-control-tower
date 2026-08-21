SELECT 'Raw FI lines' AS metric, COUNT(*) AS metric_value
FROM {{ ref('stg_bseg') }}

UNION ALL

SELECT 'Published FI lines', COUNT(*)
FROM {{ ref('fct_fi_line_items') }}

UNION ALL

SELECT 'Quarantined FI lines', COUNT(*)
FROM {{ ref('quarantine_fi_line_items') }}

UNION ALL

SELECT 'Balanced FI documents', COUNT(DISTINCT accounting_document)
FROM {{ ref('fct_fi_line_items') }}

UNION ALL

SELECT 'FI-CO matches', COUNT(*)
FROM {{ ref('rpt_fi_co_reconciliation') }}
WHERE reconciliation_status = 'MATCH'

UNION ALL

SELECT 'FI-CO exceptions', COUNT(*)
FROM {{ ref('rpt_fi_co_reconciliation') }}
WHERE reconciliation_status <> 'MATCH'
