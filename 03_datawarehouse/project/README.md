# Data Warehouse from a data in S3

## Use Case
Sparkify is a music streaming startup. Their data, songs that one can play, and log files, which contain data with information on what songs users played, resides in S3 in a json format


The goal of this exercise is to create ETL pipeline that:
1. extracts the data from S3 from the json format to a regular dataframe format
2. stages them in Redshift
3. transforms data into a set of star schema that can allow for one to perform business analytics on

## Contents
This folder contains:
* `create_table.py` is where you'll create your fact and dimension tables for the star schema in Redshift.
* `etl.py` loads data from S3 into staging tables on Redshift. It then processes data from staging table to an analytics table in Redshift
* `sql_queries.py`: Queries run by `create_table.py` and `etl.py` that creates tables, loads data from s3 and places them in tables in redshift, and inserts data from transformed stage tables into tables used for analytics
* `dwg.cfg` is read into `create_table.py`, `etl.py` and `sql_queries.py` to access Amazon Redshift database and to allow one to use a IAM role and read the S3 buckets.

### How to run ELT program
1. In `dwh.cfg`, input redshift host and database information under `[CLUSTER]`, aws credentials under `[IAM_ROLE]` and `[AWS]` (create an IAM role and user that has full access to a Redshift Cluster and read access to S3 Buckets)
2. Run `create_tables.py` and then `etl.py` in command line, with python

## Data

Fact table:
* songplays - records in event data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

Dimension Tables
* users - users in the app
user_id, first_name, last_name, gender, level
* songs - songs in music database
song_id, title, artist_id, year, duration
* artists - artists in music database
artist_id, name, location, lattitude, longitude
* time - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday