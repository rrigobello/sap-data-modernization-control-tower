SELECT
    client,
    company_code,
    accounting_document,
    fiscal_year,
    COUNT(*) AS candidate_line_count,
    SUM(signed_local_amount) AS balance_local_currency,
    CASE
        WHEN ABS(SUM(signed_local_amount)) <= 0.01 THEN 'PASS'
        ELSE 'FAIL'
    END AS document_balance_status
FROM {{ ref('int_fi_lines_classified') }}
WHERE row_quality_status = 'PASS'
GROUP BY
    client,
    company_code,
    accounting_document,
    fiscal_year
