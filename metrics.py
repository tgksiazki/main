import boto3

# AWS access details
aws_access_key_id = "ACCESS_KEY_ID"
aws_secret_access_key = "SECRET_ACCESS_KEY"
region_name = "us-west-1"

# Boto3 client
ec2 = boto3.client(
    "ec2",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name,
)

# Metrics dictionary
metrics = {"UnattachedVolumes": 0, "NonEncryptedVolumes": 0, "NonEncryptedSnapshots": 0}

# Get all volumes
volumes = ec2.describe_volumes()["Volumes"]

# Iterate over volumes
for volume in volumes:
    # Check for unattached volumes
    if len(volume["Attachments"]) == 0:
        metrics["UnattachedVolumes"] += 1

    # Check for non-encrypted volumes
    if not volume["Encrypted"]:
        metrics["NonEncryptedVolumes"] += 1

# Get all snapshots
snapshots = ec2.describe_snapshots(OwnerIds=["self"])["Snapshots"]

# Iterate over snapshots
for snapshot in snapshots:
    # Check for non-encrypted snapshots
    if not snapshot["Encrypted"]:
        metrics["NonEncryptedSnapshots"] += 1

print(metrics)
