use database tiki_db;
use schema staging;
create or replace table Tiki_Products_Raw (
    product_id string,
    name string,
    brand_name string,
    price float,
    discount float,
    discount_rate float,
    rating_average float,
    review_count integer,
    quantity_sold integer,
    original_price float,
    category_id string,
    category_name string,
    
    -- 2 Metadata columns take from file name
    source_file_name string,
    ingested_at TIMESTAMP
)
