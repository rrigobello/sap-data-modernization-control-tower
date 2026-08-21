SELECT
    CAST(source_row_id AS VARCHAR) AS source_row_id,
    CAST(mandt AS VARCHAR) AS client,
    CAST(bukrs AS VARCHAR) AS company_code,
    CAST(belnr AS VARCHAR) AS accounting_document,
    CAST(gjahr AS INTEGER) AS fiscal_year,
    CAST(buzei AS VARCHAR) AS line_item,
    CAST(hkont AS VARCHAR) AS gl_account,
    CAST(shkzg AS VARCHAR) AS debit_credit_indicator,
    CAST(dmbtr AS DECIMAL(18, 2)) AS amount_local_currency,
    CAST(wrbtr AS DECIMAL(18, 2)) AS amount_document_currency,
    NULLIF(CAST(kostl AS VARCHAR), '') AS cost_center,
    NULLIF(CAST(aufnr AS VARCHAR), '') AS internal_order,
    CAST(sgtxt AS VARCHAR) AS line_item_text,
    ROW_NUMBER() OVER (
        PARTITION BY mandt, bukrs, belnr, gjahr, buzei
        ORDER BY source_row_id
    ) AS duplicate_rank
FROM {{ ref('bseg') }}
