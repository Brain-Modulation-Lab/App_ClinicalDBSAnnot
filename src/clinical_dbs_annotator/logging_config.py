import logging
import platform
import sys
import threading
from logging.handlers import RotatingFileHandler
from pathlib import Path

from PySide6.QtCore import (
    QMessageLogContext,
    QStandardPaths,
    QtMsgType,
    qInstallMessageHandler,
)
from PySide6.QtWidgets import QApplication

from . import __version__

_configured = False
_log_file_path: Path | None = None


def setup_logging(_app: QApplication) -> Path:
    global _configured, _log_file_path
    if _configured:
        assert _log_file_path is not None
        return _log_file_path

    base = Path(
        QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppLocalDataLocation
        )
    )
    log_dir = base / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "clinical-dbs-annotator.log"

    fmt = logging.Formatter("%(asctime)s ¦ %(levelname)s ¦ %(name)s ¦ %(message)s")
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    for h in root.handlers[:]:
        root.removeHandler(h)

    fh = RotatingFileHandler(
        log_path, maxBytes=5_000_000, backupCount=3, encoding="utf-8"
    )
    fh.setLevel(logging.INFO)
    fh.setFormatter(fmt)
    root.addHandler(fh)

    if not getattr(sys, "frozen", False):
        sh = logging.StreamHandler(sys.stderr)
        sh.setLevel(logging.INFO)
        sh.setFormatter(fmt)
        root.addHandler(sh)

    def exc_hook(exc_type, exc, tb):
        logging.getLogger("uncaught").critical(
            "Uncaught exception",
            exc_info=(exc_type, exc, tb),
        )

    sys.excepthook = exc_hook

    def thread_exc_hook(args: threading.ExceptHookArgs) -> None:
        logging.getLogger("uncaught").critical(
            "Uncaught thread exception",
            exc_info=(args.exc_type, args.exc_value, args.exc_traceback),
        )

    threading.excepthook = thread_exc_hook

    def qt_handler(mode: QtMsgType, context: QMessageLogContext, message: str) -> None:
        if mode == QtMsgType.QtDebugMsg:
            level = logging.DEBUG
        elif mode == QtMsgType.QtInfoMsg:
            level = logging.INFO
        elif mode == QtMsgType.QtWarningMsg:
            level = logging.WARNING
        elif mode == QtMsgType.QtCriticalMsg:
            level = logging.ERROR
        else:
            level = logging.CRITICAL
        suffix = ""
        if context.file:
            suffix = f" ({context.file}:{context.line})"
        logging.getLogger("qt").log(level, "%s%s", message, suffix)

    qInstallMessageHandler(qt_handler)

    logging.getLogger("clinical_dbs_annotator").info(
        "Started v%s Python %s | %s | log=%s",
        __version__,
        platform.python_version(),
        platform.platform(),
        log_path.resolve(),
    )

    resolved = log_path.resolve()
    _configured = True
    _log_file_path = resolved
    return resolved
