locals {
  common_tags = {
    project       = var.project
    environment   = "shared"
    owner         = var.owner
    "cost-center" = var.cost_center
    "managed-by"  = "terraform"
    stack         = "bootstrap"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = local.common_tags
  }
}
