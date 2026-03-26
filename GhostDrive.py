import os
import sys
import time
import math
import argparse
import subprocess
import threading
import signal
from pathlib import Path
from datetime import datetime

# --- Configuration Profiles ---
# Easily extensible: Add new markers here to find other "ghost" files.
TARGET_PROFILES = {
    "python_venv": {"marker": "activate", "parent_offset": 1, "desc": "Python VirtualEnv"},
    "conda_env": {"marker": "conda-meta", "parent_offset": 0, "desc": "Conda Environment"},
}

# --- Global Exit Handler ---
def signal_handler(sig, frame):
    print("\n\n👻 GhostDrive interrupted. Staying spooky... Goodbye!")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

done_searching = False

def animate_searching():
    chars = ["|", "/", "-", "\\"]
    idx = 0
    while not done_searching:
        sys.stdout.write(f"\r🔍 GhostDrive is scanning (Ubuntu)... {chars[idx % len(chars)]} ")
        sys.stdout.flush()
        time.sleep(0.1)
        idx += 1
    sys.stdout.write("\r" + " " * 50 + "\r")

def get_dir_size(path):
    total = 0
    try:
        with os.scandir(path) as it:
            for entry in it:
                try:
                    if entry.is_file(follow_symlinks=False):
                        total += entry.stat().st_size
                    elif entry.is_dir(follow_symlinks=False):
                        total += get_dir_size(entry.path)
                except (PermissionError, OSError):
                    continue
    except (PermissionError, OSError):
        pass
    return total

def format_size(size_bytes):
    if size_bytes <= 0: return "0 B"
    units = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    return f"{round(size_bytes / (1024**i), 2)} {units[i]}"

def find_targets(root_path):
    found_items = []
    for root, dirs, files in os.walk(root_path):
        for profile_name, config in TARGET_PROFILES.items():
            marker = config["marker"]
            if marker in files or marker in dirs:
                if profile_name == "python_venv" and not root.endswith('bin'):
                    continue

                target_path = Path(root)
                for _ in range(config["parent_offset"]):
                    target_path = target_path.parent

                try:
                    marker_path = Path(root) / marker
                    stats = marker_path.stat()
                    size = get_dir_size(target_path)
                    last_mod = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d')

                    found_items.append({
                        "path": target_path,
                        "size": size,
                        "date": last_mod,
                        "type": config["desc"]
                    })
                except (PermissionError, OSError):
                    continue
    return found_items

def main():
    global done_searching
    parser = argparse.ArgumentParser(description="GhostDrive: Ubuntu-optimized environment scanner.")
    parser.add_argument("path", nargs="?", default="/", help="Start path")
    parser.add_argument("--dry-run", action="store_true", help="Simulate deletion")
    args = parser.parse_args()

    print(f"--- GhostDrive v1.1 (Ubuntu Optimized) ---")
    if args.dry_run: print("🛠  MODE: DRY RUN ACTIVE")

    t = threading.Thread(target=animate_searching, daemon=True)
    t.start()

    try:
        results = find_targets(args.path)
    finally:
        done_searching = True
        t.join()

    if not results:
        print("\n👻 No environments found. Run with 'sudo' for a full system scan.")
        return

    results.sort(key=lambda x: x['size'], reverse=True)

    print(f"\n{'ID':<4} | {'TYPE':<15} | {'PATH':<45} | {'SIZE':<10}")
    print("-" * 95)
    for i, item in enumerate(results):
        print(f"[{i}]".ljust(4) + f" | {item['type']:<15} | {str(item['path'])[:45]:<45} | {format_size(item['size']):<10}")

    print("-" * 95)
    print(f"TOTAL RECOVERABLE SPACE: {format_size(sum(r['size'] for r in results))}")
    print("-" * 95)

    try:
        user_input = input("\nEnter ID to DELETE (or type '/exit' to quit): ").strip().lower()

        if not user_input or user_input == "/exit":
            print("Exiting GhostDrive. Stay clean!")
            return

        idx = int(user_input)
        target = results[idx]

        # --- HARSH DELETE WARNING ---
        print(f"\n" + "!"*60)
        print(f"CRITICAL WARNING: PERMANENT DELETION")
        print(f"Target: {target['path']}")
        print(f"Size  : {format_size(target['size'])}")
        print(f"\nThis action CANNOT BE UNDONE. This environment will be")
        print(f"permanently erased from your drive. Backups are not enabled.")
        print("!"*60)

        confirm = input("\nType 'YES' (all caps) to confirm permanent deletion: ")

        if confirm == 'YES':
            if args.dry_run:
                print(f"\n🛠  [DRY RUN] Would have executed: sudo rm -rf {target['path']}")
            else:
                print("\n🔐 Requesting system privileges for removal...")
                subprocess.run(["sudo", "rm", "-rf", str(target['path'])])
                print(f"✅ Exterminated. {format_size(target['size'])} recovered.")
        else:
            print("\nSafe choice! Deletion aborted.")

    except (ValueError, IndexError):
        print("\nInvalid selection. GhostDrive is shutting down.")

if __name__ == "__main__":
    main()
