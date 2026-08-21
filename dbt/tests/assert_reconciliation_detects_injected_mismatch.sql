SELECT 1 AS failure
WHERE (
    SELECT COUNT(*)
    FROM {{ ref('rpt_fi_co_reconciliation') }}
    WHERE reconciliation_status = 'MISMATCH'
) <> 1
