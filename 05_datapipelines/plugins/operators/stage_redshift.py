from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.S3_hook import S3Hook

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    
    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        {}
        ;
    """
    
    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 redshift_conn_id="",
                 target_table = "",
                 aws_credentials_id="",
                 s3_bucket="",
                 s3_key="temp",
                 file_format = "CSV",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        # Map params here
        self.aws_credentials_id = aws_credentials_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.target_table = target_table
        self.redshift_conn_id = redshift_conn_id
        self.file_format = file_format
        
    def execute(self, context):
        self.log.info("Connecting to s3")
        #aws_hook = AwsHook(self.aws_credentials_id)
        #credentials = aws_hook.get_credentials()\
        
        self.s3 = S3Hook(aws_conn_id=self.aws_credentials_id , verify=False)
        credentials = self.s3.get_credentials()
        self.log.info("Connected to s3")
        self.log.info("Connecting to redshift database")
        redshift = PostgresHook(postgres_conn_id = self.redshift_conn_id)
        self.log.info("Connected to redshift database")
        self.log.info("Clearing data from destination redshift table")
        redshift.run("DELETE FROM {}".format(self.target_table))
                     
        self.log.info("Using file_format parameter to import data correctly from S3 Bucket")             
        if self.file_format == 'CSV':
            sql_formatter = "CSV DELIMITER \',\' IGNOREHEADER 1"
        else:
            sql_formatter = "FORMAT AS JSON \'auto\'"
        self.log.info("Connect to s3 bucket")
        s3_path = "s3://{}/{}".format(self.s3_bucket, self.s3_key)
        formatted_sql = StageToRedshiftOperator.copy_sql.format(
            self.target_table,
            s3_path,
            credentials.access_key,
            credentials.secret_key,
            sql_formatter
        )
        
        self.log.info("Executing importing data sql")
        redshift.run(formatted_sql)
              
        self.log.info("Data successfully copied")