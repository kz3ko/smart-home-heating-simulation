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

resource "aws_launch_template" "ec2" {
  name          = var.app_name
  image_id      = data.aws_ami.amazon_linux_2.id
  instance_type = var.app_instance_type
  key_name      = aws_key_pair.ec2_private_key_pair.key_name
  user_data     = base64encode(file("${path.module}/${var.user_data_path}"))
  depends_on    = [aws_internet_gateway.internet_gateway]

  iam_instance_profile {
    name = aws_iam_instance_profile.ec2_profile.name
  }

  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.main.id]
    subnet_id                   = aws_subnet.public.id
  }

  monitoring {
    enabled = true
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "auto_scaling_group" {
  name_prefix         = aws_launch_template.ec2.name_prefix
  min_size            = var.asg_min_size
  desired_capacity    = var.asg_desired_size
  max_size            = var.asg_max_size
  vpc_zone_identifier = [aws_subnet.public.id]

  launch_template {
    name    = aws_launch_template.ec2.name
    version = aws_launch_template.ec2.latest_version
  }

  lifecycle {
    create_before_destroy = true
  }
}