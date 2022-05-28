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
  name_prefix   = "app-instance"
  image_id      = data.aws_ami.amazon_linux_2.id
  instance_type = "t2.micro"
  key_name      = aws_key_pair.app_instance_private_key_pair.key_name
  user_data     = base64encode(file("${path.module}/scripts/user-data.sh"))
  depends_on    = [aws_internet_gateway.main]

  iam_instance_profile {
    name = aws_iam_instance_profile.app_instance_profile.name
  }

  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.default.id]
    subnet_id                   = aws_subnet.public.id
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
  vpc_zone_identifier = [aws_subnet.public.id]

  launch_template {
    name    = aws_launch_template.app_instance.name
    version = aws_launch_template.app_instance.latest_version
  }

  lifecycle {
    create_before_destroy = true
  }
}