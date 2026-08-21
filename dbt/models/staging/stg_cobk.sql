SELECT
    CAST(mandt AS VARCHAR) AS client,
    CAST(kokrs AS VARCHAR) AS controlling_area,
    CAST(bukrs AS VARCHAR) AS company_code,
    CAST(belnr AS VARCHAR) AS controlling_document,
    CAST(gjahr AS INTEGER) AS fiscal_year,
    CAST(vrgng AS VARCHAR) AS business_transaction,
    CAST(budat AS DATE) AS posting_date,
    CAST(waers AS VARCHAR) AS controlling_area_currency,
    CAST(refbn AS VARCHAR) AS reference_fi_document,
    CAST(refgj AS INTEGER) AS reference_fiscal_year
FROM {{ ref('cobk') }}
