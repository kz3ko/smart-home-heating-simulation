locals {
  region     = data.aws_region.current.name
  account_id = data.aws_caller_identity.current.account_id
  root_user  = "arn:aws:iam::${local.account_id}:root"

  app_name          = "smart-home-simulation"
  app_instance_type = "t2.micro"

  user_data_path = "scripts/user-data.sh"

  asg_min_size     = 1
  asg_desired_size = 1
  asg_max_size     = 1
}
