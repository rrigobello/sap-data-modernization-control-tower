SELECT
    CAST(source_row_id AS VARCHAR) AS source_row_id,
    CAST(mandt AS VARCHAR) AS client,
    CAST(kokrs AS VARCHAR) AS controlling_area,
    CAST(belnr AS VARCHAR) AS controlling_document,
    CAST(gjahr AS INTEGER) AS fiscal_year,
    CAST(buzei AS VARCHAR) AS line_item,
    CAST(objnr AS VARCHAR) AS object_number,
    CAST(kstar AS VARCHAR) AS cost_element,
    CAST(wrttp AS VARCHAR) AS value_type,
    CAST(wkgbtr AS DECIMAL(18, 2)) AS amount_controlling_area_currency,
    CAST(wrbtr AS DECIMAL(18, 2)) AS amount_transaction_currency,
    NULLIF(CAST(parob AS VARCHAR), '') AS partner_object
FROM {{ ref('coep') }}
