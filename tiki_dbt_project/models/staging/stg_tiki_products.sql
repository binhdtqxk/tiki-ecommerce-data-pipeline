with raw_data as (
    select * from {{ source('snowflake_raw_source', 'TIKI_PRODUCTS_RAW') }}
    
    qualify row_number() over (
        partition by product_id, crawled_date 
        order by crawled_date desc
    ) = 1
)
select
    cast(product_id as varchar) as product_id,
    
    cast(coalesce(nullif(trim(name), ''), 'Unknown Product') as varchar) as product_name,
    
    cast(coalesce(nullif(trim(brand_name), ''), 'Unknown Brand') as varchar) as brand_name,
     
    cast(coalesce(nullif(trim(category_id), ''), '-1') as varchar) as category_id,
    
    cast(coalesce(nullif(trim(category_name), ''), 'Unknown Category') as varchar) as category_name,

    cast(coalesce(price, 0) as int) as price,
    cast(coalesce(original_price, 0) as int) as original_price,
    cast(coalesce(discount, 0) as int) as discount_amount,
    cast(coalesce(discount_rate, 0) as int) as discount_rate,
    cast(coalesce(rating_average, 0.0) as float) as rating_average,
    cast(coalesce(review_count, 0) as int) as review_count,
    cast(coalesce(quantity_sold, 0) as int) as quantity_sold,
   
    cast(crawled_date as date) as crawled_date,

    cast(source_file_name as varchar) as etl_source_file

from raw_data