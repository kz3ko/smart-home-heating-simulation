data "aws_iam_policy_document" "ec2_assume_role_policy" {
  statement {
    sid     = "EC2AssumeRole"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "ec2_role_policy" {
  statement {
    sid    = "EC2InstanceRole"
    effect = "Allow"
    actions = [
      "ec2:*",
      "s3:*"
    ]
    resources = ["*"]
  }
}

data "aws_iam_policy_document" "s3_bucket_policy" {
  statement {
    sid     = "S3"
    effect  = "Allow"
    actions = ["s3:*"]
    principals {
      type = "AWS"
      identifiers = [
        aws_iam_role.ec2_role.arn
      ]
    }
    resources = [
      aws_s3_bucket.s3.arn,
      "${aws_s3_bucket.s3.arn}/*",
    ]
  }
}

data "aws_iam_policy_document" "key_policy" {
  statement {
    sid     = "KMS"
    effect  = "Allow"
    actions = ["kms:*"]
    principals {
      type = "AWS"
      identifiers = [
        local.root_user,
        aws_iam_role.ec2_role.arn
      ]
    }
    resources = ["*"]
  }
}

resource "aws_iam_role" "ec2_role" {
  name               = "${var.app_name}-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role_policy.json
}

resource "aws_iam_role_policy" "ec2_role_policy" {
  name   = "${aws_iam_role.ec2_role.name}-policy"
  role   = aws_iam_role.ec2_role.id
  policy = data.aws_iam_policy_document.ec2_role_policy.json
}

resource "aws_iam_role_policy_attachment" "ssm_policy_attachment" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.app_name}-role"
  role = aws_iam_role.ec2_role.id
}

resource "aws_s3_bucket_policy" "s3_bucket_policy" {
  bucket = aws_s3_bucket.s3.id
  policy = data.aws_iam_policy_document.s3_bucket_policy.json
}
