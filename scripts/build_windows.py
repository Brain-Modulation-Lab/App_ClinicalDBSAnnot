"""
Build script for Windows executable using PyInstaller.

This script builds a standalone Windows executable with all necessary resources.
"""

import os
import subprocess
import sys
from pathlib import Path

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"
ICONS_DIR = PROJECT_ROOT / "icons"
SRC_DIR = PROJECT_ROOT / "src"

APP_NAME = "ClinicalDBSAnnot"
VERSION = "v0.1"


def build_windows_exe():
    """Build Windows executable using PyInstaller."""
    print(f"Building {APP_NAME} {VERSION} for Windows...")

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single file executable
        "--noconsole",  # No console window
        f"--name={APP_NAME}_{VERSION.replace('.', '_')}",
        f"--icon={ICONS_DIR / 'logobml.ico'}",
        # Add data files
        f"--add-data={ICONS_DIR / 'logobml.ico'};icons",
        f"--add-data={ICONS_DIR / 'logobml.png'};icons",
        f"--add-data={PROJECT_ROOT / 'style.qss'};.",
        # Collect all PyQt5 plugins
        "--collect-all=PyQt5",
        # Entry point
        f"{SRC_DIR / 'clinical_dbs_annotator' / '__main__.py'}",
    ]

    # Run PyInstaller
    try:
        subprocess.run(cmd, check=True, cwd=PROJECT_ROOT)
        print(f"\n✓ Build successful!")
        print(f"  Executable location: {DIST_DIR / f'{APP_NAME}_{VERSION.replace('.', '_')}.exe'}")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed: {e}")
        return False

    return True


def main():
    """Main entry point."""
    if not (ICONS_DIR / "logobml.ico").exists():
        print(f"Error: Icon file not found at {ICONS_DIR / 'logobml.ico'}")
        return 1

    if not (ICONS_DIR / "logobml.png").exists():
        print(f"Error: Logo file not found at {ICONS_DIR / 'logobml.png'}")
        return 1

    if not build_windows_exe():
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
