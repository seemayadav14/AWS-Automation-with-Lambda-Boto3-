# AWS Lambda Automation Assignments with Lambda & Boto3

## Overview

This repository contains four AWS Lambda automation projects that demonstrate how to automate common AWS infrastructure management tasks using **Python (Boto3)**, **AWS Lambda**, **Amazon EventBridge**, and **Amazon EC2**. These projects focus on backup automation, resource management, disaster recovery, and cost optimization while following AWS best practices.

Each assignment includes the Lambda function code, IAM permissions, implementation steps, testing procedure, screenshots, and documentation.

---

# Assignment 1: Automated S3 Bucket Cleanup

## Objective
Automatically delete objects that are older than a specified retention period from an Amazon S3 bucket.

## Overview
As organizations store large amounts of data in Amazon S3, unnecessary or outdated files increase storage costs. This project automates the cleanup process by identifying objects older than the configured retention period and deleting them automatically.

### AWS Services Used
- AWS Lambda
- Amazon S3
- Amazon EventBridge
- IAM
- CloudWatch Logs

### Key Features
- Lists all objects in the S3 bucket
- Identifies old files
- Deletes expired objects automatically
- Logs deleted objects in CloudWatch
- Can be scheduled using EventBridge

---

# Assignment 2: Automated EBS Snapshot Creation and Cleanup

## Objective
Automatically create EBS snapshots for backup and remove snapshots older than the configured retention period.

## Overview
This project automates EBS volume backups by creating snapshots on a schedule and deleting outdated snapshots to reduce storage costs. Snapshot tagging is also implemented for easier resource management.

### AWS Services Used
- AWS Lambda
- Amazon EC2 (EBS)
- IAM
- EventBridge
- CloudWatch Logs

### Key Features
- Creates snapshots automatically
- Adds custom tags
- Deletes snapshots older than retention period
- Logs all operations
- Helps implement backup lifecycle automation

---

# Assignment 3: Auto-Tagging EC2 Instances on Launch

## Objective
Automatically apply predefined tags to newly launched EC2 instances.

## Overview
Manual tagging of EC2 instances often leads to inconsistent resource management. This project automatically tags every newly launched EC2 instance using EventBridge events, improving governance, cost allocation, and resource tracking.

### AWS Services Used
- AWS Lambda
- Amazon EC2
- Amazon EventBridge
- IAM
- CloudWatch Logs

### Key Features
- Detects newly launched EC2 instances
- Automatically applies custom tags
- Adds launch date tag
- Supports owner/environment tagging
- Simplifies cost allocation

---

# Assignment 4: Restore an EC2 Instance from the Latest Snapshot

## Objective
Automatically restore an EC2 instance using the latest available EBS snapshot.

## Overview
This project demonstrates disaster recovery automation by locating the most recent EBS snapshot, creating an AMI from it, and launching a new EC2 instance. This minimizes manual intervention during recovery scenarios.

### AWS Services Used
- AWS Lambda
- Amazon EC2
- Amazon EBS
- IAM
- CloudWatch Logs

### Key Features
- Finds the latest EBS snapshot
- Registers a temporary AMI
- Launches a new EC2 instance
- Applies recovery tags
- Supports disaster recovery automation

---

# Repository Structure

```
AWS-Lambda-Automation/
│
├── Automated-S3-Cleanup/
│   ├── lambda_function.py
│   ├── README.md
│   └── screenshots/
│

---

# Technologies Used

- Python 3.12+
- AWS Lambda
- Boto3
- Amazon EC2
- Amazon EBS
- Amazon S3
- Amazon EventBridge
- AWS IAM
- Amazon CloudWatch

---

# Learning Outcomes

After completing these assignments, you will be able to:

- Automate AWS infrastructure using Lambda.
- Work with the Boto3 SDK for AWS services.
- Configure IAM roles using least-privilege access.
- Schedule automation with Amazon EventBridge.
- Monitor Lambda executions using CloudWatch Logs.
- Automate backups and disaster recovery.
- Implement EC2 resource tagging for governance.
- Optimize AWS storage and operational costs.

---

# Author

**Seema Yadav**

AWS Lambda Automation Assignments
