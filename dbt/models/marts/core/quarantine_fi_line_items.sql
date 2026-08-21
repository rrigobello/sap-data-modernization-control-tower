SELECT
    line.source_row_id,
    line.client,
    line.company_code,
    line.accounting_document,
    line.fiscal_year,
    line.line_item,
    line.gl_account,
    line.amount_local_currency,
    line.debit_credit_indicator,
    line.posting_date,
    line.document_currency,
    COALESCE(
        line.row_quarantine_reason,
        CASE
            WHEN balance.document_balance_status = 'FAIL' THEN 'UNBALANCED_DOCUMENT'
        END
    ) AS quarantine_reason
FROM {{ ref('int_fi_lines_classified') }} AS line
LEFT JOIN {{ ref('int_fi_document_balance') }} AS balance
    ON line.client = balance.client
    AND line.company_code = balance.company_code
    AND line.accounting_document = balance.accounting_document
    AND line.fiscal_year = balance.fiscal_year
WHERE line.row_quality_status = 'QUARANTINE'
    OR balance.document_balance_status = 'FAIL'
