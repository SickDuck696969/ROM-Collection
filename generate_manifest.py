import os
import json
import urllib.parse # <-- Added this to fix URL spaces

# Replace with your GitHub details
GITHUB_USER = "SickDuck696969"
REPO_NAME = "ROM-Collection"
BRANCH = "master"

manifest = []

# Exclude system folders
EXCLUDED_DIRS = {".git", ".github", "node_modules"}
VALID_EXTENSIONS = {".zip", ".7z", ".nes", ".sfc", ".gba", ".n64", ".z64", ".bin"}

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
    folder_name = os.path.basename(root)
    
    # Skip the repository root directory
    if root == ".":
        continue

    for file in files:
        if any(file.lower().endswith(ext) for ext in VALID_EXTENSIONS):
            # 1. Get the relative path
            rel_path = os.path.relpath(os.path.join(root, file), ".").replace("\\", "/")
            
            # 2. URL-Encode the path (converts spaces to %20) but leaves the / slashes alone
            encoded_path = urllib.parse.quote(rel_path, safe='/')
            
            # 3. Build the final safe URL
            download_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{encoded_path}"
            
            manifest.append({
                "name": file,
                "console": folder_name,
                "downloadUrl": download_url
            })

# Sorts by Console folder first, then alphabetically by Game Name
manifest.sort(key=lambda x: (x["console"].lower(), x["name"].lower()))

with open("manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print(f"Successfully generated manifest.json with {len(manifest)} sorted items.")