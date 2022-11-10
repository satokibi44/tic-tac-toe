# definition provider
provider "aws" {
    version = "~> 2.0"
    region = "${var.provider_region}"
    access_key = "${var.secret_access_key}"
    secret_key = "${var.secret_key}"
}