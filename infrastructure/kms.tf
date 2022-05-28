resource "aws_kms_key" "app_enryption_key" {
  deletion_window_in_days = 10
  enable_key_rotation     = true
  policy                  = data.aws_iam_policy_document.app_instance_key_policy.json
}

resource "aws_kms_alias" "app_encryption_key" {
  name          = "alias/app-instance-kms-key"
  target_key_id = aws_kms_key.app_enryption_key.key_id
}
