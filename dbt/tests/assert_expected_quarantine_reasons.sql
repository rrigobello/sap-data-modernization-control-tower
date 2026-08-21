WITH expected_reasons(reason) AS (
    VALUES
        ('DUPLICATE_LINE'),
        ('MISSING_HEADER'),
        ('MISSING_EXCHANGE_RATE'),
        ('UNBALANCED_DOCUMENT')
),

observed_reasons AS (
    SELECT DISTINCT quarantine_reason AS reason
    FROM {{ ref('quarantine_fi_line_items') }}
)

SELECT expected.reason
FROM expected_reasons AS expected
LEFT JOIN observed_reasons AS observed
    ON expected.reason = observed.reason
WHERE observed.reason IS NULL
