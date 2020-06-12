# Udacity Nanodegree Projects

Projects worked for Udacity Nanodegree Program

## Project descriptions:

### 1 - SQL
Loaded JSON and CSV data into a PostgresSQL Database. Initialized database with certain indexes to optimize performance. Employed Star Schema

### 2 - NoSQL
Loaded JSON and CSV data into a Cassandra NoSQL Database. Formatted data for certain queries

### 03 - Datawarehouse
Loaded JSON and CSV data from an AWS S3 bucket into an AWS Redshift datawarebhouse. Database was initialized with certain indexes for sake of documentation of types of database (but Redshift doesn't enforce indexing). Employed Star Schema

### 04 - Data Lakes with Spark
Used an EMR Cluster to power a ETL from a S3 bucket of Raw files to another S3 bucket. with 'cleaned' CSV files. Implemented Staging and Fact/Dimension Tables (Employed Star Schema)

### 05 - Data Pipelines
Used Apache Airflow to move data from S3 buckets, and transform it into staged and then fact/dimension tables in Redshift. Created custom operators to move data from S3 to staging tables in Redshift, data transformations from staging to fact/dimension tables in Redshift, and Data Quality checks.

### 05 - Capstone
Used data from the Consumer Financial Protection Bureau. In it's on git repo