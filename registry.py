#!/usr/bin/env python3
import os
import inquirer
import subprocess
import requests
import json

import globals
import utils

def create_nocode_module(registry_repo_url):
    module_name, module_namespace, provider_name = get_attributes_from_registry(registry_repo_url)
    print(f"Creating no-code module with name: {module_name}, namespace: {module_namespace}, and provider: {provider_name}")
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {globals.TFC_API_TOKEN}"
    }
    payload = {
        "data": {
            "type": "registry-modules",
            "attributes": {
                "name": f"{module_name}",
                "namespace": f"{module_namespace}",
                "provider": f"{provider_name}",
                "registry-name": "public",
                "no-code": True
            }
        }
    }
    url = f"{globals.BASE_URL}/registry-modules"
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("Module created successfully!")
    else:
        print(f"POST request failed for creating module with status code: {response.status_code}")
        print(json.dumps(response.json(), indent=4))
        exit(1)

def get_attributes_from_registry(registry_repo_url):
    try:
        return registry_repo_url.split("/")[-3], registry_repo_url.split("/")[-4], registry_repo_url.split("/")[-2]
    except Exception as e:
        print(f"Error occurred while splitting Terraform registry URL: {e}")
        exit(1)
