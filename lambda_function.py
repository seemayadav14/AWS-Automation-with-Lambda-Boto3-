import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = 'seema-s3-cleanup-bucket'

def lambda_function(event, context):

    days_old = 30

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_old)

    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME
    )

    deleted_files = []

    if 'Contents' in response:

        for obj in response['Contents']:

            object_key = obj['Key']
            last_modified = obj['LastModified']

            if last_modified < cutoff_date:

                s3.delete_object(
                    Bucket=BUCKET_NAME,
                    Key=object_key
                )

                deleted_files.append(object_key)

                print(
                    f"Deleted: {object_key}"
                )

    print(
        f"Total Deleted Files: {len(deleted_files)}"
    )

    return {
        'statusCode': 200,
        'deleted_files': deleted_files
    }