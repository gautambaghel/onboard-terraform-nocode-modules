#!/usr/bin/env python3
import inquirer
import subprocess
import requests
import json

import globals
import utils

# This function is to create a no-code module with a repository
def create_nocode_module(config_repo_url, module_version):
    repo_name = utils.validate_github_repo(config_repo_url)
    oauth_token = get_oauth_token()
    branch_name = get_branch_name()
    print(f"Creating no-code module with repository: {repo_name} and branch: {branch_name}")
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {globals.TFC_API_TOKEN}"
    }
    payload = {
        "data": {
            "type": "registry-modules",
            "attributes": {
                "vcs-repo": {
                    "identifier": f"{repo_name}",
                    "display-identifier": f"{repo_name}",
                    "oauth-token-id": f"{oauth_token}",
                    "branch": f"{branch_name}",
                    "tags": False
                },
            "no-code": True,
            "initial-version": f"{module_version}",
            "publishing-mechanism": "branch",
            "registry-name": "private"
            }
        }
    }
    url = f"{globals.BASE_URL}/registry-modules/vcs"
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("VCS module created successfully!")
    else:
        print(f"POST request failed for creating module version")
        print(response.json())
        exit(1)

# This function asks for the branch name to use
def get_branch_name():
    branch_name_question = [
        inquirer.Text('branch_name',
                    message="Which git branch to use?",
                    default="main"
                ),
    ]
    branch_name = inquirer.prompt(branch_name_question)["branch_name"]
    return branch_name

# This function returns the OAuth clients for the user.
def get_oauth_token():
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {globals.TFC_API_TOKEN}"
    }
    url = f"{globals.BASE_URL}/oauth-clients"
    response = requests.get(url, headers=headers)
    response_json = response.json()

    try:
        oauth_client = response_json.get('data')

        if oauth_client is None or len(oauth_client) == 0:
            print("No OAuth clients found, please configure Terraform Cloud with GitHub or GitLab")
        elif len(oauth_client) == 1:
            oauth_token = response_json.get('data')[0].get('relationships').get('oauth-tokens').get('data')[0].get('id')
            return oauth_token
        else:
            oauth_identities = {}
            for client in oauth_client:
                oauth_identities[f"{client['attributes']['service-provider-display-name']} [{client['attributes']['http-url']}]"] = client['relationships']['oauth-tokens']['data'][0]['id']

            # ask for the OAuth client to use
            oauth_question = [
                inquirer.List('oauth_question',
                            message="Which oauth connection to use?",
                            choices=oauth_identities.keys()
                        ),
            ]
            oauth_token = oauth_identities[inquirer.prompt(oauth_question)["oauth_question"]]
            return oauth_token
    except (KeyError, TypeError):
        print("Failed to parse the response for OAuth clients")
        exit(1)
