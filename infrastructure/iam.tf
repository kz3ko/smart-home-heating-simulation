data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "app_instance_policy" {
  statement {
    sid       = "Ec2"
    effect    = "Allow"
    actions   = ["ec2:*"]
    resources = ["*"]
  }
}

resource "aws_iam_role" "app_instance_role" {
  name               = "app-instance-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
}

resource "aws_iam_role_policy" "app_instance_policy" {
  name   = "app-instance-hub-policy"
  role   = aws_iam_role.app_instance_role.id
  policy = data.aws_iam_policy_document.app_instance_policy.json
}

resource "aws_iam_role_policy_attachment" "app_instance_ssm_policy_3" {
  role       = aws_iam_role.app_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role_policy_attachment" "app_instance_ssm_policy_4" {
  role       = aws_iam_role.app_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM"
}

resource "aws_iam_policy_attachment" "app_instance_ssm_policy_1" {
  name       = "first-attachment"
  roles      = [aws_iam_role.app_instance_role.id]
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_policy_attachment" "app_instance_ssm_policy_2" {
  name       = "second-attachment"
  roles      = [aws_iam_role.app_instance_role.id]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM"
}

resource "aws_iam_instance_profile" "app_instance_profile" {
  name = "app-instance-role"
  role = aws_iam_role.app_instance_role.id
}
