import boto3
from etc.conf import settings

s3_client = boto3.client(
    's3',
    region_name='ap-southeast-1',
    aws_access_key_id=settings.S3_ACCESSKEY,
    aws_secret_access_key=settings.S3_SECRETKEY
)

resource = boto3.resource('s3',
                          region_name='ap-southeast-1',
                          aws_access_key_id=settings.S3_ACCESSKEY,
                          aws_secret_access_key=settings.S3_SECRETKEY
                          )