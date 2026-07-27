import boto3
from datetime import datetime, timedelta, timezone

ec2 = boto3.client('ec2')

# Replace with your Volume ID
VOLUME_ID = 'vol-000e7613a0f445018'

RETENTION_DAYS = 30


def lambda_handler(event, context):

    # Create Snapshot
    response = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description='Automated Lambda Backup'
    )

    snapshot_id = response['SnapshotId']

    # Tag Snapshot
    ec2.create_tags(
        Resources=[snapshot_id],
        Tags=[
            {
                'Key': 'CreatedBy',
                'Value': 'Lambda-Backup'
            }
        ]
    )

    print(f"Created Snapshot: {snapshot_id}")

    # Find snapshots created by Lambda
    snapshots = ec2.describe_snapshots(
        OwnerIds=['self'],
        Filters=[
            {
                'Name': 'tag:CreatedBy',
                'Values': ['Lambda-Backup']
            }
        ]
    )['Snapshots']

    cutoff = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)

    deleted = []

    for snapshot in snapshots:

        if snapshot['StartTime'] < cutoff:

            ec2.delete_snapshot(
                SnapshotId=snapshot['SnapshotId']
            )

            deleted.append(snapshot['SnapshotId'])

    print("Deleted Snapshots:", deleted)

    return {
        "CreatedSnapshot": snapshot_id,
        "DeletedSnapshots": deleted
    }