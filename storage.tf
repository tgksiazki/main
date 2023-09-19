/**
provider "aws" {
  region = "us-west-1"
}
**/
# Create 1 unattached disk (EBS volume)
resource "aws_ebs_volume" "unattached" {
  availability_zone = "us-west-1a"
  size              = 10  # Size in GB
}

# Create 2 non-encrypted disks (EBS volumes)
resource "aws_ebs_volume" "non_encrypted" {
  count             = 2
  availability_zone = "us-west-1a"
  size              = 10  # Size in GB
  encrypted         = false
}

# Create 3 non-encrypted snapshots from the first non-encrypted disk
resource "aws_ebs_snapshot" "non_encrypted" {
  count             = 3
  volume_id         = aws_ebs_volume.non_encrypted[0].id
  encrypted         = false
}
