## Checks whether input table is null or has 0 records
## if it has 0 records, it's likely that something went wrong. Particulary if it's a fact table
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 redshift_conn_id="",
                 tables=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        # Map params here
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables

    def execute(self, context):
        self.log.info( 'Connecting to redshift database' )
        redshift = PostgresHook(postgres_conn_id = self.redshift_conn_id)
        self.log.info( 'Connected to redshift database' )

        for table in self.tables:
            self.log.info( 'Checking number of records in table {}'.format(table) )
            records = redshift.get_records("SELECT COUNT(*) FROM \"{}\";".format(table)) # quotations to ensure it's looking at a table
            if records is None or len(records[0]) < 1:
                logging.error(f"No records present in destination table {table}")
                raise ValueError(f"No records present in destination table {table}")
            else:
                self.log.info( 'Table {} has more than 1 record'.format(table) )
