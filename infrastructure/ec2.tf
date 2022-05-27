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

resource "aws_launch_configuration" "app_instance" {
  name_prefix                 = "app-instance"
  image_id                    = data.aws_ami.amazon_linux_2.id
  instance_type               = "t2.micro"
  associate_public_ip_address = false
  iam_instance_profile        = aws_iam_instance_profile.app_instance_profile.id
  key_name                    = aws_key_pair.app_instance_private_key_pair.key_name
  security_groups             = [aws_security_group.app_instance_active_sg.id]
  user_data                   = file("${path.module}/scripts/app-instance-userdata.sh")

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "app_instance" {
  name                 = aws_launch_configuration.app_instance.name
  launch_configuration = aws_launch_configuration.app_instance.name
  capacity_rebalance   = true
  min_size             = 1
  max_size             = 1
  desired_capacity     = 1
  vpc_zone_identifier  = [aws_subnet.main.id]

  lifecycle {
    create_before_destroy = true
  }
}
