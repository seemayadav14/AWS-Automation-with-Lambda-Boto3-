# Automated S3 Bucket Cleanup (Objects Older Than 30 Days)

## Objective

Automatically delete objects from an Amazon S3 bucket that are older than **30 days** using an AWS Lambda function written in Python (Boto3).

---

# Project Overview

This project automates the cleanup of stale files stored in an Amazon S3 bucket.

The Lambda function:

- Lists all objects in the S3 bucket.
- Uses an S3 paginator to retrieve every object.
- Compares each object's **LastModified** timestamp with the current UTC time.
- Deletes files older than **30 days**.
- Logs the names of deleted files in Amazon CloudWatch Logs.

---

# Architecture

```
Upload Files
      │
      ▼
 Amazon S3 Bucket
      │
      ▼
 AWS Lambda (Python + Boto3)
      │
      ▼
Checks Object Age
      │
      ▼
Deletes Files Older Than 30 Days
      │
      ▼
CloudWatch Logs
```

---

# AWS Services Used

- Amazon S3
- AWS Lambda
- AWS IAM
- Amazon CloudWatch
- Boto3 (Python SDK)

---

# Prerequisites

Before starting, make sure you have:

- AWS Account
- IAM User with Administrator access (or required permissions)
- Python 3.12 Runtime for Lambda
- Existing S3 Bucket

Example Bucket:

```
seema-s3-cleanup-bucket
```

---

# Step 1: Create an S3 Bucket

1. Open AWS Console.
2. Navigate to **Amazon S3**.
3. Click **Create Bucket**.
4. Enter a unique bucket name.
5. Leave default settings.
6. Create the bucket.
7. Upload several files.

For testing purposes:

Since it is difficult to create files older than 30 days, temporarily reduce the age threshold in the Lambda code to a few minutes.

After successful testing, change it back to **30 days**.

---

# Step 2: Create IAM Role

Create a Lambda execution role.

### Trusted Entity

```
AWS Service
```

Select

```
Lambda
```

Attach the following inline policy.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListBucket",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME"
    },
    {
      "Sid": "DeleteObjects",
      "Effect": "Allow",
      "Action": [
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
    }
  ]
}
```

Replace:

```
YOUR_BUCKET_NAME
```

with your bucket name.

---

# Step 3: Create Lambda Function

Runtime:

```
Python 3.12
```

Function Name

```
S3CleanupFunction
```

Assign the IAM role created above.

---

# Step 4: Lambda Code

```python
import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client("s3")

BUCKET_NAME = "seema-s3-cleanup-bucket"

def lambda_function(event, context):

    days_old = 30

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_old)

    paginator = s3.get_paginator("list_objects_v2")

    deleted_files = []

    for page in paginator.paginate(Bucket=BUCKET_NAME):

        if "Contents" not in page:
            continue

        for obj in page["Contents"]:

            if obj["LastModified"] < cutoff_date:

                s3.delete_object(
                    Bucket=BUCKET_NAME,
                    Key=obj["Key"]
                )

                deleted_files.append(obj["Key"])

                print(f"Deleted: {obj['Key']}")

    if not deleted_files:
        print("No files older than 30 days found.")

    return {
        "statusCode": 200,
        "body": {
            "deleted_files": deleted_files
        }
    }
```

Replace:

```
seema-s3-cleanup-bucket
```

with your bucket name.

---

# Step 5: Deploy

Click

```
Deploy
```

---

# Step 6: Test the Lambda Function

Create a test event.

Example:

```json
{}
```

Click

```
Test
```

---

# Expected Output

If old files exist:

```
Deleted: image1.png

Deleted: backup.zip

Deleted: report.pdf
```

If no old files exist:

```
No files older than 30 days found.
```

---

# CloudWatch Logs

Open:

```
CloudWatch

→ Log Groups

→ /aws/lambda/S3CleanupFunction
```

Verify:

- Deleted file names
- Execution status
- Duration
- Memory usage

---

# Project Structure

```
Assignment1/

│── Assignment1.md

│── lambda_function.py

└── screenshots/
    │── bucket.png
    │── iam-role.png
    │── lambda.png
    │── deploy.png
    │── test.png
    └── cloudwatch.png
```

---

# Screenshots to Include

Include screenshots of:

- S3 Bucket
- Uploaded Files
- IAM Role
- IAM Policy
- Lambda Function
- Lambda Code
- Deploy Success
- Test Event
- Successful Test Output
- CloudWatch Logs

---

# Testing

For testing:

- Change

```python
timedelta(days=30)
```

to

```python
timedelta(minutes=2)
```

Upload files.

Wait 2–3 minutes.

Run Lambda.

Confirm older files are deleted.

After testing, change it back to:

```python
timedelta(days=30)
```

---




AWS Lambda Assignment

