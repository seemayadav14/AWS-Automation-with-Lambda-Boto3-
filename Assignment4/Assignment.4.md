# Restore an EC2 Instance from the Latest Snapshot

## Project Overview

This AWS Lambda project automates disaster recovery by restoring an EC2 instance from the latest available EBS snapshot.

The Lambda function:

- Finds the latest EBS snapshot.
- Registers a new AMI from that snapshot.
- Launches a new EC2 instance using the AMI.
- Adds a tag to identify the snapshot used.
- Prints the new EC2 Instance ID.

---

# Objective

Automate EC2 disaster recovery by rebuilding an EC2 instance from its latest EBS snapshot.

---

# AWS Services Used

- AWS Lambda
- Amazon EC2
- Amazon EBS Snapshots
- AWS IAM
- Amazon CloudWatch

---

# Architecture

```
Latest EBS Snapshot
        │
        ▼
AWS Lambda Function
        │
        ▼
Register AMI
        │
        ▼
Launch EC2 Instance
        │
        ▼
Add Tags
        │
        ▼
CloudWatch Logs
```

---

# Prerequisites

Before running this project, ensure:

- AWS Account
- Existing EC2 Instance
- At least one EBS Snapshot of the root volume
- IAM Role for Lambda
- Python 3.12 Runtime

---

# IAM Permissions

Attach the following permissions to the Lambda execution role.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeSnapshots",
        "ec2:RegisterImage",
        "ec2:RunInstances",
        "ec2:DescribeImages",
        "ec2:CreateTags"
      ],
      "Resource": "*"
    }
  ]
}
```

---

# Lambda Configuration

| Setting | Value |
|----------|-------|
| Runtime | Python 3.12 |
| Handler | lambda_function.lambda_function |
| Timeout | 3 minutes |
| Memory | 128 MB |

---

# Python Code

```python
import boto3
from datetime import datetime

ec2 = boto3.client('ec2')

# Replace with your Volume ID
VOLUME_ID = "vol-xxxxxxxxxxxxxxxxx"

def lambda_function(event, context):

    snapshots = ec2.describe_snapshots(
        Filters=[
            {
                'Name': 'volume-id',
                'Values': [VOLUME_ID]
            }
        ],
        OwnerIds=['self']
    )['Snapshots']

    if not snapshots:
        print("No snapshots found.")
        return

    latest_snapshot = sorted(
        snapshots,
        key=lambda x: x['StartTime'],
        reverse=True
    )[0]

    snapshot_id = latest_snapshot['SnapshotId']

    print(f"Latest Snapshot: {snapshot_id}")

    ami = ec2.register_image(
        Name=f"Recovered-{snapshot_id}",
        Architecture='x86_64',
        RootDeviceName='/dev/xvda',
        VirtualizationType='hvm',
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/xvda',
                'Ebs': {
                    'SnapshotId': snapshot_id,
                    'DeleteOnTermination': True,
                    'VolumeType': 'gp3'
                }
            }
        ]
    )

    ami_id = ami['ImageId']

    print(f"AMI Created: {ami_id}")

    waiter = ec2.get_waiter('image_available')
    waiter.wait(ImageIds=[ami_id])

    response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType='t3.micro',
        MinCount=1,
        MaxCount=1
    )

    instance_id = response['Instances'][0]['InstanceId']

    ec2.create_tags(
        Resources=[instance_id],
        Tags=[
            {
                'Key': 'RestoredFrom',
                'Value': snapshot_id
            }
        ]
    )

    print(f"New EC2 Instance Created: {instance_id}")

    return {
        "statusCode": 200,
        "InstanceId": instance_id,
        "Snapshot": snapshot_id,
        "AMI": ami_id
    }
```

---

# Deployment Steps

## Step 1

Create an EC2 instance.

---

## Step 2

Create an EBS Snapshot of the root volume.

---

## Step 3

Create an IAM Role with:

- DescribeSnapshots
- RegisterImage
- RunInstances
- DescribeImages
- CreateTags

Attach the role to Lambda.

---

## Step 4

Create a Lambda function.

Runtime:

```
Python 3.12
```

---

## Step 5

Paste the Python code.

Replace:

```python
VOLUME_ID = "vol-xxxxxxxxxxxxxxxxx"
```

with your actual EBS Volume ID.

---

## Step 6

Deploy the Lambda function.

---

## Step 7

Click **Test** to manually invoke the function.

---

# Expected Output

```
Latest Snapshot: snap-0123456789abcdef

AMI Created:
ami-0123456789abcdef

New EC2 Instance Created:
i-0123456789abcdef
```

---

# Verification

Open **EC2 Console**

You should see:

- New EC2 instance
- Running state
- Created from latest snapshot
- Tag

```
RestoredFrom=snap-xxxxxxxx
```

---

# CloudWatch Logs

CloudWatch Logs should display:

```
Latest Snapshot Found

AMI Registered

Waiting for AMI Availability

Launching EC2 Instance

Tag Added

Instance Created Successfully
```

---

# Testing

1. Create an EBS Snapshot.
2. Run the Lambda function.
3. Verify the AMI is created.
4. Verify a new EC2 instance launches.
5. Confirm the data from the snapshot is present.
6. Check the `RestoredFrom` tag.
7. Review CloudWatch Logs for successful execution.

---

# Cleanup

To avoid unnecessary AWS charges:

- Terminate the test EC2 instance.
- Deregister the AMI (if no longer needed).
- Delete unused snapshots (if appropriate).
- Delete the Lambda function if it is no longer required.

---

# Screenshots to Include

Include the following screenshots in your GitHub repository:

- EC2 Instance
- EBS Snapshot
- IAM Role Permissions
- Lambda Function Configuration
- Lambda Test Event
- Successful Lambda Execution
- CloudWatch Logs
- Registered AMI
- Newly Created EC2 Instance
- EC2 Tags (`RestoredFrom`)
- Final Output

---

# Repository Structure

```
Assignment4/
│
├── Assignment4.md
├── lambda_function.py
└── screenshots/
    ├── ec2-instance.png
    ├── snapshot.png
    ├── iam-role.png
    ├── lambda-function.png
    ├── test-output.png
    ├── cloudwatch-logs.png
    ├── ami-created.png
    ├── restored-instance.png
    └── tags.png
```

---

# Learning Outcome

After completing this project, you will understand:

- AWS Lambda automation
- EBS Snapshot management
- AMI registration
- EC2 instance recovery
- IAM permissions
- Disaster recovery automation
- CloudWatch logging
- Boto3 EC2 operations

---

**Technology Stack**

- AWS Lambda
- Amazon EC2
- Amazon EBS
- IAM
- CloudWatch
- Python (Boto3)
