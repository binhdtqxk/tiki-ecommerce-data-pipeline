use database tiki_db;
use schema staging;
COPY INTO Tiki_Products_Raw (
    product_id, name, brand_name, price, discount, discount_rate,
    rating_average, review_count, quantity_sold, original_price,
    category_id, category_name, source_file_name, crawled_date
)
FROM (
    SELECT 
        $1, $2, $3, $4, $5, $6, 
        $7, $8, $9, $10, $11, $12,
        METADATA$FILENAME, to_date(regexp_substr(METADATA$FILENAME, '\\d{8}'), 'YYYYMMDD')
    FROM @STAGING.my_s3_tiki_stage
)
FILE_FORMAT = (
    TYPE = 'CSV' 
    FIELD_DELIMITER = ',' 
    SKIP_HEADER = 1 
    FIELD_OPTIONALLY_ENCLOSED_BY = '"' 
    NULL_IF = ('') 
);