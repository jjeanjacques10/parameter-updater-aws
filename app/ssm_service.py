import os

import boto3
import botocore
from botocore.config import Config

ENVIRONMENT = os.getenv('ENVIRONMENT')


class SSMService:
    def __init__(self, parameter_store_name=None):
        # TODO: delete
        print("😎👀✨ ENVIRONMENT: ", ENVIRONMENT)
        self.ssm = boto3.client(
            'ssm',
            endpoint_url='http://localstack:4566' if ENVIRONMENT == 'local' else None,  # LocalStack endpoint
            region_name='us-east-1',  # The region specified in your docker-compose.yml
            aws_access_key_id='admin',  # LocalStack uses 'admin' for both access key and secret key
            aws_secret_access_key='admin',
            config=Config(
                connect_timeout=2,  # Timeout for establishing a connection (in seconds)
                read_timeout=3  # Timeout for reading a response (in seconds)
            )
        )
        self.parameter_store_name = parameter_store_name

    def get_parameter_store_value(self):
        try:
            response = self.ssm.get_parameter(Name=self.parameter_store_name, WithDecryption=True)
            return response['Parameter']['Value']
        except botocore.exceptions.ClientError as e:
            print(e)
            # throw exception error
            raise e

    def update_parameter_store_value(self, parameters):
        try:
            response = self.ssm.put_parameter(
                Name=self.parameter_store_name,
                Description='Parameters for onepiece-app',
                Value=parameters,
                Type='SecureString',
                Overwrite=True
            )
            print(response)
        except botocore.exceptions.ClientError as e:
            print(e)
            raise e
