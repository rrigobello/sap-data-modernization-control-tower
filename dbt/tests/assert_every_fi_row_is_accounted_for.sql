WITH memberships AS (
    SELECT
        source.source_row_id,
        CASE WHEN published.source_row_id IS NOT NULL THEN 1 ELSE 0 END
            + CASE WHEN quarantined.source_row_id IS NOT NULL THEN 1 ELSE 0 END AS membership_count
    FROM {{ ref('stg_bseg') }} AS source
    LEFT JOIN {{ ref('fct_fi_line_items') }} AS published
        ON source.source_row_id = published.source_row_id
    LEFT JOIN {{ ref('quarantine_fi_line_items') }} AS quarantined
        ON source.source_row_id = quarantined.source_row_id
)

SELECT *
FROM memberships
WHERE membership_count <> 1
