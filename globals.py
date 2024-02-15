#!/usr/bin/env python3
import os
import inquirer
import subprocess
import json

TFC_URL = "https://app.terraform.io"
TFC_ORG = "tfc-integration-sandbox"
TFC_API_TOKEN = ""
TFC_CREDS_PATH = os.path.abspath(os.path.expanduser("~/.terraform.d/credentials.tfrc.json"))

BASE_URL = f"{TFC_URL}/api/v2/organizations/{TFC_ORG}"
ARCHIVE_NAME = "archive.tar.gz"

# Read the Terraform credentials file
with open(TFC_CREDS_PATH) as file:
    data = json.load(file)

# Search for the TFC URL in the credentials file, prompt if not found
host = TFC_URL.strip("https://")
try:
    TFC_API_TOKEN = data["credentials"][host]["token"]
except (KeyError, TypeError):
    tfc_token_question = [
        inquirer.Text('tfc_token_question',
                    message="Terraform Cloud API token not found, please enter it",
                ),
    ]
    tfc_token_answer = inquirer.prompt(tfc_token_question)
    TFC_API_TOKEN = tfc_token_answer['tfc_token_question']
