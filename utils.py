#!/usr/bin/env python3
import os
import re

def validate_terraform_folder(name):
    if not re.match(r'^terraform-.*-.*$', folder_name):
        print("Invalid folder name format. Folder name should have the pattern 'terraform-provider-*'.")
        exit(1)

    # Split folder_name with the value of the first two dashes
    split_folder_name = folder_name.split('-', 2)
    return split_folder_name[1]

def validate_github_repo(repo_url):
    #TODO: return the repo name
    if not re.match(r'^https?://github.com/.*$', repo_url):
        print("Invalid GitHub repository URL.")
        exit(1)

# Create a tar.gz file from the given folder path
def create_tar_gz(folder_path):
    with tarfile.open(globals.ARCHIVE_NAME, "w:gz") as tar:
        tar.add(folder_path, arcname=os.path.basename(folder_path))
    print(f"Created tar.gz file: {globals.ARCHIVE_NAME}!")
