import hashlib
import os
import json
from datetime import datetime

HASH_DB = "file_hashes.json"

def get_file_hash(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def scan_folder(folder_path):
    hashes = {}
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            hashes[filepath] = get_file_hash(filepath)
    return hashes

def save_baseline(folder_path):
    print(f"\n[*] Scanning folder: {folder_path}")
    hashes = scan_folder(folder_path)
    
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "folder": folder_path,
        "hashes": hashes
    }
    
    with open(HASH_DB, "w") as f:
        json.dump(data, f, indent=4)
    
    print(f"[+] Baseline saved! {len(hashes)} files recorded.")
    print(f"[+] Saved to: {HASH_DB}")

def check_integrity(folder_path):
    if not os.path.exists(HASH_DB):
        print("[!] No baseline found. Run with --baseline first.")
        return
    
    with open(HASH_DB, "r") as f:
        data = json.load(f)
    
    print(f"\n[*] Checking integrity against baseline from: {data['timestamp']}")
    baseline = data["hashes"]
    current = scan_folder(folder_path)
    
    modified = []
    new_files = []
    deleted = []
    
    for filepath, curr_hash in current.items():
        if filepath not in baseline:
            new_files.append(filepath)
        elif baseline[filepath] != curr_hash:
            modified.append(filepath)
    
    for filepath in baseline:
        if filepath not in current:
            deleted.append(filepath)
    
    print("\n" + "="*50)
    if not modified and not new_files and not deleted:
        print("[✓] ALL FILES INTACT — No changes detected.")
    else:
        if modified:
            print(f"\n[!] MODIFIED FILES ({len(modified)}):")
            for f in modified:
                print(f"    → {f}")
        if new_files:
            print(f"\n[+] NEW FILES ({len(new_files)}):")
            for f in new_files:
                print(f"    → {f}")
        if deleted:
            print(f"\n[-] DELETED FILES ({len(deleted)}):")
            for f in deleted:
                print(f"    → {f}")
    print("="*50)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("\nUsage:")
        print("  python file_integrity.py --baseline <folder>")
        print("  python file_integrity.py --check <folder>")
        sys.exit(1)
    
    mode = sys.argv[1]
    folder = sys.argv[2]
    
    if mode == "--baseline":
        save_baseline(folder)
    elif mode == "--check":
        check_integrity(folder)
    else:
        print("[!] Invalid option. Use --baseline or --check")
