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

# CloudWatch Metric Alarm for disk usage
resource "aws_cloudwatch_metric_alarm" "disk_usage" {
  alarm_name          = "disk-usage-alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "2"
  metric_name         = "DiskWriteBytes"
  namespace           = "AWS/EBS"
  period              = "60"
  statistic           = "SampleCount"
  threshold           = "20000000"
  alarm_description   = "This metric checks disk usage"
  alarm_actions       = [aws_sns_topic.disk_usage.arn]
  dimensions = {
    VolumeId = aws_ebs_volume.unattached.id
  }
}

resource "aws_sns_topic" "disk_usage" {
  name = "disk-usage"
}

# CloudWatch Log Group for EBS volumes
resource "aws_cloudwatch_log_group" "ebs_log_group" {
  name = "/aws/ebs/${aws_ebs_volume.unattached.id}"
}
