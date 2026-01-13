"""
Custom UI widgets and components.

This module provides reusable UI components such as increment buttons,
section labels, and horizontal lines.
"""

from typing import Optional

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..config import BUTTON_SIZES, COLORS, ICON_SIZES
from ..utils import create_arrow_icon


def create_horizontal_line() -> QFrame:
    """
    Create a styled horizontal separator line.

    Returns:
        QFrame configured as a horizontal line
    """
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)
    line.setStyleSheet(
        f"background: {COLORS['separator']}; "
        "max-height: 2pt; min-height: 2pt; "
        "border: none; margin: 10pt 0 10pt 0;"
    )
    return line


def create_section_label(text: str) -> QLabel:
    """
    Create a styled section label.

    Args:
        text: The label text

    Returns:
        QLabel styled as a section header
    """
    label = QLabel(text)
    label.setStyleSheet(
        f"color: {COLORS['primary']}; "
        "font-size: 18pt; font-weight: 600; "
        "margin-bottom: 4pt;"
    )
    return label


class IncrementWidget(QWidget):
    """
    A widget that combines a QLineEdit with increment/decrement buttons.

    This widget provides a text input field with up/down arrow buttons for
    incrementing/decrementing numeric values. Supports single and dual-step modes.

    Attributes:
        line_edit: The QLineEdit for value input
        step1: Large increment/decrement step
        step2: Small increment/decrement step (optional)
        decimals: Number of decimal places for formatting
        min_value: Minimum allowed value
        max_value: Maximum allowed value
    """

    def __init__(
        self,
        line_edit: QLineEdit,
        step1: float = 1.0,
        step2: Optional[float] = None,
        decimals: int = 2,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
    ):
        """
        Initialize the increment widget.

        Args:
            line_edit: QLineEdit to attach increment buttons to
            step1: Primary step size for large adjustments
            step2: Secondary step size for small adjustments (optional)
            decimals: Number of decimal places for value formatting
            min_value: Minimum allowed value
            max_value: Maximum allowed value
        """
        super().__init__()
        self.line_edit = line_edit
        self.step1 = step1
        self.step2 = step2
        self.decimals = decimals
        self.min_value = min_value
        self.max_value = max_value

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the widget UI layout."""
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        hbox.addWidget(self.line_edit)

        # Create primary increment/decrement buttons (step1)
        vbox1 = self._create_button_column(self.step1, double=True)
        hbox.addLayout(vbox1)

        # Create secondary buttons if step2 is provided
        if self.step2 is not None:
            vbox2 = self._create_button_column(self.step2, double=False)
            hbox.addLayout(vbox2)

        self.setMaximumWidth(self.sizeHint().width())

    def _create_button_column(
        self, step: float, double: bool = False
    ) -> QVBoxLayout:
        """
        Create a column of up/down buttons.

        Args:
            step: The step value for this button pair
            double: If True, creates double arrow icons

        Returns:
            QVBoxLayout containing the up and down buttons
        """
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        # Create up button
        btn_up = self._create_arrow_button("up", double)
        btn_up.clicked.connect(lambda: self._adjust_value(+step))

        # Create down button
        btn_down = self._create_arrow_button("down", double)
        btn_down.clicked.connect(lambda: self._adjust_value(-step))

        vbox.addWidget(btn_up)
        vbox.addWidget(btn_down)

        return vbox

    def _create_arrow_button(self, direction: str, double: bool) -> QPushButton:
        """
        Create an arrow button.

        Args:
            direction: Arrow direction ("up" or "down")
            double: If True, creates a double arrow icon

        Returns:
            Configured QPushButton with arrow icon
        """
        btn = QPushButton()
        btn.setIcon(create_arrow_icon(direction, double))
        btn.setIconSize(QSize(*ICON_SIZES["increment"]))
        btn.setFixedSize(
            BUTTON_SIZES["increment"]["width"], BUTTON_SIZES["increment"]["height"]
        )
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
                padding: 0;
            }
            QPushButton:hover, QPushButton:pressed {
                background: transparent;
            }
        """
        )
        return btn

    def _adjust_value(self, delta: float) -> None:
        """
        Adjust the line edit value by a delta.

        Args:
            delta: Amount to add to current value (can be negative)
        """
        try:
            value = float(self.line_edit.text())
        except (ValueError, TypeError):
            value = 0.0

        value += delta

        # Apply min/max constraints
        if self.min_value is not None:
            value = max(value, self.min_value)
        if self.max_value is not None:
            value = min(value, self.max_value)

        # Format and set the new value
        self.line_edit.setText(f"{value:.{self.decimals}f}")

    def get_line_edit(self) -> QLineEdit:
        """Get the underlying QLineEdit widget."""
        return self.line_edit
