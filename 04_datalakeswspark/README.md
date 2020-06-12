# Data Lake in S3 with Spark

## Introduction
Sparkify, a music streaming company wants to create a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## How project works
This ETL pipeline that extracts the raw Sparikfy data from an S3 bucket, processes and transforms this data into sensible analytical tables using Spark (and an Amazon EMR Cluster in order to speed up the process of processing the data). The transformed data is then loaded into a seperate S3 Bucket.

## Files and how to use them
The files in this project include:
* `etl.py` reads data from S3, processes that data using Spark, and writes them back to S3
* `dl.cfg`: contains your AWS credentials

To get this project to run, input the credentials of an IAM role that has S3 access, and run etl.py in command line

## Data

The output data is as follows:

Fact Table
* songplays - records in log data associated with song plays i.e. records with page NextSong:
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