import boto3
import json
from datetime import datetime

ec2 = boto3.client("ec2")

def lambda_handler(event, context):

    print("Received Event:")
    print(json.dumps(event, indent=2))

    if "detail" not in event:
        return {
            "statusCode": 400,
            "body": "No detail field found."
        }

    instance_id = event["detail"]["instance-id"]

    launch_date = datetime.utcnow().strftime("%Y-%m-%d")

    ec2.create_tags(
        Resources=[instance_id],
        Tags=[
            {"Key": "LaunchDate", "Value": launch_date},
            {"Key": "Environment", "Value": "Production"}
        ]
    )

    print(f"Tagged {instance_id}")

    return {
        "statusCode": 200,
        "body": "Success"
    }