SELECT
    line.source_row_id,
    line.client,
    line.controlling_area,
    header.company_code,
    line.controlling_document,
    line.fiscal_year,
    line.line_item,
    header.business_transaction,
    header.posting_date,
    line.object_number,
    line.cost_element,
    line.value_type,
    line.amount_controlling_area_currency,
    line.amount_transaction_currency,
    line.partner_object,
    header.reference_fi_document,
    header.reference_fiscal_year
FROM {{ ref('stg_coep') }} AS line
INNER JOIN {{ ref('stg_cobk') }} AS header
    ON line.client = header.client
    AND line.controlling_area = header.controlling_area
    AND line.controlling_document = header.controlling_document
    AND line.fiscal_year = header.fiscal_year
