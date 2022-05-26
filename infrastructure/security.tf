resource "tls_private_key" "app_instance_private_key" {
  algorithm = "RSA"
}

resource "aws_key_pair" "app_instance_private_key_pair" {
  key_name   = "app-instance-private-key-pair"
  public_key = tls_private_key.app_instance_private_key.public_key_openssh
}

resource "aws_security_group" "app_instance_active_sg" {
  name_prefix = "app-instance-active-sg-"
  vpc_id      = aws_vpc.main.id
}

resource "aws_security_group_rule" "egress_all" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.app_instance_active_sg.id
}

resource "aws_security_group_rule" "ingress_all" {
  type              = "ingress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.app_instance_active_sg.id
}
