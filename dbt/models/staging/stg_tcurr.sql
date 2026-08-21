SELECT
    CAST(from_currency AS VARCHAR) AS from_currency,
    CAST(to_currency AS VARCHAR) AS to_currency,
    CAST(valid_from AS DATE) AS valid_from,
    CAST(valid_to AS DATE) AS valid_to,
    CAST(rate AS DECIMAL(18, 6)) AS exchange_rate
FROM {{ ref('tcurr') }}
