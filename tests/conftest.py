"""Shared pytest fixtures for Qt and the main wizard."""

from __future__ import annotations

import os

# Headless-friendly Qt before any QWidget is constructed (pytest loads conftest early).
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

from dbs_annotator.views.wizard_window import WizardWindow


@pytest.fixture
def wizard(qtbot, qapp):
    """Main wizard window bound to the session QApplication."""
    w = WizardWindow(qapp)
    qtbot.addWidget(w)
    w.show()
    return w


@pytest.fixture
def bids_like_tsv(tmp_path):
    """Minimal TSV path suitable for SessionData.open_file (new file)."""
    path = tmp_path / "sub-01_ses-20250101_task-prog_run-01_events.tsv"
    path.write_text("", encoding="utf-8")
    return path
