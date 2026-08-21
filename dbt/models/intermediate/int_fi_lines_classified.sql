WITH classified AS (
    SELECT
        line.*,
        header.document_type,
        header.posting_date,
        header.document_currency,
        fx.exchange_rate,
        CASE
            WHEN header.accounting_document IS NULL THEN 'MISSING_HEADER'
            WHEN line.duplicate_rank > 1 THEN 'DUPLICATE_LINE'
            WHEN line.amount_local_currency IS NULL
                OR line.amount_document_currency IS NULL
                THEN 'MISSING_AMOUNT'
            WHEN header.document_currency <> 'USD'
                AND fx.exchange_rate IS NULL
                THEN 'MISSING_EXCHANGE_RATE'
        END AS row_quarantine_reason
    FROM {{ ref('stg_bseg') }} AS line
    LEFT JOIN {{ ref('stg_bkpf') }} AS header
        ON line.client = header.client
        AND line.company_code = header.company_code
        AND line.accounting_document = header.accounting_document
        AND line.fiscal_year = header.fiscal_year
    LEFT JOIN {{ ref('stg_tcurr') }} AS fx
        ON header.document_currency = fx.from_currency
        AND fx.to_currency = 'USD'
        AND header.posting_date BETWEEN fx.valid_from AND fx.valid_to
)

SELECT
    *,
    CASE
        WHEN debit_credit_indicator = 'S' THEN amount_local_currency
        WHEN debit_credit_indicator = 'H' THEN -amount_local_currency
    END AS signed_local_amount,
    CASE
        WHEN row_quarantine_reason IS NULL THEN 'PASS'
        ELSE 'QUARANTINE'
    END AS row_quality_status
FROM classified
