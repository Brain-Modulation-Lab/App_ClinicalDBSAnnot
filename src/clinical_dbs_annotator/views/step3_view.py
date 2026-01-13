"""
Step 3 view - Active session recording.

This module contains the view for the third step where users actively record
session data including stimulation parameters and scale values.
"""

from typing import List, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QFont, QIntValidator, QPixmap
from PyQt5.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QStyle,
    QTextEdit,
    QVBoxLayout,
    QMenu,
)

from ..config import (
    PLACEHOLDERS,
    SESSION_SCALE_LIMITS,
    STIMULATION_LIMITS,
)
from ..ui import IncrementWidget, create_horizontal_line, MultiSelectComboBox
from .base_view import BaseStepView


class Step3View(BaseStepView):
    """
    Third step view for active session recording.

    This view handles:
    - Real-time stimulation parameter adjustment
    - Session scale value recording
    - Session notes
    - Data insertion and session closing
    """

    def __init__(self, logo_pixmap: QPixmap, parent_style):
        """
        Initialize Step 3 view.

        Args:
            logo_pixmap: Application logo
            parent_style: Parent widget style for icon access
        """
        super().__init__(logo_pixmap)
        self.parent_style = parent_style
        self.session_scale_value_edits: List[Tuple[str, QLineEdit]] = []
        self.step3_session_scales_form: QFormLayout = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the UI layout."""
        self.main_layout.setSpacing(8)
        self.main_layout.setContentsMargins(12, 8, 12, 8)

        # Header
        header = self.create_header(
            "Let's start with the clinical programming session"
        )
        self.main_layout.addWidget(header)

        # Main content area
        content_layout = QHBoxLayout()

        # Left side: Stimulation parameters
        params_group = self._create_stimulation_params_group()
        content_layout.addWidget(params_group)

        # Right side: Session scales and notes
        right_layout = QVBoxLayout()
        scales_group = self._create_session_scales_group()
        right_layout.addWidget(scales_group)
        right_layout.addWidget(create_horizontal_line())
        notes_group = self._create_notes_group()
        right_layout.addWidget(notes_group)
        content_layout.addLayout(right_layout)

        self.main_layout.addLayout(content_layout)
        self.main_layout.addStretch(1)

        # Action buttons
        button_row = QHBoxLayout()
        button_row.addStretch(1)

        self.insert_button = QPushButton("Insert")
        self.insert_button.setIcon(
            self.parent_style.standardIcon(QStyle.SP_DialogApplyButton)
        )
        self.insert_button.setMaximumWidth(120)
        button_row.addWidget(self.insert_button)

        self.close_button = QPushButton("Close session")
        self.close_button.setIcon(
            self.parent_style.standardIcon(QStyle.SP_DialogCloseButton)
        )
        self.close_button.setFixedWidth(150)
        button_row.addWidget(self.close_button)

        self.export_button = QPushButton("Export Report")
        self.export_button.setIcon(
            self.parent_style.standardIcon(QStyle.SP_DialogSaveButton)
        )
        self.export_button.setFixedWidth(150)
        
        # Create dropdown menu for export options
        self.export_menu = QMenu(self)
        
        # Excel export action
        self.export_excel_action = self.export_menu.addAction("📊 Excel Report")
        self.export_excel_action.setToolTip("Export to Excel (.xlsx) with summary statistics")
        
        # Word export action  
        self.export_word_action = self.export_menu.addAction("📄 Word Report")
        self.export_word_action.setToolTip("Export to Word (.docx) document")
        
        # PDF export action
        self.export_pdf_action = self.export_menu.addAction("📋 PDF Report")
        self.export_pdf_action.setToolTip("Export to PDF document")
        
        # Set menu to button
        self.export_button.setMenu(self.export_menu)
        
        button_row.addWidget(self.export_button)

        self.main_layout.addLayout(button_row)

    def _create_stimulation_params_group(self) -> QGroupBox:
        """Create the stimulation parameters group box."""
        gb_params = QGroupBox("Stimulation parameters")
        gb_params.setStyleSheet(
            "QGroupBox::title { color: #ff8800; font-size: 15pt; font-weight: 600; }"
        )
        gb_params.setFont(QFont("Segoe UI", 12, QFont.Bold))

        form = QFormLayout(gb_params)
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignTop)
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(10)

        freq_limits = STIMULATION_LIMITS["frequency"]
        amp_limits = STIMULATION_LIMITS["amplitude"]
        pw_limits = STIMULATION_LIMITS["pulse_width"]

        # Left electrode section
        form.addRow(QLabel(""), QLabel(""))  # Empty row for spacing
        left_electrode_label = QLabel("Left electrode")
        left_electrode_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        form.addRow(left_electrode_label, QLabel(""))

        # Left stimulation frequency
        self.session_left_stim_freq_edit = QLineEdit()
        self.session_left_stim_freq_edit.setPlaceholderText(PLACEHOLDERS["frequency"])
        self.session_left_stim_freq_edit.setFixedWidth(100)
        self.session_left_stim_freq_edit.setValidator(
            QIntValidator(freq_limits["min"], freq_limits["max"])
        )
        left_freq_widget = IncrementWidget(
            self.session_left_stim_freq_edit,
            step1=freq_limits["step"],
            decimals=0,
            min_value=freq_limits["min"],
            max_value=freq_limits["max"],
        )
        form.addRow(QLabel("Stimulation frequency:"), left_freq_widget)

        # Left Anode (-)
        self.session_left_anode_combo = MultiSelectComboBox()
        self.session_left_anode_combo.setMaximumWidth(150)
        self.session_left_anode_combo.addItems([
            "ground", "0", "1a", "1b", "1c", "1-all",
            "2a", "2b", "2c", "2-all", "3"
        ])
        anode_label = QLabel("Anode (-):")
        form.addRow(anode_label, self.session_left_anode_combo)

        # Left Cathode (+)
        self.session_left_cathode_combo = MultiSelectComboBox()
        self.session_left_cathode_combo.setMaximumWidth(150)
        self.session_left_cathode_combo.addItems([
            "ground", "0", "1a", "1b", "1c", "1-all",
            "2a", "2b", "2c", "2-all", "3"
        ])
        # Set ground as default for cathode
        self.session_left_cathode_combo.set_selected_items(["ground"])
        cathode_label = QLabel("Cathode (+):")
        form.addRow(cathode_label, self.session_left_cathode_combo)

        # Left amplitude
        self.session_left_amp_edit = QLineEdit()
        self.session_left_amp_edit.setPlaceholderText(PLACEHOLDERS["amplitude"])
        self.session_left_amp_edit.setFixedWidth(100)
        self.session_left_amp_edit.setValidator(
            QDoubleValidator(amp_limits["min"], amp_limits["max"], amp_limits["decimals"])
        )
        left_amp_widget = IncrementWidget(
            self.session_left_amp_edit,
            step1=amp_limits["step1"],
            step2=amp_limits["step2"],
            decimals=1,
            min_value=amp_limits["min"],
            max_value=amp_limits["max"],
        )
        form.addRow(QLabel("Amplitude:"), left_amp_widget)

        # Left pulse width
        self.session_left_pw_edit = QLineEdit()
        self.session_left_pw_edit.setPlaceholderText(PLACEHOLDERS["pulse_width"])
        self.session_left_pw_edit.setFixedWidth(100)
        self.session_left_pw_edit.setValidator(
            QIntValidator(pw_limits["min"], pw_limits["max"])
        )
        left_pw_widget = IncrementWidget(
            self.session_left_pw_edit,
            step1=pw_limits["step"],
            decimals=0,
            min_value=pw_limits["min"],
            max_value=pw_limits["max"],
        )
        form.addRow(QLabel("Pulse width:"), left_pw_widget)
        form.addWidget(create_horizontal_line())

        # Right electrode section
        form.addRow(QLabel(""), QLabel(""))  # Empty row for spacing
        right_electrode_label = QLabel("Right electrode")
        right_electrode_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        form.addRow(right_electrode_label, QLabel(""))

        # Right stimulation frequency
        self.session_right_stim_freq_edit = QLineEdit()
        self.session_right_stim_freq_edit.setPlaceholderText(PLACEHOLDERS["frequency"])
        self.session_right_stim_freq_edit.setFixedWidth(100)
        self.session_right_stim_freq_edit.setValidator(
            QIntValidator(freq_limits["min"], freq_limits["max"])
        )
        right_freq_widget = IncrementWidget(
            self.session_right_stim_freq_edit,
            step1=freq_limits["step"],
            decimals=0,
            min_value=freq_limits["min"],
            max_value=freq_limits["max"],
        )
        form.addRow(QLabel("Stimulation frequency:"), right_freq_widget)

        # Right Anode (-)
        self.session_right_anode_combo = MultiSelectComboBox()
        self.session_right_anode_combo.setMaximumWidth(150)
        self.session_right_anode_combo.addItems([
            "ground", "0", "1a", "1b", "1c", "1-all",
            "2a", "2b", "2c", "2-all", "3"
        ])
        anode_label_r = QLabel("Anode (-):")
        form.addRow(anode_label_r, self.session_right_anode_combo)

        # Right Cathode (+)
        self.session_right_cathode_combo = MultiSelectComboBox()
        self.session_right_cathode_combo.setMaximumWidth(150)
        self.session_right_cathode_combo.addItems([
            "ground", "0", "1a", "1b", "1c", "1-all",
            "2a", "2b", "2c", "2-all", "3"
        ])
        # Set ground as default for cathode
        self.session_right_cathode_combo.set_selected_items(["ground"])
        cathode_label_r = QLabel("Cathode (+):")
        form.addRow(cathode_label_r, self.session_right_cathode_combo)

        # Right amplitude
        self.session_right_amp_edit = QLineEdit()
        self.session_right_amp_edit.setPlaceholderText(PLACEHOLDERS["amplitude"])
        self.session_right_amp_edit.setFixedWidth(100)
        self.session_right_amp_edit.setValidator(
            QDoubleValidator(amp_limits["min"], amp_limits["max"], amp_limits["decimals"])
        )
        right_amp_widget = IncrementWidget(
            self.session_right_amp_edit,
            step1=amp_limits["step1"],
            step2=amp_limits["step2"],
            decimals=1,
            min_value=amp_limits["min"],
            max_value=amp_limits["max"],
        )
        form.addRow(QLabel("Amplitude:"), right_amp_widget)

        # Right pulse width
        self.session_right_pw_edit = QLineEdit()
        self.session_right_pw_edit.setPlaceholderText(PLACEHOLDERS["pulse_width"])
        self.session_right_pw_edit.setFixedWidth(100)
        self.session_right_pw_edit.setValidator(
            QIntValidator(pw_limits["min"], pw_limits["max"])
        )
        right_pw_widget = IncrementWidget(
            self.session_right_pw_edit,
            step1=pw_limits["step"],
            decimals=0,
            min_value=pw_limits["min"],
            max_value=pw_limits["max"],
        )
        form.addRow(QLabel("Pulse width:"), right_pw_widget)

        return gb_params

    def _create_session_scales_group(self) -> QGroupBox:
        """Create the session scales group box."""
        gb_session = QGroupBox("Session scales")
        gb_session.setStyleSheet(
            "QGroupBox::title { color: #ff8800; font-size: 15pt; font-weight: 600; }"
        )
        gb_session.setFont(QFont("Segoe UI", 12, QFont.Bold))

        self.step3_session_scales_form = QFormLayout(gb_session)
        self.step3_session_scales_form.setLabelAlignment(Qt.AlignRight)
        self.step3_session_scales_form.setFormAlignment(Qt.AlignTop)
        self.step3_session_scales_form.setHorizontalSpacing(18)
        self.step3_session_scales_form.setVerticalSpacing(10)

        return gb_session

    def _create_notes_group(self) -> QGroupBox:
        """Create the session notes group box."""
        gb_notes = QGroupBox("Session notes")
        gb_notes.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        gb_notes.setStyleSheet(
            "QGroupBox::title { color: #ff8800; font-size: 11pt; font-weight: 600; }"
        )
        gb_notes.setFont(QFont("Segoe UI", 10, QFont.Bold))

        layout = QHBoxLayout(gb_notes)
        self.session_notes_edit = QTextEdit()
        self.session_notes_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.session_notes_edit.setMinimumHeight(40)
        layout.addWidget(self.session_notes_edit)

        return gb_notes

    def update_session_scales(self, scale_names: List[str]) -> None:
        """
        Update the session scales form with the given scale names.

        Args:
            scale_names: List of scale names to display
        """
        # Clear existing form
        while self.step3_session_scales_form.rowCount():
            self.step3_session_scales_form.removeRow(0)

        self.session_scale_value_edits = []

        # Add scale inputs
        limits = SESSION_SCALE_LIMITS
        for name in scale_names:
            value_edit = QLineEdit()
            value_edit.setPlaceholderText(PLACEHOLDERS["scale_value"])
            value_edit.setFixedWidth(75)

            widget = IncrementWidget(
                value_edit,
                step1=limits["step1"],
                step2=limits["step2"],
                decimals=limits["decimals"],
                min_value=limits["min"],
                max_value=limits["max"],
            )

            self.step3_session_scales_form.addRow(QLabel(name + ":"), widget)
            self.session_scale_value_edits.append((name, value_edit))

    def set_initial_stimulation_params(
        self,
        left_frequency: str,
        left_cathode: str,
        left_anode: str,
        left_amp: str,
        left_pw: str,
        right_frequency: str,
        right_cathode: str,
        right_anode: str,
        right_amp: str,
        right_pw: str,
    ) -> None:
        """
        Set initial stimulation parameters from previous step.

        Args:
            left_frequency: Left stimulation frequency
            left_cathode: Left electrode cathode configuration
            left_anode: Left electrode anode configuration
            left_amp: Left amplitude
            left_pw: Left pulse width
            right_frequency: Right stimulation frequency
            right_cathode: Right electrode cathode configuration
            right_anode: Right electrode anode configuration
            right_amp: Right amplitude
            right_pw: Right pulse width
        """
        self.session_left_stim_freq_edit.setText(left_frequency)
        self.session_left_cathode_combo.set_selected_from_string(left_cathode)
        self.session_left_anode_combo.set_selected_from_string(left_anode)
        self.session_left_amp_edit.setText(left_amp)
        self.session_left_pw_edit.setText(left_pw)
        self.session_right_stim_freq_edit.setText(right_frequency)
        self.session_right_cathode_combo.set_selected_from_string(right_cathode)
        self.session_right_anode_combo.set_selected_from_string(right_anode)
        self.session_right_amp_edit.setText(right_amp)
        self.session_right_pw_edit.setText(right_pw)
