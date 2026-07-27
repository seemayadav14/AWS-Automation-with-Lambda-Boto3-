# Auto-Tagging EC2 Instances on Launch Using AWS Lambda

## 📌 Objective

Automatically tag newly launched Amazon EC2 instances using AWS Lambda and Amazon EventBridge. This helps with resource tracking, ownership identification, and cost allocation.

---

# Architecture

```
EC2 Instance Launch
        │
        ▼
Amazon EventBridge Rule
(EC2 State = Running)
        │
        ▼
AWS Lambda Function
        │
        ▼
Add Tags to EC2 Instance
```

---

# AWS Services Used

- Amazon EC2
- AWS Lambda
- Amazon EventBridge
- AWS IAM
- Amazon CloudWatch Logs

---

# Prerequisites

- AWS Account
- IAM permissions to create Lambda, IAM Roles, and EventBridge Rules
- Python 3.12 Runtime
- Existing VPC (optional)

---

# Step 1: Create IAM Role

Create an IAM Role for Lambda with the following trust relationship:

- Trusted Entity:
  - AWS Service
  - Lambda

Attach the following inline policy.

## IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateTags",
        "ec2:DescribeInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

---

# Step 2: Create Lambda Function

- Function Name:
  - AutoTagEC2

- Runtime:
  - Python 3.12

- Execution Role:
  - Use the IAM role created above.

Paste the following code into **lambda_function.py**.

```python
import boto3
from datetime import datetime

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    instance_id = event['detail']['instance-id']

    current_date = datetime.utcnow().strftime("%Y-%m-%d")

    ec2.create_tags(
        Resources=[instance_id],
        Tags=[
            {
                'Key': 'LaunchDate',
                'Value': current_date
            },
            {
                'Key': 'Environment',
                'Value': 'Development'
            }
        ]
    )

    print(f"Successfully tagged instance {instance_id}")

    return {
        "statusCode": 200,
        "body": f"Tags added to {instance_id}"
    }
```

Deploy the Lambda function.

---

# Step 3: Create EventBridge Rule

Open **Amazon EventBridge**.

Create a new rule.

## Rule Type

Event Pattern

### Event Source

AWS Events

### Service

EC2

### Event Type

EC2 Instance State-change Notification

### Event Pattern

```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["running"]
  }
}
```

Choose the Lambda function as the target.

Create the rule.

---

# Step 4: Test the Automation

Launch a new EC2 instance.

Wait approximately one minute.

Open:

EC2 Console → Instances → Tags

You should see tags similar to:

| Key | Value |
|------|-------|
| LaunchDate | 2026-07-28 |
| Environment | Development |

---

# Expected Lambda Output

CloudWatch Logs:

```
Successfully tagged instance i-0123456789abcdef0
```

---

# Expected Result

Before Lambda execution

| Tag | Value |
|------|-------|
| None | None |

After Lambda execution

| Tag | Value |
|------|-------|
| LaunchDate | 2026-07-28 |
| Environment | Development |

---

# CloudWatch Logs

Open

```
CloudWatch
    ↓
Log Groups
        ↓
/aws/lambda/AutoTagEC2
```

Successful log output

```
START RequestId: xxxxxxxxx

Successfully tagged instance i-0123456789abcdef0

END RequestId: xxxxxxxxx

REPORT RequestId: xxxxxxxxx
```

---

# Bonus Task – Automatically Tag the Launching IAM User

Instead of a static Owner tag, you can retrieve the IAM user who launched the EC2 instance from AWS CloudTrail and automatically assign it.

Example:

| Key | Value |
|------|-------|
| Owner | seema.yadav |
| LaunchDate | 2026-07-28 |
| Environment | Development |

This approach is commonly used in production environments and is a frequent AWS interview scenario.

---

# Project Folder Structure

```
Assignment2/

│── Assignment2.md
│── lambda_function.py
│── screenshots/
│     ├── IAM-Role.png
│     ├── Lambda-Configuration.png
│     ├── EventBridge-Rule.png
│     ├── EC2-Before-Tags.png
│     ├── EC2-After-Tags.png
│     ├── CloudWatch-Logs.png
│     └── Test-Success.png
```

---

