terraform {
  backend "s3" {
    bucket = "pwc-skrzyniarzplesniarski-eu-west-1-tfstate"
    key    = "eu-west-1.tfstate"
    region = "eu-west-1"
  }
}
