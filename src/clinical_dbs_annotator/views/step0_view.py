"""
Step 0 view: Mode selection page.

This module contains the initial view where users choose between
full mode (with stimulation settings and scales) or annotations-only mode.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSizePolicy,
)
from PyQt5.QtGui import QFont


class Step0View(QWidget):
    """
    Step 0: Mode selection view.

    Users can choose between:
    - Full mode: Annotations + stimulation settings + clinical scales
    - Simple mode: Annotations only
    """

    def __init__(self, parent=None):
        """Initialize the Step 0 view."""
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(30)

        # Title
        title_label = QLabel("Select Annotation Mode")
        font = QFont("Segoe UI")   
        font.setPointSize(25)      
        font.setBold(True)         
        title_label.setFont(font) 
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Choose the type of annotation session you want to perform")
        subtitle_label.setFont(QFont("Segoe UI", 11))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #64748b;")
        self.main_layout.addWidget(subtitle_label)

        # Add spacing
        self.main_layout.addSpacing(20)

        # Buttons container
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(30)

        # Full mode button
        self.full_mode_button = QPushButton(
            "Annotations + Stimulation\nSettings + Clinical Scales"
        )
        self.full_mode_button.setObjectName("full_mode_button")
        self.full_mode_button.setMinimumHeight(180)
        self.full_mode_button.setMinimumWidth(300)
        self.full_mode_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.full_mode_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.full_mode_button.setCursor(Qt.PointingHandCursor)
        buttons_layout.addWidget(self.full_mode_button)

        # Annotations only button
        self.annotations_only_button = QPushButton("Annotations Only")
        self.annotations_only_button.setObjectName("annotations_only_button")
        self.annotations_only_button.setMinimumHeight(180)
        self.annotations_only_button.setMinimumWidth(300)
        self.annotations_only_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.annotations_only_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.annotations_only_button.setCursor(Qt.PointingHandCursor)
        buttons_layout.addWidget(self.annotations_only_button)

        self.main_layout.addLayout(buttons_layout)

        # Description labels
        descriptions_layout = QHBoxLayout()
        descriptions_layout.setSpacing(30)

        # Full mode description
        full_desc = QLabel(
            "Complete workflow including:\n"
            "• Patient and session details\n"
            "• Stimulation parameters\n"
            "• Clinical assessment scales\n"
            "• Session annotations"
        )
        full_desc.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        full_desc.setWordWrap(True)
        full_desc.setFont(QFont("Segoe UI", 10))
        full_desc.setStyleSheet("color: #64748b; padding: 10px;")
        full_desc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        descriptions_layout.addWidget(full_desc)

        # Annotations only description
        annot_desc = QLabel(
            "Simplified workflow for:\n"
            "• Quick annotations\n"
            "• Time-stamped notes\n"
            "• Text-only observations\n"
            "• Rapid session recording"
        )
        annot_desc.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        annot_desc.setWordWrap(True)
        annot_desc.setFont(QFont("Segoe UI", 10))
        annot_desc.setStyleSheet("color: #64748b; padding: 10px;")
        annot_desc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        descriptions_layout.addWidget(annot_desc)

        self.main_layout.addLayout(descriptions_layout)

        # Add stretch to push everything to the top
        self.main_layout.addStretch(1)
