from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 redshift_conn_id="",
                 target_table = "",
                 truncate = False,
                 sql="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        # Map params here
        self.redshift_conn_id = redshift_conn_id
        self.target_table = target_table
        self.truncate = truncate
        self.sql = sql

    def execute(self, context):
        self.log.info('Connecting to redshift database')
        # connect to redshift
        redshift = PostgresHook(postgres_conn_id = self.redshift_conn_id)
        self.log.info('Connected to redshift database')
        
        # truncate destination table
        if self.truncate:
                self.log.info( 'Truncate is set to true; Truncating {} table in redshift'.format() )
                redshift.run("TRUNCATE TABLE {}".format(self.target_table) )
                
        # Insert data by running SQL query into target_table 
        self.log.info( 'Inserting data into {} table in redshift'.format(self.target_table) )
        redshift.run( self.sql )
        self.log.info("Success: {} fact table loaded".format(self.target_table))


        #redshift.get_record(")".format(self.target_table)