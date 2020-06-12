# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS SONGPLAYS"
user_table_drop = "DROP TABLE IF EXISTS USERS"
song_table_drop = "DROP TABLE IF EXISTS SONGS"
artist_table_drop = "DROP TABLE IF EXISTS ARTISTS"
time_table_drop = "DROP TABLE IF EXISTS TIME"

# CREATE TABLES
user_table_create = ("""
CREATE TABLE IF NOT EXISTS users  (user_id int PRIMARY KEY, first_name varchar, last_name varchar, gender char(1), level varchar NOT NULL);
""")


song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (song_id varchar  PRIMARY KEY, title varchar, artist_id varchar, year int, duration decimal);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (artist_id varchar PRIMARY KEY, name varchar, location varchar, latitude decimal, longitude decimal);

""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (start_time timestamp PRIMARY KEY, hour int  NOT NULL, day int NOT NULL, week int NOT NULL, month int NOT NULL, year int NOT NULL, weekday int NOT NULL);
""")


songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (songplay_id SERIAL PRIMARY KEY, start_time timestamp NOT NULL, user_id int references users, level varchar NOT NULL, song_id varchar references songs, artist_id varchar references artists, session_id int NOT NULL, location varchar, user_agent varchar);
""")


# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays ( start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)  VALUES ( %s, %s,%s, %s, %s,%s, %s, %s)
""")

user_table_insert = ("""
INSERT INTO users  (user_id, first_name, last_name, gender, level)  VALUES (%s, %s, %s,%s, %s)
    ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level;
""")

song_table_insert = ("""
INSERT INTO songs  (song_id, title, artist_id, year , duration) VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (song_id) DO NOTHING;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude) VALUES  (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id) DO NOTHING;
""")


time_table_insert = ("""
INSERT INTO  time (start_time, hour, day, week, month, year, weekday)  VALUES  (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time) DO NOTHING;
""")

# FIND SONGS

song_select = ("""
select song_id, a.artist_id from songs s
join artists a on s.artist_id = a.artist_id
where s.title = %s and a.name = %s and s.duration = %s
""")

# QUERY LISTS 
# Will be imported into etl.py and create_tables.py
create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]