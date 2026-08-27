import os
import json

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
            rel_path = os.path.relpath(os.path.join(root, file), ".").replace("\\", "/")
            download_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{rel_path}"
            
            manifest.append({
                "name": file,
                "console": folder_name,
                "downloadUrl": download_url
            })

# Sort the manifest entries alphabetically by file name (case-insensitive)
manifest.sort(key=lambda x: (x["console"].lower(), x["name"].lower()))

with open("manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print(f"Successfully generated manifest.json with {len(manifest)} sorted items.")