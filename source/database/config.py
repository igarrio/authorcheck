import os
import boto3

dynamodb_client = boto3.resource(service_name='dynamodb', region_name='eu-central-1',
                                 aws_access_key_id=os.environ.get('aws_access_key_id'),
                                 aws_secret_access_key=os.environ.get('aws_secret_access_key'))