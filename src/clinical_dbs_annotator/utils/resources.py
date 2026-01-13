"""
Resource path management utilities.

This module provides functions for locating resources (icons, styles, etc.)
whether running from source or as a PyInstaller bundle.
"""

import os
import sys


def resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a resource file.

    This function works both when running from source and when running
    as a PyInstaller bundle. PyInstaller creates a temp folder and stores
    path in _MEIPASS.

    Args:
        relative_path: Relative path to the resource file

    Returns:
        Absolute path to the resource file
    """
    if hasattr(sys, "_MEIPASS"):
        # Running as PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    # Running from source
    return os.path.join(os.path.abspath("."), relative_path)
