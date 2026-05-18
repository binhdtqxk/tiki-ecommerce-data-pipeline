create database if not exists tiki_db;
use database tiki_db;

--Create staging (contain raw data from asw s3)
create schema if not exists staging;

--Create warehouse (contain dim and fact table)
create schema if not exists core;

--Create staging that point to asw s3 bucket
use schema staging;
create or replace stage my_s3_tiki_stage
url='s3://binh-tiki-data-pipeline-646984527458-ap-southeast-1-an/raw_data/tiki/'
STORAGE_INTEGRATION = s3_tiki_integration;