#!/usr/bin/env python3
import os
import inquirer
import subprocess
import requests
import json

import globals
import registry
import configure
import github
import folder
import delete

def main():
    """
    This function is the entry point of the program.
    It prompts the user to select the kind of Terraform to onboard as a no-code module,
    and performs the corresponding actions based on the user's choice.
    """

    onboard_kind_question = [
        inquirer.List('onboard_kind',
                    message="What would you like to do?",
                    choices=['Onboard Terraform no-code module', 'Configure Terraform no-code module', 'Delete Terraform no-code module'],
                ),
    ]
    onboard_kind_answer = inquirer.prompt(onboard_kind_question)["onboard_kind"]

    # ask for the module options
    if onboard_kind_answer == 'Onboard Terraform no-code module':

        # ask for the location of the config, and create the no-code module
        config_kind_question = [
            inquirer.List('config_kind',
                        message="Where is your Terraform config?",
                        choices=['Local folder', 'GitHub repository', 'Terraform public registry'],
                        default=os.getcwd()
                    ),
        ]
        config_kind = inquirer.prompt(config_kind_question)["config_kind"]

        # ask for the folder path of the config
        if config_kind == 'Local folder':
            config_location_question = [
                inquirer.Text('config_location',
                            message="Please enter the path to your Terraform config folder",
                            default=f"{os.getcwd()}/terraform-null-test"
                        ),
            ]
            config_location = inquirer.prompt(config_location_question)["config_location"]
            print(f"Uploading Terraform at: {config_location} and using it as the no-code module name.")
            folder.create_nocode_module(config_location, "0.0.1")

        # ask for the URL of the GitHub repository
        elif config_kind == 'GitHub repository':
            config_location_question = [
                inquirer.Text('config_location',
                            message="Please enter the URL of your GitHub repository"
                        ),
            ]
            config_location = inquirer.prompt(config_location_question)["config_location"]
            print(f"Uploading Terraform at: {config_location}")
            github.create_nocode_module(config_location, "0.0.1")

        # ask for the URL of the Terraform module
        elif config_kind == 'Terraform public registry':
            config_location_question = [
                inquirer.Text('config_location',
                            message="Please enter the URL of the public Terraform registry \n (e.g. https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest)"
                        ),
            ]
            config_location = inquirer.prompt(config_location_question)["config_location"]
            print(f"Uploading Terraform at: {config_location}")
            registry.create_nocode_module(config_location)

    elif onboard_kind_answer == 'Configure Terraform no-code module':

        # ask for the name of the module to configure
        configure_name_question = [
            inquirer.Text('configure_name',
                        message="What is the name of the module to configure?",
                    ),
        ]
        configure_name_answer = inquirer.prompt(configure_name_question)["configure_name"]

        # ask for the module options
        configure_provider_question = [
            inquirer.Text('configure_provider',
                        message="What is the name of provider for the module?",
                    ),
        ]
        configure_provider_answer = inquirer.prompt(configure_provider_question)["configure_provider"]
        configure.configure_nocode_module(configure_name_answer, configure_provider_answer)

    elif onboard_kind_answer == 'Delete Terraform no-code module':

        # ask for the name of the module to delete
        delete_name_question = [
            inquirer.Text('delete_name',
                        message="What is the name of the module to delete?",
                    ),
        ]
        delete_name_answer = inquirer.prompt(delete_name_question)["delete_name"]
        print(f"Deleting {delete_name_answer} module...")
        delete.delete_nocode_module(delete_name_answer)

    print("Goodbye!")

if __name__ == "__main__":
    main()
