WITH fi AS (
    SELECT
        company_code,
        accounting_document,
        fiscal_year,
        SUM(signed_local_amount) AS fi_expense_amount
    FROM {{ ref('fct_fi_line_items') }}
    WHERE account_category = 'EXPENSE'
    GROUP BY company_code, accounting_document, fiscal_year
),

co AS (
    SELECT
        company_code,
        reference_fi_document AS accounting_document,
        reference_fiscal_year AS fiscal_year,
        SUM(amount_controlling_area_currency) AS co_primary_cost_amount
    FROM {{ ref('fct_co_line_items') }}
    WHERE value_type = '04'
    GROUP BY company_code, reference_fi_document, reference_fiscal_year
),

reconciled AS (
    SELECT
        COALESCE(fi.company_code, co.company_code) AS company_code,
        COALESCE(fi.accounting_document, co.accounting_document) AS accounting_document,
        COALESCE(fi.fiscal_year, co.fiscal_year) AS fiscal_year,
        fi.fi_expense_amount,
        co.co_primary_cost_amount,
        COALESCE(fi.fi_expense_amount, 0) - COALESCE(co.co_primary_cost_amount, 0)
            AS difference_amount
    FROM fi
    FULL OUTER JOIN co
        ON fi.company_code = co.company_code
        AND fi.accounting_document = co.accounting_document
        AND fi.fiscal_year = co.fiscal_year
)

SELECT
    *,
    CASE
        WHEN fi_expense_amount IS NULL THEN 'MISSING_FI'
        WHEN co_primary_cost_amount IS NULL THEN 'MISSING_CO'
        WHEN ABS(difference_amount) <= 0.01 THEN 'MATCH'
        ELSE 'MISMATCH'
    END AS reconciliation_status
FROM reconciled
