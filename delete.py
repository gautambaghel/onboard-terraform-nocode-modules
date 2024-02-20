#!/usr/bin/env python3
import requests
import json
import globals

def delete_nocode_module(name):
    url = f"{globals.BASE_URL}/registry-modules/private/{globals.TFC_ORG}/{name}"
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {globals.TFC_API_TOKEN}"
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print("No-code module deleted successfully!")
    else:
        print(f"PUT request failed for uploading module with status code: {response.status_code}")
        print(json.dumps(response.json(), indent=4))
        exit(1)
