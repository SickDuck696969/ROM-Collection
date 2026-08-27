import os
import json
import urllib.parse

GITHUB_USER = "SickDuck696969"
REPO_NAME = "ROM-Collection"
BRANCH = "master"

manifest = []
EXCLUDED_DIRS = {".git", ".github", "node_modules"}
VALID_EXTENSIONS = {".zip", ".7z", ".nes", ".sfc", ".gba", ".n64", ".z64", ".bin"}

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
    folder_name = os.path.basename(root)
    
    if root == ".":
        continue

    folder_has_roms = False

    for file in files:
        if any(file.lower().endswith(ext) for ext in VALID_EXTENSIONS):
            folder_has_roms = True
            rel_path = os.path.relpath(os.path.join(root, file), ".").replace("\\", "/")
            encoded_path = urllib.parse.quote(rel_path, safe='/')
            download_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{encoded_path}"
            
            manifest.append({
                "name": file,
                "console": folder_name,
                "downloadUrl": download_url
            })
    
    # If the folder has no ROMs, add a dummy entry so the app sees the console
    if not folder_has_roms:
        manifest.append({
            "name": ".empty",
            "console": folder_name,
            "downloadUrl": ""
        })

manifest.sort(key=lambda x: (x["console"].lower(), x["name"].lower()))

with open("manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)