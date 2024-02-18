#!/usr/bin/env python3
import os
import re
import tarfile

import globals

def validate_terraform_folder(folder_name):
    match = re.match(r'^terraform-([^/]+)-([^/]+)', folder_name)
    if match:
        # Split folder_name with the value of the first two dashes
        split_folder_name = folder_name.split('-', 2)
        return split_folder_name[1]
    else:
        print("Invalid folder name format. Folder name should have the pattern 'terraform-provider-*'.")
        exit(1)


def validate_github_repo(repo_url):
    # Extract the organization and repository name from the URL
    match = re.match(r'^https?://github.com/([^/]+)/([^/]+)', repo_url)
    if match:
        org_name = match.group(1)
        repo_name = match.group(2)
        return f"{org_name}/{repo_name}"
    else:
        print("Invalid GitHub repository URL.")
        exit(1)

# Create a tar.gz file from the given folder path
def create_tar_gz(folder_path):
    with tarfile.open(globals.ARCHIVE_NAME, "w:gz") as tar:
        tar.add(folder_path, arcname=os.path.basename(folder_path))
    print(f"Created tar.gz file: {globals.ARCHIVE_NAME}!")
