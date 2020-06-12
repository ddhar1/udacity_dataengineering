from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


insert_query =  """
                INSERT INTO {} 
                ({});               
                """

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 redshift_conn_id="",
                 target_table = "",
                 sql = "",
                 append = True,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        self.redshift_conn_id = redshift_conn_id
        self.target_table = target_table
        self.sql = sql
        self.append = append


    def execute(self, context):
        self.log.info('Connecting to redshift database')
        # connect to redsfhit
        redshift = PostgresHook(postgres_conn_id = self.redshift_conn_id)
        self.log.info('Connected to redshift database')
        
        # If user doesn't want you to append, truncate the table before inserting data
        if self.append == False:
                self.log.info( 'Append is set to False so Truncating {} table in redshift'.format(self.target_table) )
                redshift.run("TRUNCATE TABLE {}".format(self.target_table) )
                
        # Insert data by running SQL query into target_table 
        self.log.info( 'Inserting data into {} table in redshift'.format(self.target_table) )
        redshift.run( insert_query.format(self.target_table, self.sql) )
        self.log.info("Success: {} dimension table loaded".format(self.target_table))
