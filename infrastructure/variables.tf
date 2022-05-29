variable app_name {
  description = "Name of an application."
  type        = string
  default     = "smart-home-simulation"
}

variable app_instance_type {
  description = "Type of an EC2 instance."
  type        = string
  default     = "t2.micro"
}

variable user_data_path {
  description = "Path to file storing user data for an EC2."
  type        = string
  default     = "scripts/user_data.sh"
}

variable asg_min_size {
  description = "Minimum number of instances in an auto scaling group."
  type        = number
  default     = 1
}

variable asg_desired_size {
  description = "Desired number of instances in an auto scaling group."
  type        = number
  default     = 1
}

variable asg_max_size {
  description = "Maximum number of instances in an auto scaling group."
  type        = number
  default     = 1
}
