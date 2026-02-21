import os
import json

VAULT_DIR = "public/vault"
OUTPUT_FILE = "public/files.json"

def get_file_tree(path, base_path):
    tree = []
    try:
        for entry in os.scandir(path):
            if entry.name.startswith('.'):
                continue
                
            # Create relative path from the perspective of the 'public' directory
            # For app.js to use: fetch('vault/...')
            rel_path = os.path.relpath(entry.path, "public").replace(os.sep, '/')
            
            item = {
                "name": entry.name,
                "path": rel_path,
                "isDir": entry.is_dir()
            }
            
            if entry.is_dir():
                item["children"] = get_file_tree(entry.path, base_path)
            
            # Only include supported files or directories
            if entry.is_dir() or entry.name.lower().endswith(('.md', '.pdf')):
                tree.append(item)
    except Exception as e:
        print(f"Error scanning {path}: {e}")
        
    return sorted(tree, key=lambda x: (not x["isDir"], x["name"].lower()))

if __name__ == "__main__":
    print(f"Generating manifest from: {VAULT_DIR}")
    if os.path.exists(VAULT_DIR):
        files_tree = get_file_tree(VAULT_DIR, VAULT_DIR)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(files_tree, f, indent=2, ensure_ascii=False)
        print(f"Manifest saved to: {OUTPUT_FILE}")
    else:
        print(f"Error: {VAULT_DIR} not found.")
