SELECT
    CAST(hkont AS VARCHAR) AS gl_account,
    CAST(account_name AS VARCHAR) AS account_name,
    CAST(account_category AS VARCHAR) AS account_category
FROM {{ ref('gl_accounts') }}
