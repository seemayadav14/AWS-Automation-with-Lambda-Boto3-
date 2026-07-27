
Serverless-Architecture_HeroVired-Assignment
HeroVired Assignment on Serverless Architecture using AWS Lambda and Boto3

Assignment 1: Automated S3 Bucket Cleanup Using AWS Lambda and Boto3
Objective: In this assignment, we will gain experience with AWS Lambda and Boto3 by creating a Lambda function that will automatically clean up old files in an S3 bucket.
Task: Automate the deletion of files older than 30 days in a specific S3 bucket.
                                 
                                                                                  
Step 1: S3 Setup
1.Navigate to the S3 dashboard and create a new bucket.
 
2.Upload multiple files to this bucket, ensuring that some files are older than 30 days (you may need to adjust your system's date temporarily for this or use old files). 
 

 
 
Step 2: Lambda IAM Role
1.In the IAM dashboard, create a new role for Lambda by attaching the following roles AmazonS3FullAccess and AWSLambdaBasicExecutionRole.
 

2.IAM Role Inline Policy
 
 

Step 3: Lambda Function
1.Navigate to the Lambda dashboard, create a new function by choosing Python 3.14 as the runtime and assign the custom role created previous step.
 
2.Write the Boto3 Python script to:
i.	Initialize a boto3 S3 client.
ii.	List objects in the specified bucket.
iii.	Delete objects older than 30 days.
iv.	Print the names of deleted objects for logging purposes

import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = 'seema-s3-cleanup-bucket'

def lambda_handler(event, context):

    days_old = 30

    cutoff_date = datetime.now(timezone.utc) - timedelta(minutes=1)

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


Step 4:Deployment of code with Lambda function
 
Step 5: Manual Invocation
1.After saving the function, manually trigger i 
2.Go to the S3 dashboard and confirm that only files newer than 30 days remain.
 

3.Check in CloudWatch logs the files which were deleted.
 
 









