import boto3
from datetime import datetime

ec2 = boto3.client('ec2')

# Change these values
OWNER_ID = "self"
VOLUME_ID = "vol-xxxxxxxxxxxxxxxxx"

def lambda_handler(event, context):

    # Step 1: Get all snapshots
    snapshots = ec2.describe_snapshots(
        OwnerIds=[OWNER_ID],
        Filters=[
            {
                'Name': 'volume-id',
                'Values': [VOLUME_ID]
            }
        ]
    )['Snapshots']

    if not snapshots:
        return {
            "statusCode": 404,
            "body": "No snapshots found."
        }

    # Step 2: Find latest snapshot
    latest_snapshot = sorted(
        snapshots,
        key=lambda x: x['StartTime'],
        reverse=True
    )[0]

    snapshot_id = latest_snapshot['SnapshotId']

    print("Latest Snapshot:", snapshot_id)

    # Step 3: Register AMI

    image_name = f"Restore-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

    response = ec2.register_image(
        Name=image_name,
        Architecture='x86_64',
        RootDeviceName='/dev/xvda',
        VirtualizationType='hvm',
        EnaSupport=True,
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

    image_id = response['ImageId']

    print("AMI:", image_id)

    # Step 4: Wait until AMI becomes available

    waiter = ec2.get_waiter('image_available')
    waiter.wait(ImageIds=[image_id])

    print("AMI Available")

    # Step 5: Launch Instance

    launch = ec2.run_instances(
        ImageId=image_id,
        InstanceType='t3.micro',
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'RestoredFrom',
                        'Value': snapshot_id
                    },
                    {
                        'Key': 'Name',
                        'Value': 'Restored-Instance'
                    }
                ]
            }
        ]
    )

    instance_id = launch['Instances'][0]['InstanceId']

    print("New Instance:", instance_id)

    return {
        "statusCode": 200,
        "Snapshot": snapshot_id,
        "AMI": image_id,
        "Instance": instance_id
    }