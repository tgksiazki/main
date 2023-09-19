import boto3
import time

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2', region_name='us-west-1')

    # Create 1 unattached disk (EBS volume)
    unattached_volume = ec2.create_volume(AvailabilityZone='us-west-1a', Size=10)
    print("Created unattached volume with ID:", unattached_volume.id)
    time.sleep(10)  # Give AWS some time to reflect the changes

    # Create 2 non-encrypted disks (EBS volumes)
    non_encrypted_volumes = []
    for i in range(2):
        non_encrypted_volume = ec2.create_volume(AvailabilityZone='us-west-1a', Size=10, Encrypted=False)
        non_encrypted_volumes.append(non_encrypted_volume)
        print("Created non-encrypted volume with ID:", non_encrypted_volume.id)
    time.sleep(10)  # Give AWS some time to reflect the changes

    # Create 3 non-encrypted snapshots from the first non-encrypted disk
    for i in range(3):
        non_encrypted_snapshot = ec2.create_snapshot(VolumeId=non_encrypted_volumes[0].id, Description="Non-encrypted snapshot", Encrypted=False)
        print("Created non-encrypted snapshot with ID:", non_encrypted_snapshot.id)
    time.sleep(10)  # Give AWS some time to reflect the changes

    # Collect metrics
    metrics = {"UnattachedVolumes": 0, "NonEncryptedVolumes": 0, "NonEncryptedSnapshots": 0, "TotalUnattachedVolumeSize": 0, "TotalNonEncryptedVolumeSize": 0}

    for volume in ec2.volumes.all():
        if len(volume.attachments) == 0:
            metrics["UnattachedVolumes"] += 1
            metrics["TotalUnattachedVolumeSize"] += volume.size

        if not volume.encrypted:
            metrics["NonEncryptedVolumes"] += 1
            metrics["TotalNonEncryptedVolumeSize"] += volume.size

    for snapshot in ec2.snapshots.filter(OwnerIds=['self']):
        if not snapshot.encrypted:
            metrics["NonEncryptedSnapshots"] += 1

    print(metrics)
