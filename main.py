#!/usr/bin/env python3
import os
import inquirer
import subprocess
import requests
import json
import tarfile

import globals
import create
import delete

def main():
    """
    This function is the entry point of the program.
    It prompts the user to select the kind of Terraform to onboard as a no-code module,
    and performs the corresponding actions based on the user's choice.
    """

    # Ask kind of Terraform to onboard
    onboard_kind_question = [
        inquirer.List('onboard_kind',
                    message="Which kind of Terraform would you like to onboard as a no-code module?",
                    choices=['Terraform config', 'Terraform module', 'Delete no-code module'],
                ),
    ]
    onboard_kind_answer = inquirer.prompt(onboard_kind_question)["onboard_kind"]

    # ask for the name of the module or config
    if onboard_kind_answer == 'Terraform module':
        module_name_question = [
            inquirer.Text('module_name',
                        message="What is the name of the module?",
                    ),
        ]
        module_name_answer = inquirer.prompt(module_name_question)["module_name"]
        print(module_name_answer)

    elif onboard_kind_answer == 'Terraform config':

        # ask for the location of the config, and create the no-code module
        config_kind_question = [
            inquirer.List('config_kind',
                        message="Where is your Terraform config?",
                        choices=['Local folder', 'GitHub repository'],
                        default=os.getcwd()
                    ),
        ]
        config_kind = inquirer.prompt(config_kind_question)["config_kind"]

        # ask for the folder path of the config
        if config_kind == 'Local folder':
            config_location_question = [
                inquirer.Text('config_location',
                            message="Please enter the path to your Terraform config folder",
                            default=os.getcwd()
                        ),
            ]
            config_location = inquirer.prompt(config_location_question)["config_location"]
            print(f"Uploading Terraform at: {config_location} and using it as the no-code module name.")
            create.create_nocode_module(config_location, "0.0.1")

        # ask for the URL of the GitHub repository
        elif config_kind == 'GitHub repository':
            config_location_question = [
                inquirer.Text('config_location',
                            message="Please enter the URL of your GitHub repository",
                            default=os.getcwd()
                        ),
            ]
            config_location = inquirer.prompt(config_location_question)["config_location"]
            print(f"Uploading Terraform at: {config_location}")
            create.create_nocode_module_with_repo(config_location)

    elif onboard_kind_answer == 'Delete no-code module':

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
