# GhostDrive 👻🚗

**GhostDrive** is a surgical CLI tool for Ubuntu Linux designed to find and exterminate forgotten, bloated environments and hidden cache files that are haunting your storage.

## Why GhostDrive?
As developers, we often leave behind GBs of "ghost" data—old virtual environments, Conda packages, and build artifacts—that we no longer use. GhostDrive scans your system, profiles the disk usage of these folders, and lets you safely prune them with a single command.

## Features
- **Profile-Based Scanning:** Automatically detects Standard Python venvs and Conda environments.
- **Ubuntu Optimized:** Tailored for Linux directory structures and permission handling.
- **Deep Size Analysis:** Accurately calculates the total footprint of nested environment directories.
- **Dry Run Mode:** See what *would* be deleted without touching a single byte.
- **Safety First:** Built-in `Ctrl+C` handling and `/exit` commands for a graceful exit.
- **Secure Deletion:** Uses system-level authorization for clean, permanent removal.

## Installation
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/ghostdrive.git](https://github.com/yourusername/ghostdrive.git)
   cd ghostdrive
