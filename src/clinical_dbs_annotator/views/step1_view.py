"""
Step 1 view - Initial settings and clinical scales.

This module contains the view for the first step of the wizard where users
configure initial settings, stimulation parameters, and clinical scales.
"""

from typing import Callable, List, Tuple

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QDoubleValidator, QFont, QIntValidator, QPixmap
from PyQt5.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStyle,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..config import (
    PLACEHOLDERS,
    PRESET_BUTTONS,
    STIMULATION_LIMITS,
)
from ..ui import create_horizontal_line, MultiSelectComboBoxWithDisplay
from .base_view import BaseStepView


class Step1View(BaseStepView):
    """
    First step view for initial configuration.

    This view handles:
    - File selection for TSV output
    - Initial stimulation parameters
    - Clinical scales configuration
    - Initial notes
    """

    def __init__(self, logo_pixmap: QPixmap, parent_style):
        """
        Initialize Step 1 view.

        Args:
            logo_pixmap: Application logo
            parent_style: Parent widget style for icon access
        """
        super().__init__(logo_pixmap)
        self.parent_style = parent_style
        self.clinical_scales_rows: List[Tuple[QLineEdit, QLineEdit, QHBoxLayout]] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the UI layout."""
        # Header
        header = self.create_step1_header(
            "Welcome to the BML Annotator for Percept clinical programming sessions!"
        )
        self.main_layout.addWidget(header)

        # Main content area
        content_layout = QHBoxLayout()

        # Left side: Initial settings
        settings_group = self._create_settings_group()
        content_layout.addWidget(settings_group)

        # Right side: Clinical scales and notes
        right_layout = QVBoxLayout()
        clinical_group = self._create_clinical_scales_group()
        notes_group = self._create_notes_group()
        right_layout.addWidget(clinical_group)
        right_layout.addWidget(notes_group)
        content_layout.addLayout(right_layout)

        self.main_layout.addLayout(content_layout)

        # Next button
        self.next_button = QPushButton("Next")
        self.next_button.setIcon(self.parent_style.standardIcon(QStyle.SP_ArrowForward))
        self.next_button.setIconSize(QSize(16, 16))
        self.next_button.setMaximumWidth(120)
        self.main_layout.addWidget(self.next_button, alignment=Qt.AlignRight)

    def _create_settings_group(self) -> QGroupBox:
        """Create the initial settings group box."""
        gb_init = QGroupBox("Initial settings")
        gb_init.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        gb_init.setFont(QFont("Segoe UI", 12, QFont.Bold))
        gb_init.setStyleSheet(
            "QGroupBox { margin-top: 16pt; } "
            "QGroupBox::title { color: #ff8800; margin-left: 4pt; "
            "font-size: 16pt; font-weight: 600; }"
        )

        layout = QFormLayout(gb_init)
        layout.setLabelAlignment(Qt.AlignRight)

        # File selection
        file_row = QHBoxLayout()
        self.file_path_edit = QLineEdit()
        browse_button = QPushButton()
        browse_button.setMaximumWidth(32)
        browse_button.setIcon(self.parent_style.standardIcon(QStyle.SP_DirOpenIcon))
        browse_button.setToolTip("Browse for file")
        browse_button.clicked.connect(self.browse_file)
        file_row.addWidget(self.file_path_edit)
        file_row.addWidget(browse_button)
        file_container = QWidget()
        file_container.setStyleSheet("background-color: transparent;")
        file_container.setLayout(file_row)
        layout.addRow(QLabel("File:"), file_container)

        layout.addWidget(create_horizontal_line())

        # Left electrode section
        layout.addRow(QLabel(""), QLabel(""))  # Empty row for spacing
        left_electrode_label = QLabel("Left electrode")
        left_electrode_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        layout.addRow(left_electrode_label, QLabel(""))

        # Left stimulation frequency
        self.left_stim_freq_edit = QLineEdit()
        self.left_stim_freq_edit.setMaximumWidth(80)
        self.left_stim_freq_edit.setPlaceholderText(PLACEHOLDERS["frequency"])
        freq_limits = STIMULATION_LIMITS["frequency"]
        self.left_stim_freq_edit.setValidator(
            QIntValidator(freq_limits["min"], freq_limits["max"])
        )
        layout.addRow(QLabel("Stimulation frequency:"), self.left_stim_freq_edit)

        # Left Anode (+)
        self.left_anode_combo = MultiSelectComboBoxWithDisplay()
        self.left_anode_combo.setMinimumWidth(150)
        self.left_anode_combo.addItems([
            "case", "0 ring", "1 ring", "1a", "1b", "1c",
            "2 ring", "2a", "2b", "2c", "3 ring"
        ])
        anode_label = QLabel("Anode (+):")
        layout.addRow(anode_label, self.left_anode_combo)

        # Left Cathode (-)
        self.left_cathode_combo = MultiSelectComboBoxWithDisplay()
        self.left_cathode_combo.setMinimumWidth(150)
        self.left_cathode_combo.addItems([
            "case", "0 ring", "1 ring", "1a", "1b", "1c",
            "2 ring", "2a", "2b", "2c", "3 ring"
        ])
        # # Set ground as default for cathode
        # self.left_cathode_combo.set_selected_items(["ground"])
        cathode_label = QLabel("Cathode (-):")
        layout.addRow(cathode_label, self.left_cathode_combo)

        # Left amplitude
        self.left_amp_edit = QLineEdit()
        self.left_amp_edit.setMaximumWidth(80)
        self.left_amp_edit.setPlaceholderText(PLACEHOLDERS["amplitude"])
        amp_limits = STIMULATION_LIMITS["amplitude"]
        self.left_amp_edit.setValidator(
            QDoubleValidator(amp_limits["min"], amp_limits["max"], amp_limits["decimals"])
        )
        layout.addRow(QLabel("Amplitude:"), self.left_amp_edit)

        # Left pulse width
        self.left_pw_edit = QLineEdit()
        self.left_pw_edit.setMaximumWidth(80)
        self.left_pw_edit.setPlaceholderText(PLACEHOLDERS["pulse_width"])
        pw_limits = STIMULATION_LIMITS["pulse_width"]
        self.left_pw_edit.setValidator(QIntValidator(pw_limits["min"], pw_limits["max"]))
        layout.addRow(QLabel("Pulse width:"), self.left_pw_edit)

        layout.addWidget(create_horizontal_line())



        # Right electrode section
        layout.addRow(QLabel(""), QLabel(""))  # Empty row for spacing
        right_electrode_label = QLabel("Right electrode")
        right_electrode_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        layout.addRow(right_electrode_label, QLabel(""))

        # Right stimulation frequency
        self.right_stim_freq_edit = QLineEdit()
        self.right_stim_freq_edit.setMaximumWidth(80)
        self.right_stim_freq_edit.setPlaceholderText(PLACEHOLDERS["frequency"])
        self.right_stim_freq_edit.setValidator(
            QIntValidator(freq_limits["min"], freq_limits["max"])
        )
        layout.addRow(QLabel("Stimulation frequency:"), self.right_stim_freq_edit)

        # Right Anode (+)
        self.right_anode_combo = MultiSelectComboBoxWithDisplay()
        self.right_anode_combo.setMaximumWidth(150)
        self.right_anode_combo.addItems([
            "case", "0 ring", "1 ring", "1a", "1b", "1c",
            "2 ring", "2a", "2b", "2c", "3 ring"
        ])
        anode_label_r = QLabel("Anode (+):")
        layout.addRow(anode_label_r, self.right_anode_combo)

        # Right Cathode (-)
        self.right_cathode_combo = MultiSelectComboBoxWithDisplay()
        self.right_cathode_combo.setMaximumWidth(150)
        self.right_cathode_combo.addItems([
            "case", "0 ring", "1 ring", "1a", "1b", "1c",
            "2 ring", "2a", "2b", "2c", "3 ring"
        ])
        # # Set ground as default for cathode
        # self.right_cathode_combo.set_selected_items(["ground"])
        cathode_label_r = QLabel("Cathode (-):")
        layout.addRow(cathode_label_r, self.right_cathode_combo)

        # Right amplitude
        self.right_amp_edit = QLineEdit()
        self.right_amp_edit.setMaximumWidth(80)
        self.right_amp_edit.setPlaceholderText(PLACEHOLDERS["amplitude"])
        self.right_amp_edit.setValidator(
            QDoubleValidator(amp_limits["min"], amp_limits["max"], amp_limits["decimals"])
        )
        layout.addRow(QLabel("Amplitude:"), self.right_amp_edit)

        # Right plse width
        self.right_pw_edit = QLineEdit()
        self.right_pw_edit.setMaximumWidth(80)
        self.right_pw_edit.setPlaceholderText(PLACEHOLDERS["pulse_width"])
        self.right_pw_edit.setValidator(QIntValidator(pw_limits["min"], pw_limits["max"]))
        layout.addRow(QLabel("Pulse width:"), self.right_pw_edit)

        return gb_init

    def _create_clinical_scales_group(self) -> QGroupBox:
        """Create the clinical scales group box."""
        gb_clinical = QGroupBox("Clinical scales")
        gb_clinical.setStyleSheet(
            "QGroupBox::title { color: #ff8800; font-size: 11pt; font-weight: 600; }"
        )
        gb_clinical.setFont(QFont("Segoe UI", 10, QFont.Bold))
        gb_clinical.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout(gb_clinical)

        # Preset buttons
        preset_row = QHBoxLayout()
        for label in PRESET_BUTTONS:
            btn = QPushButton(label)
            btn.setObjectName(f"preset_{label}")
            preset_row.addWidget(btn)
        preset_row.addStretch(1)
        layout.addLayout(preset_row)

        # Container for dynamic scale rows - expands to show all rows
        scroll_content = QWidget()
        scroll_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.clinical_scales_container = QVBoxLayout(scroll_content)
        self.clinical_scales_container.setContentsMargins(0, 0, 0, 0)

        # Scrollable area - will only scroll when user resizes window smaller
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll_area.setWidget(scroll_content)

        layout.addWidget(scroll_area)

        return gb_clinical

    def _create_notes_group(self) -> QGroupBox:
        """Create the initial notes group box."""
        gb_notes = QGroupBox("Initial notes")
        gb_notes.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        gb_notes.setFont(QFont("Segoe UI", 10, QFont.Bold))
        gb_notes.setStyleSheet(
            "QGroupBox::title { color: #ff8800; font-size: 11pt; font-weight: 600; }"
        )

        layout = QHBoxLayout(gb_notes)
        self.notes_edit = QTextEdit()
        self.notes_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.notes_edit.setMinimumHeight(40)
        layout.addWidget(self.notes_edit)

        return gb_notes

    def browse_file(self) -> None:
        """Open file dialog for TSV file selection."""
        import os

        # Get current path if available
        current_path = self.file_path_edit.text()
        if current_path:
            start_dir = os.path.dirname(current_path)
            default_name = os.path.basename(current_path)
        else:
            start_dir = ""
            default_name = "annot.tsv"

        # Combine directory and default filename
        default_path = os.path.join(start_dir, default_name) if start_dir else default_name

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save TSV File", default_path, "TSV Files (*.tsv);;All Files (*)"
        )
        if file_path:
            if not file_path.endswith(".tsv"):
                file_path += ".tsv"
            self.file_path_edit.setText(file_path)

    def get_preset_button(self, preset_name: str) -> QPushButton:
        """Get a preset button by name."""
        return self.findChild(QPushButton, f"preset_{preset_name}")

    def update_clinical_scales(
        self, preset_scales: List[str], on_add_callback: Callable, on_remove_callback: Callable
    ) -> None:
        """
        Update the clinical scales UI with the given scales.

        Args:
            preset_scales: List of scale names to display
            on_add_callback: Callback for add button
            on_remove_callback: Callback for remove button
        """
        # Clear existing rows
        for _, _, row_layout in self.clinical_scales_rows:
            while row_layout.count():
                item = row_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            self.clinical_scales_container.removeItem(row_layout)
        self.clinical_scales_rows = []

        # Add preset scales
        for name in preset_scales:
            self._add_clinical_scale_row(name, with_minus=True, on_remove=on_remove_callback)

        # Add empty row with add button
        self._add_clinical_scale_row("", with_plus=True, on_add=on_add_callback)

    def _add_clinical_scale_row(
        self,
        name: str = "",
        with_plus: bool = False,
        with_minus: bool = False,
        on_add: Callable = None,
        on_remove: Callable = None,
    ) -> None:
        """Add a single clinical scale row."""
        row = QHBoxLayout()

        name_edit = QLineEdit()
        name_edit.setPlaceholderText(PLACEHOLDERS["scale_name"])
        name_edit.setMaximumWidth(80)
        name_edit.setText(name)

        score_edit = QLineEdit()
        score_edit.setPlaceholderText(PLACEHOLDERS["scale_score"])
        score_edit.setMaximumWidth(50)

        if with_plus:
            btn = QPushButton("+")
            btn.setToolTip("Add clinical scale")
            btn.setMaximumWidth(24)
            if on_add:
                btn.clicked.connect(on_add)
        elif with_minus:
            btn = QPushButton("-")
            btn.setToolTip("Remove clinical scale")
            btn.setMaximumWidth(24)
            if on_remove:
                btn.clicked.connect(lambda: on_remove(row))
        else:
            btn = QLabel("")

        row.addWidget(QLabel("Name:"))
        row.addWidget(name_edit)
        row.addSpacing(5)
        row.addWidget(QLabel("Score:"))
        row.addWidget(score_edit)
        row.addWidget(btn)
        row.addStretch(1)

        self.clinical_scales_container.addLayout(row)
        self.clinical_scales_rows.append((name_edit, score_edit, row))
