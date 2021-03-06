resource "aws_kms_key" "app_enryption_key" {
  deletion_window_in_days = 10
  enable_key_rotation     = true
  policy                  = data.aws_iam_policy_document.key_policy.json
}

resource "aws_kms_alias" "app_encryption_key" {
  name          = "alias/${var.app_name}kms-key"
  target_key_id = aws_kms_key.app_enryption_key.key_id
}
