import os
import json
import urllib.parse
import subprocess

GITHUB_USER = "SickDuck696969"
REPO_NAME = "ROM-Collection"
BRANCH = "master"

manifest = []
VALID_EXTENSIONS = {".zip", ".7z", ".nes", ".sfc", ".gba", ".n64", ".z64", ".bin", ".gb", ".gbc", ".epub", ".pdf", ".mp3"}

# Ask Git directly for the repository structure instead of scanning the hard drive
result = subprocess.run(['git', 'ls-tree', '-r', '--name-only', 'HEAD'], capture_output=True, text=True)
all_files = result.stdout.splitlines()

# Group files by their parent folder
folders = {}

for file_path in all_files:
    # Skip files in the root directory (like generate_manifest.py, manifest.json)
    if "/" not in file_path:
        continue
        
    parts = file_path.split("/")
    folder_name = parts[0]
    file_name = parts[-1]
    
    # Ignore hidden GitHub/Git folders
    if folder_name in {".git", ".github", "node_modules"}:
        continue
        
    if folder_name not in folders:
        folders[folder_name] = []
        
    # Check if the file is a valid ROM extension
    if any(file_name.lower().endswith(ext) for ext in VALID_EXTENSIONS):
        folders[folder_name].append(file_path)

# Build the manifest dictionary
for folder_name, files in folders.items():
    if not files:
        # If the folder has no ROMs, add a dummy entry so the app sees the console
        manifest.append({
            "name": ".empty",
            "console": folder_name,
            "downloadUrl": ""
        })
    else:
        for file_path in files:
            file_name = os.path.basename(file_path)
            
            # Safely encode the path for the web
            encoded_path = urllib.parse.quote(file_path, safe='/')
            download_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{encoded_path}"
            
            manifest.append({
                "name": file_name,
                "console": folder_name,
                "downloadUrl": download_url
            })

# Sort alphabetically by Console, then by Game Name
manifest.sort(key=lambda x: (x["console"].lower(), x["name"].lower()))

# Save the JSON file
with open("manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)
