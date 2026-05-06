import requests
import pandas as pd
import time
import random
from datetime import datetime
import os
import boto3
from dotenv import load_dotenv

# 1. Declare header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 OPR/130.0.0.0',
    'Accept': 'application/json, text/plain, */*'
}
# 2. Create list of category
categories=[
    {'id':'1846','name':'Laptop_May_vi_tinh_Linh_kien'},
    {'id':'1789','name':'Dien_thoai_May_tinh_bang'},
    {'id':'1815','name':'thiet_bi_kts_phu_kien_so'},
]
# 3. Create list
product_data = []

# 3. Create loop to crawl from multiple categories
for cat in categories:
    cat_id=cat['id']
    cat_name=cat['name']
    print(f"Start crawl category: {cat_name} \n---")

    #4. Create loop to crawl through product's pages
    for page in range(1,21):
        print(f"Start crawl from page: {page}...")

        #API Url
        url = f"https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&sort=top_seller&page={page}&category={cat_id}"

        response=requests.get(url, headers=headers)

        if response.status_code==200 :
            json_data=response.json()
            items=json_data.get('data',[])

            if not items:
                break
            for item in items:
                product_data.append({
                    'product_id':item.get('id'),
                    'name':item.get('name'),
                    'brand_name':item.get('brand_name'),
                    'price':item.get('price'),
                    'discount':item.get('discount'),
                    'discount_rate':item.get('discount_rate'),
                    'rating_average':item.get('rating_average'),
                    'review_count':item.get('review_count'),
                    # Handle nested object
                    'quantity_sold':(item.get('quantity_sold') or {}).get('value', 0),
                    'original_price':item.get('original_price'),
                    'category_id': cat_id,
                    'category_name': cat_name
                })
        time.sleep(random.uniform(1, 3))

# 4. Turn list to Dataframe and export to csv file(staging)
#Create datetime for the file
current_date = datetime.now().strftime("%Y%m%d")
#Create file name based on datetime
file_name= f'tiki_raw_products_{current_date}.csv'
df = pd.DataFrame(product_data)
df.to_csv(f'data/raw/{file_name}', index=False, encoding='utf-8-sig')
print(f"Crawl finish! Crawled {len(df)} product. Saved in {file_name}")

# --- UPLOAD RAW DATA TO AWS S3 ---

# 1. Load env variables from .env file.
load_dotenv()

AWS_ACCESS_KEY_ID= os.getenv(AWS_ACCESS_KEY_ID)
AWS_SECRET_ACCESS_KEY=os.getenv(AWS_SECRET_ACCESS_KEY)
AWS_REGION=os.getenv(AWS_REGION)
S3_BUCKET_NAME=os.getenv(S3_BUCKET_NAME)

#2. Declare S3 client

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

#3. Declare local & cloud file path
local_file_path= f'data/raw/{file_name}'
s3_file_key= f'raw_data/tiki/{file_name}'

#4. Upload
try:
    print(f'Uploading csv file {file_name} to AWS S3...')
    s3_client.upload_file(local_file_path, S3_BUCKET_NAME, s3_file_key)
    print(f'Uploaded successfully! Data now arrived at S3: s3://{S3_BUCKET_NAME}/{s3_file_key}')
except Exception as e:
    print(f'Uploaded unsuccessfully! Error: {e}')