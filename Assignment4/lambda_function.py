import boto3

ec2 = boto3.client("ec2")

VOLUME_ID = "vol-0bcc7d80ce744e0c8"

def lambda_handler(event, context):

    snapshots = ec2.describe_snapshots(
        Filters=[
            {
                "Name": "volume-id",
                "Values": [VOLUME_ID]
            }
        ],
        OwnerIds=["self"]
    )["Snapshots"]

    if not snapshots:
        return {
            "statusCode": 404,
            "body": "No snapshots found."
        }

    latest_snapshot = sorted(
        snapshots,
        key=lambda x: x["StartTime"],
        reverse=True
    )[0]

    snapshot_id = latest_snapshot["SnapshotId"]

    ami_name = f"RestoreAMI-{snapshot_id}"

    response = ec2.register_image(
        Name=ami_name,
        RootDeviceName="/dev/xvda",
        BlockDeviceMappings=[
            {
                "DeviceName": "/dev/xvda",
                "Ebs": {
                    "SnapshotId": snapshot_id,
                    "VolumeSize": latest_snapshot["VolumeSize"],
                    "VolumeType": "gp3",
                    "DeleteOnTermination": True
                }
            }
        ],
        VirtualizationType="hvm",
        Architecture="x86_64"
    )

    ami_id = response["ImageId"]

    waiter = ec2.get_waiter("image_available")
    waiter.wait(ImageIds=[ami_id])

    instance = ec2.run_instances(
        ImageId=ami_id,
        InstanceType="t3.micro",
        MinCount=1,
        MaxCount=1
    )

    instance_id = instance["Instances"][0]["InstanceId"]

    ec2.create_tags(
        Resources=[instance_id],
        Tags=[
            {
                "Key": "RestoredFrom",
                "Value": snapshot_id
            }
        ]
    )

    print("Instance Created:", instance_id)

    return {
        "statusCode": 200,
        "InstanceId": instance_id,
        "SnapshotId": snapshot_id,
        "AMI": ami_id
    }
