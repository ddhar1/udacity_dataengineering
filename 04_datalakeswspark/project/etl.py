import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import udf, col, row_number, year, month, dayofmonth, hour, weekofyear, date_format


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['aws']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['aws']['AWS_SECRET_ACCESS_KEY']

def create_spark_session():
    """Starts session of spark
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.5") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """ Processes all song_data json files.
        Output is a parquet file loaded into an amazon s3 bucket
    """
    # get filepath to song data file
    print("Reading in song_data...")
    song_data = input_data + "song_data/*/*/*/*.json"

    # read song data file
    df = spark.read.json(song_data)
    print("Finished reading song_data")
    
    print("Creating songs table")
    # extract columns to create songs table
    songs_table =  df['song_id', 'title', 'artist_id', 'year', 'duration']
    songs_table = songs_table.dropDuplicates(['song_id'])
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy('year', 'artist_id').parquet(os.path.join(output_data, 'songs.parquet'), 'overwrite')
    print("Finished writing songs table")

    
    print("Extracting data for artist table")
    # extract columns to create artists table
    artists_table = df['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']
    artists_table = artists_table.dropDuplicates(['artist_id'])

    # write artists table to parquet files
    artists_table.write.parquet(os.path.join(output_data, 'artists/artists.parquet'), 'overwrite')
    print("Finished writing artists table")


def process_log_data(spark, input_data, output_data):
    """Loads all log data json files from an s3 bucket
        Output is a parquet file
    """
    print("Reading log_data")
    # get filepath to log data file
    log_data = input_data + "log_data/*/*/*.json"

    # read log data file
    df = spark.read.json(log_data)
    print("log_data loaded")
    
    # filter by actions for song plays
    df = df[df.page == "NextSong"]
    
    # extract columns for users table    
    users_table = df['userId', 'firstName', 'lastName', 'gender', 'level']
    users_table = users_table.dropDuplicates(['userId'])
        
    # write users table to parquet files
    users_table.write.parquet(os.path.join(output_data, 'users.parquet'), 'overwrite')
    print("Users table parquet file created")

    print("Performing feature engineering for time table")
    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: str( int ( int( x ) / 1000 ) ) )
    df = df.withColumn('timestamp', get_timestamp(df.ts))
    
    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: str(datetime.fromtimestamp(int(x) / 1000.0)))
    df = df.withColumn("datetime", get_datetime(df.ts))
    
    # extract columns to create time table
    time_table = df.dropDuplicates(['datetime'])    

    time_table = time_table.select(
        col('datetime').alias('start_time'),
        hour('datetime').alias('hour'),
        dayofmonth('datetime').alias('day'),
        weekofyear('datetime').alias('week'),
        month('datetime').alias('month'),
        year('datetime').alias('year') 
    )
    
    # write time table to parquet files partitioned by year and month
    time_table.write.parquet(os.path.join(output_data, 'time.parquet'), 'overwrite')
    print("time table parquet file written to s3 bucket")

    print("Reading in song_data, to merge with log_data in order to create songplay table")
    # read in song data to use for songplays table
    song_df = spark.read.json(input_data + 'song_data/*/*/*/*.json')
    
    print("Feature engineering for songplays table")
    songplays = df.select('datetime', 'userId', 'level', 'song', 'artist', 'sessionId', 'location', 'userAgent')

    print("joining songplays_table and song_data table")
    # extract columns from joined song and log datasets to create songplays table 
    songplays_table =  songplays.join(song_df, (song_df.title == songplays.song) & (song_df.artist_name == songplays.artist) )
    
    # create songplay_id column
    songplays_table = songplays_table.withColumn("songplay_id", row_number().over( Window.orderBy("datetime") ))
    
    #select columns to go into final table
    songplays_table = songplays_table.select( "songplay_id", col('datetime').alias('start_time'), "userId", "level", "song_id", 'artist_id', 'sessionId', 'location', 'userAgent', year('datetime').alias('year'), month('datetime').alias('month')   )
    
    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy('year', 'month').parquet(os.path.join(output_data, 'songplays.parquet'), 'overwrite')
    print("songplays table parquet file written to s3 bucket")


def main():
    """Create spark session
        Process song_data and log_data and write it to songplays, time, users, artists, songs parquet files in own s3 Bucket
    """
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://udacity-4datalake/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
