import os
import json
import urllib.parse
import subprocess

GITHUB_USER = "SickDuck696969"
REPO_NAME = "ROM-Collection"
BRANCH = "master"

manifest = []
VALID_EXTENSIONS = {".zip", ".7z", ".nes", ".sfc", ".gba", ".n64", ".z64", ".bin", ".gb", ".gbc", ".epub", ".pdf", ".mp3", ".jar"}

# Ask Git directly for the repository structure
result = subprocess.run(['git', 'ls-tree', '-r', '--name-only', 'HEAD'], capture_output=True, text=True)
all_files = result.stdout.splitlines()

# Group files by their parent folder
folders = {}

for file_path in all_files:
    if "/" not in file_path:
        continue
        
    parts = file_path.split("/")
    folder_name = parts[0]
    file_name = parts[-1]
    
    if folder_name in {".git", ".github", "node_modules"}:
        continue
        
    if folder_name not in folders:
        folders[folder_name] = []
        
    if any(file_name.lower().endswith(ext) for ext in VALID_EXTENSIONS):
        folders[folder_name].append(file_path)

# Build the manifest dictionary
for folder_name, files in folders.items():
    if not files:
        manifest.append({
            "name": ".empty",
            "console": folder_name,
            "downloadUrl": ""
        })
    else:
        for file_path in files:
            file_name = os.path.basename(file_path)
            encoded_path = urllib.parse.quote(file_path, safe='/')
            
            # Check if this file is tracked by Git LFS
            attr_check = subprocess.run(['git', 'check-attr', 'filter', '--', file_path], capture_output=True, text=True)
            is_lfs = "lfs" in attr_check.stdout.split()

            # Select URL host based on LFS status
            if is_lfs:
                download_url = f"https://media.githubusercontent.com/media/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{encoded_path}"
            else:
                download_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{encoded_path}"
            
            manifest.append({
                "name": file_name,
                "console": folder_name,
                "downloadUrl": download_url
            })

manifest.sort(key=lambda x: (x["console"].lower(), x["name"].lower()))

with open("manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print("manifest.json successfully generated!")