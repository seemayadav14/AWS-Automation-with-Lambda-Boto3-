# Automated EBS Snapshot Creation and Cleanup using AWS Lambda

## Objective
Automate the creation of Amazon EBS snapshots for backup purposes and delete snapshots older than a specified retention period (30 days).

---

# Architecture

```
+------------------+
|  EventBridge     |
| (Weekly Trigger) |
+--------+---------+
         |
         v
+-------------------------+
| AWS Lambda (Python)     |
|-------------------------|
| 1. Create Snapshot      |
| 2. Add Tags             |
| 3. List Old Snapshots   |
| 4. Delete Old Snapshots |
+-----------+-------------+
            |
            v
+--------------------------+
| Amazon EC2 / EBS Volume  |
+--------------------------+
```

---

# Prerequisites

- AWS Account
- An existing EC2 instance with an attached EBS volume
- IAM permissions to create and delete snapshots
- Python 3.12 Runtime
- AWS Lambda
- Amazon EventBridge

---

# AWS Services Used

- AWS Lambda
- Amazon EC2
- Amazon EBS
- Amazon EventBridge
- AWS IAM
- Amazon CloudWatch

---

# Step 1: Create or Identify an EBS Volume

1. Open the AWS Console.
2. Navigate to **EC2**.
3. Select **Elastic Block Store → Volumes**.
4. Copy the **Volume ID**.

Example:

```
vol-0123456789abcdef0
```

---

# Step 2: Create IAM Role

Create a Lambda execution role.

### Trusted Entity

- AWS Service
- Lambda

---

## Inline IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateSnapshot",
        "ec2:DescribeSnapshots",
        "ec2:DeleteSnapshot",
        "ec2:CreateTags"
      ],
      "Resource": "*"
    }
  ]
}
```

---

# Step 3: Create Lambda Function

Runtime:

```
Python 3.12
```

Function Name:

```
EBS-Snapshot-Backup
```

Paste the Python code into the Lambda function.

---

# Step 4: Configure Environment Variable (Optional)

Instead of hardcoding the Volume ID, create an environment variable.

| Key | Value |
|------|--------|
| VOLUME_ID | vol-xxxxxxxxxxxxxxxx |

---

# Step 5: Deploy the Function

Click **Deploy** after saving the code.

---

# Step 6: Test the Lambda Function

1. Click **Test**
2. Create a new test event.
3. Use the default JSON.
4. Click **Test** again.

Expected CloudWatch Logs:

```
Created Snapshot:
snap-0abcd123456789xyz

Deleted Snapshot:
snap-01234567890abcdef
```

---

# Step 7: Verify Snapshot Creation

Go to:

```
EC2
→ Snapshots
```

Verify:

- New snapshot created
- Tag added

Example Tags

| Key | Value |
|------|--------|
| CreatedBy | Lambda-Backup |

---

# Step 8: Verify Cleanup

If snapshots older than 30 days exist:

```
EC2
→ Snapshots
```

They should be automatically deleted.

---

# Step 9: Configure EventBridge

Navigate to:

```
Amazon EventBridge
```

Create Rule

Name

```
Weekly-EBS-Backup
```

Schedule

```
Rate Expression

rate(7 days)
```

Target

```
AWS Lambda

EBS-Snapshot-Backup
```

Save the rule.

---

# Testing Checklist

- Lambda executes successfully.
- Snapshot is created.
- Snapshot contains the tag:

```
CreatedBy = Lambda-Backup
```

- Old snapshots (>30 days) are deleted.
- CloudWatch logs show created and deleted snapshot IDs.
- EventBridge invokes Lambda automatically every week.

---

# CloudWatch Logs

Verify execution:

```
CloudWatch

→ Log Groups

→ /aws/lambda/EBS-Snapshot-Backup
```

Example:

```
START RequestId...

Created Snapshot:
snap-0d7fd98a56c98d1a

Deleted Snapshot:
snap-0ae762341cb83f7b

END RequestId...
```

---

# Project Structure

```
Assignment2

│
├── Assignment2.md
├── lambda_function.py
└── screenshots/
    ├── 01-ebs-volume.png
    ├── 02-iam-policy.png
    ├── 03-lambda-code.png
    ├── 04-test-success.png
    ├── 05-created-snapshot.png
    ├── 06-tags.png
    ├── 07-cloudwatch-logs.png
    └── 08-eventbridge-rule.png
```

---

# Screenshots to Include

## 1. EBS Volume

- Volume ID
- State

---

## 2. IAM Role

- Inline Policy
- Permissions

---

## 3. Lambda Function

- Runtime
- Function Name
- Code

---

## 4. Test Execution

Successful Lambda execution.

---

## 5. Snapshot Created

EC2 → Snapshots page showing the newly created snapshot.

---

## 6. Snapshot Tags

Display the `CreatedBy=Lambda-Backup` tag.

---

## 7. CloudWatch Logs

Execution logs showing created and deleted snapshot IDs.

---

## 8. EventBridge Rule

Weekly schedule and Lambda target.

---

# Expected Output

```
Created Snapshot:
snap-0123456789abcdef0

Tagged Snapshot:
CreatedBy = Lambda-Backup

Deleted Snapshot:
snap-0abcdef1234567890
```

---

