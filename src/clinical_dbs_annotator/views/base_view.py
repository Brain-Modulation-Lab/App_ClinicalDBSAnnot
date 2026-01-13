"""
Base view class for wizard steps.

This module provides the base class that all step views inherit from,
containing common functionality and UI elements.
"""

from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ..utils import rounded_pixmap


class BaseStepView(QWidget):
    """
    Base class for all wizard step views.

    This class provides common functionality for step views including:
    - Logo display
    - Welcome message layout
    - Common UI patterns

    Subclasses should implement their specific UI in the create_content() method.
    """

    def __init__(self, logo_pixmap: Optional[QPixmap] = None):
        """
        Initialize the base step view.

        Args:
            logo_pixmap: The application logo pixmap to display
        """
        super().__init__()
        self.logo_pixmap = logo_pixmap
        self.main_layout = QVBoxLayout(self)

    def create_header(
        self, welcome_text: str, logo_width: int = 70, logo_radius: int = 5
    ) -> QWidget:
        """
        Create a header with logo and welcome text.

        Args:
            welcome_text: The welcome/instruction text to display
            logo_width: Width to scale the logo to
            logo_radius: Corner radius for rounded logo

        Returns:
            QWidget containing the header elements with fixed height
        """
        header_widget = QWidget()
        header_widget.setMaximumHeight(80)
        header_row = QHBoxLayout(header_widget)
        header_row.setContentsMargins(0, 0, 0, 0)

        # Logo
        if self.logo_pixmap:
            image_label = QLabel()
            logo = self.logo_pixmap.scaledToWidth(logo_width, Qt.SmoothTransformation)
            logo = rounded_pixmap(logo, logo_radius)
            image_label.setPixmap(logo)
            image_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
            header_row.addWidget(image_label, 1)

        # Welcome text
        welcome_label = QLabel(welcome_text)
        welcome_label.setStyleSheet("font-size: 14pt; font-weight: 500;")
        welcome_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        welcome_label.setWordWrap(True)
        header_row.addWidget(welcome_label, 4)

        return header_widget

    def create_step1_header(self, welcome_text: str) -> QWidget:
        """
        Create header for step 1 with larger logo.

        Args:
            welcome_text: The welcome text to display

        Returns:
            QWidget containing the header elements with fixed height
        """
        header_widget = QWidget()
        header_widget.setMaximumHeight(100)
        header_row = QHBoxLayout(header_widget)
        header_row.setContentsMargins(0, 0, 0, 0)

        # Logo (larger for first step)
        if self.logo_pixmap:
            image_label = QLabel()
            logo = self.logo_pixmap.scaledToWidth(80, Qt.SmoothTransformation)
            logo = rounded_pixmap(logo, 10)
            image_label.setPixmap(logo)
            image_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
            header_row.addWidget(image_label, 1)

        # Welcome text (larger for first step)
        welcome_label = QLabel(welcome_text)
        welcome_label.setStyleSheet("font-size: 16pt; font-weight: 500;")
        welcome_label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        welcome_label.setWordWrap(True)
        header_row.addWidget(welcome_label, 4)

        return header_widget
