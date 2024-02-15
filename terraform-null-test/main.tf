terraform {
    required_providers {
        null = {
            source = "hashicorp/null"
            version = "3.1.0"
        }
    }
}

provider "null" {}

resource "null_resource" "example" {
    triggers = {
        timestamp = timestamp()
    }

    provisioner "local-exec" {
        command = "echo Hello, Terraform!"
    }
}
