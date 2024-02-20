#!/usr/bin/env python3
import json
import requests

import globals

def configure_nocode_module(no_code_module_name, no_code_provider_name):
    no_code_id = get_id_from_name(no_code_module_name, no_code_provider_name)
    get_no_code_module(no_code_id)
    # headers = {
    #     "Content-Type": "application/vnd.api+json",
    #     "Authorization": f"Bearer {globals.TFC_API_TOKEN}"
    # }
    # payload = {
    #     "data": {
    #         "type": "no-code-modules",
    #         "attributes": {
    #             "enabled": True
    #         },
    #         "relationships": {
    #             "variable-options": {
    #                 "data": [
    #                 {
    #                     "id": "ncvaropt-fcHDfnZ1EGdRzFNC",
    #                     "type": "variable-options",
    #                     "attributes": {
    #                     "variable-name": "Linux AMIs",
    #                     "variable-type": "array",
    #                     "options": [
    #                         "Xenial Xerus",
    #                         "Trusty Tahr"
    #                     ]
    #                     }
    #                 },
    #                 ]
    #             }
    #         }
    #     }
    # }
    # url = f"{globals.BASE_URL}/no-code-modules/{no_code_id}"
    # response = requests.patch(url, json=payload, headers=headers)

    # if response.status_code == 201:
    #     print("Module created successfully!")
    # else:
    #     print(f"POST request failed for creating module with status code: {response.status_code}")
    #     print(response.json())
    #     exit(1)

def get_id_from_name(no_code_module_name, no_code_provider_name):
    url = f"{globals.BASE_URL}/registry-modules/private/{globals.TFC_ORG}/{no_code_module_name}/{no_code_provider_name}"
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {globals.TFC_API_TOKEN}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            return response.json()["data"]["relationships"]["no-code-modules"]["data"][0]["id"]
        except (KeyError, TypeError):
            print(f"Error occurred while getting id from the nocode module name: {json.dumps(response.json(), indent=4)}")
            exit(1)
    else:
        print(f"POST request failed for creating module with status code: {response.status_code}")
        print(json.dumps(response.json(), indent=4))
        exit(1)

def get_no_code_module(no_code_id):
    url = f"{globals.TFC_URL}/api/v2/no-code-modules/{no_code_id}?include=variable_options"
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {globals.TFC_API_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    print(json.dumps(response.json(), indent=4))
    variable_options = {}
    if response.status_code == 200:
        if len(response.json()["data"]["relationships"]["variable-options"]["data"]) == 0:
            print(f"No variable options found for the no-code module with id: {no_code_id}")
            exit(0)
        try:
            for var in response.json()["data"]["relationships"]["variable-options"]["data"]:
                variable_options[f"{var['attributes']['variable-name']}"] = var
            print(f"Variable options: {variable_options}")
        except (KeyError, TypeError):
            print(f"Error occurred while getting variable options: {json.dumps(response.json(), indent=4)}")
            exit(1)
    else:
        print(f"Error reading the nocode module with id: {no_code_id}, status code: {response.status_code}")
        print(json.dumps(response.json(), indent=4))
        exit(1)
