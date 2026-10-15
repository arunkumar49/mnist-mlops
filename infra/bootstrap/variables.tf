variable "aws_region" {
  description = "AWS region for all resources."
  type        = string
  default     = "ap-south-1"
}

variable "project" {
  description = "Project name, used in resource names and tags."
  type        = string
  default     = "mnist-mlops"
}

variable "owner" {
  description = "Owner tag value."
  type        = string
  default     = "mlops-admin"
}

variable "cost_center" {
  description = "Cost-center tag value, for grouping costs in billing."
  type        = string
  default     = "learning"
}
