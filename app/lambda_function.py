import boto3
import botocore

def lambda_handler(event, context):
   print('Hello World')
   print(get_parameter_store_value())

def get_parameter_store_value():
   ssm = boto3.client('ssm')
   try:
       response = ssm.get_parameter(Name='/dev/onepiece-app/env', WithDecryption=True)
       return response['Parameter']['Value']
   except botocore.exceptions.ClientError as e:
       print(e)
       return None


if (__name__ == '__main__'):
   lambda_handler(None, None)