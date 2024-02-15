#!/usr/bin/env python3
import os
import inquirer
import subprocess
import requests
import json
import tarfile

import globals
import utils

def create_nocode_module(config_location, provider_name, module_version):
    provider_name = utils.validate_terraform_folder(config_location)
    module_name = os.path.basename(config_location)
    payload = {
        "data": {
            "type": "registry-modules",
            "attributes": {
                "name": f"{module_name}",
                "provider": f"{provider_name}",
                "registry-name": "private",
                "no-code": True
            }
        }
    }

    url = f"{globals.BASE_URL}/registry-modules"
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {globals.TFC_API_TOKEN}"
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("Module created successfully!")
        create_nocode_module_version(module_name, provider_name, module_version)
    else:
        print(f"POST request failed for creating module with status code: {response.status_code}")
        print(response.json())
        exit(1)


def create_nocode_module_version(module_name, provider_name, module_version):
    payload = {
        "data": {
            "type": "registry-modules-versions",
            "attributes": {
                "version": f"{module_version}"
            }
        }
    }

    url = f"{globals.BASE_URL}/registry-modules/private/{globals.TFC_ORG}/{module_name}/{provider_name}/versions"
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {globals.TFC_API_TOKEN}"
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("Module version created successfully!")
        response_json = response.json()
        try:
            upload_link = response_json['data']['links']['upload']
            upload_nocode_module(config_kind, upload_link)
        except (KeyError, TypeError):
            print("Failed to retrieve the upload link in the response")
            exit(1)
    else:
        print(f"POST request failed for creating module version with status code: {response.status_code}")
        print(response.json())
        exit(1)

def upload_nocode_module(config_path, upload_link):
    utils.create_tar_gz(config_path)
    headers = {
        "Content-Type": "application/octet-stream",
        "Authorization": f"Bearer {globals.TFC_API_TOKEN}"
    }
    with open(globals.ARCHIVE_NAME, "rb") as file:
        response = requests.put(upload_link, data=file, headers=headers)

    if response.status_code == 200:
        try:
            os.remove(globals.ARCHIVE_NAME)
            print(f"File '{globals.ARCHIVE_NAME}' deleted successfully!")
        except OSError as e:
            print(f"Error deleting file '{globals.ARCHIVE_NAME}': {e}")
        print("No-code module created successfully!")
    else:
        print(f"PUT request failed for uploading module with status code: {response.status_code}")
        print(response.json())
        exit(1)

def create_nocode_module_with_repo(config_repo_url):
    repo_name = utils.validate_github_repo(config_repo_url)
    #TODO: get oauth token id or github app installation id
    payload = {
        "data": {
            "type": "registry-modules",
            "attributes": {
                "vcs-repo": {
                    "identifier":f"{repo_name}",
                    "oauth-token-id":"ot-hmAyP66qk2AMVdbJ",
                    "display_identifier":f"{repo_name}"
                },
            "no-code": true
            }
        }
    }
