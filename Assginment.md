# AWS Lambda Assignment – Automated S3 Bucket Cleanup

## 📌 Project Overview

This project automates the deletion of objects older than **30 days** from an Amazon S3 bucket using **AWS Lambda** and **Amazon EventBridge**.

---

## 🎯 Objective

Automatically identify and delete files older than 30 days from an S3 bucket.

---

## 🛠️ AWS Services Used

* AWS Lambda
* Amazon S3
* Amazon EventBridge
* AWS IAM
* Amazon CloudWatch

---

## 📋 Prerequisites

* AWS Account
* IAM Role with required permissions
* S3 Bucket
* Python 3.12 Runtime
* Boto3 Library (available in Lambda)

---

# Step 1: Create an S3 Bucket

1. Open the AWS Management Console.
2. Navigate to **Amazon S3**.
3. Click **Create Bucket**.
4. Enter a unique bucket name.
5. Create the bucket.

### Screenshot

![S3 Bucket](02.png)

---

# Step 2: Upload Test Files

Upload a few files to the bucket for testing.

### Screenshot

![Upload Files](images/upload-files.png)

---

# Step 3: Create IAM Role

Create an IAM role with permissions:

* s3:ListBucket
* s3:DeleteObject

Attach the role to the Lambda function.

### Screenshot

![IAM Role](images/iam-role.png)

---

# Step 4: Create Lambda Function

1. Open AWS Lambda.
2. Click **Create Function**.
3. Select **Author from Scratch**.
4. Runtime: **Python 3.12**
5. Attach the IAM role.

### Screenshot

![Lambda Function](images/lambda-function.png)

---

# Step 5: Add Python Code

Paste the Python code into the Lambda editor and deploy the function.

### Screenshot

![Lambda Code](images/lambda-code.png)

---

# Step 6: Configure EventBridge Trigger

1. Open Amazon EventBridge.
2. Create a scheduled rule.
3. Configure it to trigger the Lambda function automatically.

### Screenshot

![EventBridge](images/eventbridge.png)

---

# Step 7: Test the Lambda Function

1. Click **Test**.
2. Execute the function.
3. Verify that old files are deleted.

### Screenshot

![Lambda Test](images/lambda-test.png)

---

# Step 8: Verify CloudWatch Logs

Open **CloudWatch Logs** to verify successful execution.

### Screenshot

![CloudWatch Logs](images/cloudwatch-logs.png)

---

# 📂 Repository Structure

```text
AWS-S3-Cleanup/
│
├── README.md
├── lambda_function.py
├── images/
│   ├── s3-bucket.png
│   ├── upload-files.png
│   ├── iam-role.png
│   ├── lambda-function.png
│   ├── lambda-code.png
│   ├── eventbridge.png
│   ├── lambda-test.png
│   └── cloudwatch-logs.png
```

---

# ▶️ How to Run

1. Create the S3 bucket.
2. Upload sample files.
3. Create the IAM role.
4. Deploy the Lambda function.
5. Configure the EventBridge trigger.
6. Test the Lambda function.
7. Verify the CloudWatch logs.

---

# ✅ Expected Output

* Objects older than 30 days are automatically deleted.
* Successful execution is recorded in CloudWatch Logs.

---

# 👩‍💻 Author

**Seema Yadav**

AWS Lambda Automation Assignment
