SELECT
    client,
    company_code,
    accounting_document,
    fiscal_year,
    SUM(signed_local_amount) AS balance
FROM {{ ref('fct_fi_line_items') }}
GROUP BY client, company_code, accounting_document, fiscal_year
HAVING ABS(SUM(signed_local_amount)) > 0.01
