resource "aws_iam_role" "app_instance_role" {
  name = "app-instance-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_instance_profile" "app_instance_profile" {
  name = "app-instance-profile"
  role = aws_iam_role.app_instance_role.id
}

resource "aws_iam_policy_attachment" "app_instance_attachment" {
  name       = "app-instance-attachment"
  roles      = [aws_iam_role.app_instance_role.id]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM"
}

resource "aws_instance" "app_instance" {
  ami                         = "ami-07bd2fc45c8a8dd48"
  instance_type               = "t2.micro"
  iam_instance_profile        = aws_iam_instance_profile.app_instance_profile.id
  user_data                   = file("${path.module}/scripts/docker_install.sh")
  monitoring                  = true
  associate_public_ip_address = false

  credit_specification {
    cpu_credits = "unlimited"
  }
}
