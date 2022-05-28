locals {
  region        = data.aws_region.current.name
  account_id    = data.aws_caller_identity.current.account_id
  root_user     = "arn:aws:iam::${local.account_id}:root"
}