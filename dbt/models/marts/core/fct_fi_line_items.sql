SELECT
    line.source_row_id,
    line.client,
    line.company_code,
    line.accounting_document,
    line.fiscal_year,
    line.line_item,
    line.document_type,
    line.posting_date,
    line.document_currency,
    line.gl_account,
    account.account_name,
    account.account_category,
    line.debit_credit_indicator,
    line.amount_local_currency,
    line.amount_document_currency,
    line.signed_local_amount,
    line.cost_center,
    line.internal_order,
    line.line_item_text
FROM {{ ref('int_fi_lines_classified') }} AS line
INNER JOIN {{ ref('int_fi_document_balance') }} AS balance
    ON line.client = balance.client
    AND line.company_code = balance.company_code
    AND line.accounting_document = balance.accounting_document
    AND line.fiscal_year = balance.fiscal_year
LEFT JOIN {{ ref('stg_gl_accounts') }} AS account
    ON line.gl_account = account.gl_account
WHERE line.row_quality_status = 'PASS'
    AND balance.document_balance_status = 'PASS'
