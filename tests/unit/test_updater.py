"""Tests for :mod:`dbs_annotator.utils.updater`."""

from __future__ import annotations

import io
import urllib.error
from unittest.mock import patch

import pytest

from dbs_annotator.utils.updater import _CheckSignals, _CheckWorker


def test_fetch_latest_release_http_404_returns_none() -> None:
    """GitHub ``/releases/latest`` → 404 when nothing published; no exception."""
    signals = _CheckSignals()
    worker = _CheckWorker("owner/repo", "1.0.0", 10.0, signals)
    err = urllib.error.HTTPError(
        "https://api.github.com/repos/owner/repo/releases/latest",
        404,
        "Not Found",
        {},
        io.BytesIO(b""),
    )
    with patch("urllib.request.urlopen", side_effect=err):
        assert worker._fetch_latest_release() is None


@pytest.mark.parametrize("code", [403, 500, 502])
def test_fetch_latest_release_other_http_raises(code: int) -> None:
    signals = _CheckSignals()
    worker = _CheckWorker("owner/repo", "1.0.0", 10.0, signals)
    err = urllib.error.HTTPError(
        "https://example.com",
        code,
        "err",
        {},
        io.BytesIO(b""),
    )
    with patch("urllib.request.urlopen", side_effect=err), pytest.raises(
        urllib.error.HTTPError
    ) as ctx:
        worker._fetch_latest_release()
    assert ctx.value.code == code
