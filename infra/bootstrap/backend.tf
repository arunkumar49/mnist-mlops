terraform {
  backend "s3" {
    bucket       = "mnist-mlops-tfstate-b0eb75"
    key          = "bootstrap/terraform.tfstate"
    region       = "ap-south-1"
    encrypt      = true
    use_lockfile = true
  }
}
