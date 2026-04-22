"""Per-user data locations for config and presets.

All user-owned runtime files (config JSON, preset overrides, cached state) MUST
resolve under :func:`user_data_dir` so they survive reinstalls and in-place
upgrades on every platform. The install directory (Windows ``Program Files`` /
``%LOCALAPPDATA%\\Programs\\...``, the macOS ``.app`` bundle, the Linux
``/opt`` or ``/usr`` prefix) is wiped or replaced by every MSI / DMG / dpkg
upgrade and must never hold user data.

The path is derived from Qt's :class:`QStandardPaths` so it follows platform
conventions. Organization and application directory names are set in
``dbs_annotator.config`` as ``FS_ORG_NAME`` / ``FS_APP_NAME`` (ASCII, no spaces)
and applied in ``__main__`` via ``QApplication``:

* Windows: ``%LOCALAPPDATA%\\WyssGeneva\\DBSAnnotator``
* macOS:   ``~/Library/Application Support/WyssGeneva/DBSAnnotator``
* Linux:   ``~/.local/share/WyssGeneva/DBSAnnotator``
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QStandardPaths


def user_data_dir() -> Path:
    """Return the platform-appropriate per-user data directory for the app.

    The directory is created if it does not yet exist. If Qt cannot determine a
    writable location (e.g. headless CI without a home directory), the caller
    gets a sensible fallback under ``~/.dbs-annotator``.
    """
    location = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.AppLocalDataLocation
    )
    base = Path(location) if location else Path.home() / ".dbs-annotator"
    base.mkdir(parents=True, exist_ok=True)
    return base


def user_config_file(name: str) -> Path:
    """Return a path under :func:`user_data_dir` for a named config file.

    Parent directories are created on demand so callers can immediately write
    to the returned path.
    """
    path = user_data_dir() / name
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
