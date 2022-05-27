data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "owner-alias"
    values = ["amazon"]
  }

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm*"]
  }
}

resource "aws_launch_template" "app_instance" {
  name_prefix            = "app-instance"
  image_id               = data.aws_ami.amazon_linux_2.id
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.app_instance_private_key_pair.key_name
  vpc_security_group_ids = [aws_security_group.app_instance_active_sg.id]

  iam_instance_profile {
    name = aws_iam_instance_profile.app_instance_profile.name
  }

  monitoring {
    enabled = true
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "app_instance" {
  name_prefix         = aws_launch_template.app_instance.name_prefix
  min_size            = 1
  desired_capacity    = 1
  max_size            = 1
  vpc_zone_identifier = [aws_subnet.main.id]

  launch_template {
    name    = aws_launch_template.app_instance.name
    version = aws_launch_template.app_instance.latest_version
  }

  lifecycle {
    create_before_destroy = true
  }
}