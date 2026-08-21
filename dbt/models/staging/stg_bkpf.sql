SELECT
    CAST(mandt AS VARCHAR) AS client,
    CAST(bukrs AS VARCHAR) AS company_code,
    CAST(belnr AS VARCHAR) AS accounting_document,
    CAST(gjahr AS INTEGER) AS fiscal_year,
    CAST(blart AS VARCHAR) AS document_type,
    CAST(budat AS DATE) AS posting_date,
    CAST(waers AS VARCHAR) AS document_currency,
    CAST(cpudt AS DATE) AS entry_date,
    CAST(cputm AS VARCHAR) AS entry_time
FROM {{ ref('bkpf') }}
