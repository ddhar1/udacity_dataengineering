# Data Pipelines with Airflow

## About Project

In this Udacity project, we were asked to see how we can use **Airflow** to create a data pipeline that pulled data from an S3 bucket, cleaned this data and put it into a database on a Redshift cluster

The company use case in this project was to shift log files, or history of what music people played on their online streaming app, and song files, or a list of what types of songs people can play possibly

## Contents
This project contains
* dags/logandsongs_s3_to_redshift.py: a dag that connects operators that take a csv of logs from s3, and json of song files from s3, puts these files in a staging table, and manipulates them to store into a csv file
* plugins/operators/stage_redshift.py: for a given target table, source s3 bucket, and input file format (CSV or JSON), you can stage a redshift table
* plugins/operators/load_fact.py: load the fact table that was apart of this exercise: the log data file
* plugins/operators/load_dimension.py: load the dimension tables in question for this file, 
* plugins/operators/data_quality.py: Checks whether the inputted array of tables  actually have data.
* plugins/helpers/sql_queries.py: actually checks whether or not that 


## How to use
In order to run this project. You first need to make sure that airflow is installed, either through installing via pip, or through a docker image
1. Run create_tables.sql in the target database/schema in redshift. In this file **all target tables, for both stage and final tables is in the public schema** and you must change this 
2. Add two connectiosn in Airflow
	* redshift: this will connect to the target database in redshift in order to uploade data from s3 to redshift, as well as manipulate data in redshift
	* aws_credentials: IAM credentials that allow one to connect to the s3 buckets containing the log and song data
2. Fill out the appropriate source s3 buckets and keys in the s3 bucket for song data and log data
3. Fix the dag's schedule based on the source and target data's timelines and turn on the dag in the airflow UIyou

