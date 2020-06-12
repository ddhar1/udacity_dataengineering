import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries

    
def drop_tables(cur, conn):
    """Drops all tables in cluster - events_stage, songs_stage songplays, songs, artists, users, time
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """ Creates all database in cluster -  events_stage, songs_stage songplays, songs, artists, users, time
    """
    for query in create_table_queries:
        print(query)
        cur.execute(query)
        conn.commit()


def main():
    """Connects to Redshift database. Resets all the tables in the redshift cluster
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()