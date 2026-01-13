"""
Step 2 view - Session scales configuration.

This module contains the view for the second step where users configure
the session tracking scales that will be used during the programming session.
"""

from typing import Callable, List, Tuple

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStyle,
    QVBoxLayout,
    QWidget,
)

from ..config import PLACEHOLDERS, PRESET_BUTTONS
from .base_view import BaseStepView


class Step2View(BaseStepView):
    """
    Second step view for session scales configuration.

    This view handles:
    - Selection of session tracking scales
    - Configuration of scale ranges (min/max values)
    """

    def __init__(self, logo_pixmap: QPixmap, parent_style):
        """
        Initialize Step 2 view.

        Args:
            logo_pixmap: Application logo
            parent_style: Parent widget style for icon access
        """
        super().__init__(logo_pixmap)
        self.parent_style = parent_style
        self.session_scales_rows: List[
            Tuple[QLineEdit, QLineEdit, QLineEdit, QHBoxLayout]
        ] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the UI layout."""
        # Header
        header = self.create_header("Which session scales would you like to track?")
        self.main_layout.addWidget(header)

        # Session scales group
        session_group = self._create_session_scales_group()
        self.main_layout.addWidget(session_group)
        self.main_layout.addStretch(1)

        # Next button
        self.next_button = QPushButton("Next")
        self.next_button.setIcon(self.parent_style.standardIcon(QStyle.SP_ArrowForward))
        self.next_button.setIconSize(QSize(16, 16))
        self.next_button.setMaximumWidth(120)
        self.main_layout.addWidget(self.next_button, alignment=Qt.AlignRight)

    def _create_session_scales_group(self) -> QGroupBox:
        """Create the session scales group box."""
        gb_session = QGroupBox("Session scales")
        gb_session.setStyleSheet(
            "QGroupBox::title { color: #ff8800; font-size: 11pt; font-weight: 600; }"
        )
        gb_session.setFont(QFont("Segoe UI", 10, QFont.Bold))
        gb_session.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        gb_session.setMinimumHeight(400)  # Increased height for better visibility

        layout = QVBoxLayout(gb_session)

        # Preset buttons
        preset_row = QHBoxLayout()
        for label in PRESET_BUTTONS:
            btn = QPushButton(label)
            btn.setObjectName(f"preset2_{label}")
            preset_row.addWidget(btn)
        preset_row.addStretch(1)
        layout.addLayout(preset_row)

        # Container for dynamic scale rows - expands to show all rows
        scroll_content = QWidget()
        scroll_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.session_scales_container = QVBoxLayout(scroll_content)
        self.session_scales_container.setContentsMargins(0, 0, 0, 0)

        # Scrollable area - will only scroll when user resizes window smaller
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll_area.setWidget(scroll_content)

        layout.addWidget(scroll_area)

        return gb_session

    def get_preset_button(self, preset_name: str) -> QPushButton:
        """Get a preset button by name."""
        return self.findChild(QPushButton, f"preset2_{preset_name}")

    def update_session_scales(
        self,
        preset_scales: List[Tuple[str, str, str]],
        on_add_callback: Callable,
        on_remove_callback: Callable,
    ) -> None:
        """
        Update the session scales UI with the given scales.

        Args:
            preset_scales: List of (name, min, max) tuples
            on_add_callback: Callback for add button
            on_remove_callback: Callback for remove button
        """
        # Clear existing rows
        for _, _, _, row_layout in self.session_scales_rows:
            while row_layout.count():
                item = row_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            self.session_scales_container.removeItem(row_layout)
        self.session_scales_rows = []

        # Add preset scales
        for name, minval, maxval in preset_scales:
            self._add_session_scale_row(
                name, minval, maxval, with_minus=True, on_remove=on_remove_callback
            )

        # Add empty row with add button
        self._add_session_scale_row("", "", "", with_plus=True, on_add=on_add_callback)

    def _add_session_scale_row(
        self,
        name: str = "",
        minval: str = "",
        maxval: str = "",
        with_plus: bool = False,
        with_minus: bool = False,
        on_add: Callable = None,
        on_remove: Callable = None,
    ) -> None:
        """Add a single session scale row."""
        row = QHBoxLayout()

        name_edit = QLineEdit()
        name_edit.setPlaceholderText(PLACEHOLDERS["scale_name"])
        name_edit.setMaximumWidth(100)
        name_edit.setText(name)

        scale1_edit = QLineEdit()
        scale1_edit.setPlaceholderText(PLACEHOLDERS["scale_min"])
        scale1_edit.setMaximumWidth(40)
        scale1_edit.setText(minval)

        scale2_edit = QLineEdit()
        scale2_edit.setPlaceholderText(PLACEHOLDERS["scale_max"])
        scale2_edit.setMaximumWidth(40)
        scale2_edit.setText(maxval)

        if with_plus:
            btn = QPushButton("+")
            btn.setToolTip("Add session scale")
            btn.setMaximumWidth(24)
            if on_add:
                btn.clicked.connect(on_add)
        elif with_minus:
            btn = QPushButton("-")
            btn.setToolTip("Remove session scale")
            btn.setMaximumWidth(24)
            if on_remove:
                btn.clicked.connect(lambda: on_remove(row))
        else:
            btn = QLabel("")

        row.addWidget(QLabel("Name:"))
        row.addWidget(name_edit)
        row.addSpacing(5)
        row.addWidget(QLabel("Min:"))
        row.addWidget(scale1_edit)
        row.addWidget(QLabel("Max:"))
        row.addWidget(scale2_edit)
        row.addWidget(btn)
        row.addStretch(1)

        self.session_scales_container.addLayout(row)
        self.session_scales_rows.append((name_edit, scale1_edit, scale2_edit, row))
