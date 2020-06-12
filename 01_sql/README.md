# Project: Data Modeling with Postgres

## Introduction
This database is being built for the fake startup Sparkify. The files are raw json files from Sparkify's songs and user activity from their music streaming app.

The goal of this database is to help the analytics team understand what songs users are listening to, as well as perform other relevant analytics for moving forward the application

## Files in Repo
* create_tables.py: Drops all existing tables that are listed in the above "Output database" section. Then it create these tables
* etl.py uses the data that we intend to put in the database: A log of songs played is located in /data/log_data. A list of songs is located in /data/song_data. This takes a combination of the rows in each of these files in order to fill the appropriate tables.
* sql_queries.py: queries run in create_tables.py and etl.py. These queries DROP, CREATE and INSERT data into tables
* data/log_data: log data of what songs users played at certain times
* data/song_data: data of songs in music streaming service
* test.ipynb: a file allowing one to view and test changes made by create_table.py and etl.py
* etl.ipynb: a testing file allowing one to insert data into etl.py. Sets the stage for etl.py

## How to use files
`create_tables.py` and `etl.py` are both run in order to create the relevant tables using strings in `sql_queries.py`. The files are run in the command line using `python [filename]` in the following order:
1. create_tables.py: Drops all existing tables that are listed in the above "Output database" section. Then it create these tables
2. etl.py uses the data that we intend to put in the database: A log of songs played is located in /data/log_data. A list of songs is located in /data/song_data. This takes a combination of the rows in each of these files in order to fill the appropriate tables.


## Output database
A star schema was employed to create dimension tables that track the songs, artists that could be played, users that are apart of the streaming platform, the time of the song plays. The center fact table records what songs were played. 

Here is a break down of tables:

1. songplays - A fact table records in log data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

Dimension tables:
2. users - Users using Sparkify's music streaming app
user_id, first_name, last_name, gender, level
3. songs - songs in music database
song_id, title, artist_id, year, duration
4. artists - artists in music database
artist_id, name, location, latitude, longitude
5. time - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday

## Source Data
### Songs dataset
It's a subset of songs from the http://millionsongdataset.com/. Each song is in a .json file, containing various meta-data descriptors about the song including artist_id, artist_name, title, duration, year

The files for each song are stored in numerous directories in data/song_data. To load and access all the songs, one needs to traverse through the folders containing songs recursively.

### Logs
The logs are events from a music streaming app where users can listen to the songs in the songs dataset.

The log files are partitioned by year and month




## Examples with database
The sparkify database is a postgres database. These are a few examples of possible queries:

1. Select count all the users that are paid
```sql
select COUNT(*) from users where level = 'paid'
```
output:
```
5569
```

2. Select unique list of artists
```sql
select distinct name from artists
```

output:
```
name
Willie Bobo
The Box Tops
Jeff And Sheri Easter
King Curtis
Jimmy Wakely
```