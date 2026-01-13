"""
Simplified annotations view for annotations-only mode.

This module contains views for the simplified workflow that only
handles file naming and text annotations.
"""

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QGroupBox,
    QStyle,
    QTextEdit,
)
from PyQt5.QtGui import QFont


class AnnotationsFileView(QWidget):
    """View for file selection in annotations-only mode."""

    def __init__(self, parent=None):
        """Initialize the file selection view."""
        super().__init__(parent)
        self.parent_style = self.style()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # File information group
        file_group = self._create_file_group()
        self.main_layout.addWidget(file_group)

        self.main_layout.addStretch(1)

        # Next button
        self.next_button = QPushButton("Next")
        self.next_button.setIcon(self.parent_style.standardIcon(QStyle.SP_ArrowForward))
        self.next_button.setIconSize(QSize(16, 16))
        self.next_button.setMaximumWidth(120)
        self.main_layout.addWidget(self.next_button, alignment=Qt.AlignRight)

    def _create_file_group(self) -> QGroupBox:
        """Create the file information group box."""
        gb_file = QGroupBox("Output File")
        gb_file.setFont(QFont("Segoe UI", 10, QFont.Bold))

        layout = QFormLayout(gb_file)
        layout.setHorizontalSpacing(15)
        layout.setVerticalSpacing(12)

        # File path with browse button
        file_row = QHBoxLayout()
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("Select file location and name...")
        file_row.addWidget(self.file_path_edit)

        self.browse_button = QPushButton()
        self.browse_button.setMaximumWidth(32)
        self.browse_button.setIcon(self.parent_style.standardIcon(QStyle.SP_DirOpenIcon))
        self.browse_button.setToolTip("Browse for file")
        file_row.addWidget(self.browse_button)

        layout.addRow(QLabel("File:"), file_row)

        return gb_file


class AnnotationsSessionView(QWidget):
    """View for recording annotations in annotations-only mode."""

    def __init__(self, parent=None):
        """Initialize the annotations session view."""
        super().__init__(parent)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # Annotation input group
        annotation_group = self._create_annotation_group()
        self.main_layout.addWidget(annotation_group)

        # Action buttons
        buttons_row = QHBoxLayout()
        buttons_row.addStretch(1)

        self.insert_button = QPushButton("Insert Annotation")
        self.insert_button.setObjectName("insert_button")
        self.insert_button.setMinimumWidth(150)
        buttons_row.addWidget(self.insert_button)

        self.close_button = QPushButton("Close Session")
        self.close_button.setObjectName("close_button")
        self.close_button.setMinimumWidth(150)
        buttons_row.addWidget(self.close_button)

        self.main_layout.addLayout(buttons_row)

    def _create_annotation_group(self) -> QGroupBox:
        """Create the annotation input group box."""
        gb_annotation = QGroupBox("Session Annotations")
        gb_annotation.setFont(QFont("Segoe UI", 10, QFont.Bold))

        layout = QVBoxLayout(gb_annotation)
        layout.setSpacing(10)

        # Instructions
        instructions = QLabel(
            "Enter your observations and notes below. "
            "Each annotation will be saved with the current timestamp."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #64748b; padding: 5px;")
        layout.addWidget(instructions)

        # Annotation text area
        self.annotation_edit = QTextEdit()
        self.annotation_edit.setPlaceholderText(
            "Type your annotation here...\n\n"
            "Example:\n"
            "- Patient shows improvement in tremor\n"
            "- Side effects: mild tingling in left hand\n"
            "- Response to stimulation adjustment: positive"
        )
        self.annotation_edit.setMinimumHeight(300)
        layout.addWidget(self.annotation_edit)

        return gb_annotation

    def get_annotation(self) -> str:
        """Get the current annotation text."""
        return self.annotation_edit.toPlainText()

    def clear_annotation(self) -> None:
        """Clear the annotation text area."""
        self.annotation_edit.clear()
