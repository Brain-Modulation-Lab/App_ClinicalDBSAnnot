"""
Main wizard window for the Clinical DBS Annotator application.

This module contains the main window that manages the wizard flow,
navigation, and coordinates views with the controller.
"""

import os

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QStyle,
    QVBoxLayout,
    QWidget,
)

from ..config import (
    APP_NAME,
    APP_VERSION,
    CLINICAL_SCALES_PRESETS,
    FONT_SCALE_ENABLED,
    BASE_DPI,
    ICON_FILENAME,
    ICONS_DIR,
    WINDOW_SIZE_RATIO,
    WINDOW_MIN_SIZE,
    WINDOW_MAX_SIZE_RATIO,
)
from ..controllers import WizardController
from ..utils import resource_path, get_theme_manager
from .step0_view import Step0View
from .step1_view import Step1View
from .step2_view import Step2View
from .step3_view import Step3View
from .annotations_simple_view import AnnotationsFileView, AnnotationsSessionView


class WizardWindow(QWidget):
    """
    Main window for the annotation wizard.

    This window manages:
    - Multi-step wizard interface
    - Navigation between steps
    - Controller integration
    - Window configuration and styling
    """

    def __init__(self, app):
        """
        Initialize the wizard window.

        Args:
            app: QApplication instance for screen geometry
        """
        super().__init__()
        self.app = app
        self.controller = WizardController()
        self.current_step = 0
        self.workflow_mode = None  # "full" or "annotations_only"

        # Load logo
        logo_path = resource_path(os.path.join(ICONS_DIR, ICON_FILENAME))
        self.logo_pixmap = QPixmap(logo_path)

        self._setup_window()
        self._setup_ui()
        self._update_ui_state()

    def _setup_window(self) -> None:
        """Configure the main window properties with responsive sizing."""
        self.setWindowTitle(f"{APP_NAME} {APP_VERSION}")

        # Set window icon
        icon_path = resource_path(os.path.join(ICONS_DIR, ICON_FILENAME))
        self.setWindowIcon(QIcon(icon_path))

        # Get screen geometry and DPI
        screen = self.app.primaryScreen()
        rect = screen.availableGeometry()
        screen_width = rect.width()
        screen_height = rect.height()

        # Get logical DPI for font scaling
        logical_dpi = screen.logicalDotsPerInch()
        self.dpi_scale = logical_dpi / BASE_DPI if FONT_SCALE_ENABLED else 1.0

        # Calculate desired window size with ratio
        desired_width = int(screen_width * WINDOW_SIZE_RATIO["width"])
        desired_height = int(screen_height * WINDOW_SIZE_RATIO["height"])

        # Apply minimum size constraints
        width = max(desired_width, WINDOW_MIN_SIZE["width"])
        height = max(desired_height, WINDOW_MIN_SIZE["height"])

        # Apply maximum size constraints (prevent too large on big screens)
        max_width = int(screen_width * WINDOW_MAX_SIZE_RATIO["width"])
        max_height = int(screen_height * WINDOW_MAX_SIZE_RATIO["height"])
        width = min(width, max_width)
        height = min(height, max_height)

        # Calculate position (centered)
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)

        # Set geometry and constraints
        self.setGeometry(x, y, width, height)
        self.setMinimumSize(WINDOW_MIN_SIZE["width"], WINDOW_MIN_SIZE["height"])

        # Make window resizable
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def _setup_ui(self) -> None:
        """Set up the main UI layout."""
        main_layout = QVBoxLayout(self)

        # Add theme toggle button in top-right corner
        header_layout = self._create_header()
        main_layout.addLayout(header_layout)

        # Create stacked widget for steps
        self.stack = QStackedWidget(self)

        # Create Step 0 - Mode selection
        self.step0_view = Step0View(self)
        self.stack.addWidget(self.step0_view)
        self._connect_step0_signals()

        # Full workflow views (lazy loaded)
        self.step1_view = None
        self.step2_view = None
        self.step3_view = None

        # Annotations-only workflow views (lazy loaded)
        self.annotations_file_view = None
        self.annotations_session_view = None

        main_layout.addWidget(self.stack)

        # Navigation bar
        nav_layout = self._create_nav_bar()
        main_layout.addLayout(nav_layout)

    def _create_header(self) -> QHBoxLayout:
        """
        Create header with theme toggle button.

        Returns:
            QHBoxLayout containing header elements
        """
        header_layout = QHBoxLayout()
        header_layout.addStretch()  # Push button to the right

        # Theme toggle button
        self.theme_toggle_btn = QPushButton()
        self.theme_toggle_btn.setObjectName("theme_toggle")
        self.theme_toggle_btn.setToolTip("Switch between Dark and Light mode")
        self.theme_toggle_btn.setCursor(Qt.PointingHandCursor)
        self._update_theme_button_icon()

        self.theme_toggle_btn.clicked.connect(self._toggle_theme)

        header_layout.addWidget(self.theme_toggle_btn)

        return header_layout

    def _update_theme_button_icon(self) -> None:
        """Update the theme toggle button icon based on current theme."""
        theme_manager = get_theme_manager()
        current_theme = theme_manager.get_current_theme()

        # Show the icon for what the button will switch TO
        # (opposite of current theme)
        if theme_manager.is_dark_mode():
            self.theme_toggle_btn.setText("☀")  # Sun = will switch to light
        else:
            self.theme_toggle_btn.setText("🌙")  # Moon = will switch to dark

    def _toggle_theme(self) -> None:
        """Toggle between dark and light themes."""
        theme_manager = get_theme_manager()
        theme_manager.toggle_theme(self.app)
        self._update_theme_button_icon()

    def _connect_step0_signals(self) -> None:
        """Connect Step 0 mode selection signals."""
        self.step0_view.full_mode_button.clicked.connect(self._select_full_mode)
        self.step0_view.annotations_only_button.clicked.connect(self._select_annotations_only_mode)

    def _select_full_mode(self) -> None:
        """Handle selection of full workflow mode."""
        self.workflow_mode = "full"
        self.controller.workflow_mode = "full"
        self._go_to_step1()

    def _select_annotations_only_mode(self) -> None:
        """Handle selection of annotations-only mode."""
        self.workflow_mode = "annotations_only"
        self.controller.workflow_mode = "annotations_only"
        self._go_to_annotations_file()

    def _connect_step1_signals(self) -> None:
        """Connect Step 1 view signals to controller."""
        # Connect preset buttons
        for preset_name in CLINICAL_SCALES_PRESETS.keys():
            btn = self.step1_view.get_preset_button(preset_name)
            if btn:
                btn.clicked.connect(
                    lambda checked, name=preset_name: self.controller.apply_clinical_preset(
                        name, self.step1_view
                    )
                )

        # Initialize empty clinical scales
        self.step1_view.update_clinical_scales(
            [],
            on_add_callback=lambda: self.controller.on_add_clinical_scale(
                self.step1_view
            ),
            on_remove_callback=lambda row: self.controller.on_remove_clinical_scale(
                self.step1_view, row
            ),
        )

        # Connect next button
        self.step1_view.next_button.clicked.connect(self._go_to_step2)

    def _connect_step2_signals(self) -> None:
        """Connect Step 2 view signals to controller."""
        self.controller.prepare_step2(self.step2_view)
        self.step2_view.next_button.clicked.connect(self._go_to_step3)

    def _connect_step3_signals(self) -> None:
        """Connect Step 3 view signals to controller."""
        self.controller.prepare_step3(self.step3_view)
        self.step3_view.insert_button.clicked.connect(
            lambda: self.controller.insert_session_row(self.step3_view)
        )
        self.step3_view.close_button.clicked.connect(
            lambda: self.controller.close_session(self)
        )
        self.step3_view.export_button.clicked.connect(
            lambda: self.controller.export_session_report(self)
        )
        self.step3_view.export_excel_action.triggered.connect(
            lambda: self.controller.export_session_excel(self)
        )
        self.step3_view.export_word_action.triggered.connect(
            lambda: self.controller.export_session_word(self)
        )
        self.step3_view.export_pdf_action.triggered.connect(
            lambda: self.controller.export_session_pdf(self)
        )

    def _create_nav_bar(self) -> QHBoxLayout:
        """
        Create the navigation bar with back button.

        Returns:
            QHBoxLayout containing navigation controls
        """
        nav_layout = QHBoxLayout()

        self.back_button = QPushButton("Back")
        self.back_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowBack))
        self.back_button.setIconSize(QSize(22, 22))
        self.back_button.setFixedWidth(140)
        self.back_button.clicked.connect(self._go_back)

        nav_layout.addWidget(self.back_button)
        nav_layout.addStretch()

        return nav_layout

    def _go_to_step1(self) -> None:
        """Navigate to Step 1 (full workflow)."""
        # Create Step 1 if needed
        if self.step1_view is None:
            self.step1_view = Step1View(self.logo_pixmap, self.style())
            self.stack.addWidget(self.step1_view)
            self._connect_step1_signals()

        self.current_step = 1
        self.stack.setCurrentWidget(self.step1_view)
        self._update_ui_state()

    def _go_to_annotations_file(self) -> None:
        """Navigate to annotations file selection (annotations-only workflow)."""
        # Create annotations file view if needed
        if self.annotations_file_view is None:
            self.annotations_file_view = AnnotationsFileView(self)
            self.stack.addWidget(self.annotations_file_view)
            self._connect_annotations_file_signals()

        self.current_step = 1  # First step after mode selection
        self.stack.setCurrentWidget(self.annotations_file_view)
        self._update_ui_state()

    def _connect_annotations_file_signals(self) -> None:
        """Connect signals for annotations file view."""
        self.annotations_file_view.browse_button.clicked.connect(
            lambda: self.controller.browse_save_location_simple(self.annotations_file_view, self)
        )
        self.annotations_file_view.next_button.clicked.connect(self._go_to_annotations_session)

    def _go_to_annotations_session(self) -> None:
        """Navigate to annotations session (annotations-only workflow)."""
        # Validate file info
        if not self.controller.validate_annotations_file(self.annotations_file_view, self):
            return

        # Create annotations session view if needed
        if self.annotations_session_view is None:
            self.annotations_session_view = AnnotationsSessionView(self)
            self.stack.addWidget(self.annotations_session_view)
            self._connect_annotations_session_signals()

        self.current_step = 2
        self.stack.setCurrentWidget(self.annotations_session_view)
        self._update_ui_state()

    def _connect_annotations_session_signals(self) -> None:
        """Connect signals for annotations session view."""
        self.annotations_session_view.insert_button.clicked.connect(
            lambda: self.controller.insert_simple_annotation(self.annotations_session_view)
        )
        self.annotations_session_view.close_button.clicked.connect(
            lambda: self.controller.close_session(self)
        )

    def _go_to_step2(self) -> None:
        """Navigate to Step 2 after validating Step 1."""
        if not self.controller.validate_step1(self.step1_view, self):
            return

        # Create Step 2 if needed
        if self.step2_view is None:
            self.step2_view = Step2View(self.logo_pixmap, self.style())
            self.stack.addWidget(self.step2_view)
            self._connect_step2_signals()

        self.current_step = 2
        self.stack.setCurrentWidget(self.step2_view)
        self._update_ui_state()

    def _go_to_step3(self) -> None:
        """Navigate to Step 3 after validating Step 2."""
        if not self.controller.validate_step2(self.step2_view):
            return

        # Create Step 3 if needed
        if self.step3_view is None:
            self.step3_view = Step3View(self.logo_pixmap, self.style())
            self.stack.addWidget(self.step3_view)
            self._connect_step3_signals()
        else:
            # Update if already created
            self.controller.prepare_step3(self.step3_view)

        self.current_step = 3
        self.stack.setCurrentWidget(self.step3_view)
        self._update_ui_state()

    def _go_back(self) -> None:
        """Navigate to the previous step."""
        if self.current_step > 0:
            self.current_step -= 1

            # Determine which widget to show based on workflow and step
            if self.current_step == 0:
                self.stack.setCurrentWidget(self.step0_view)
            elif self.workflow_mode == "full":
                if self.current_step == 1 and self.step1_view:
                    self.stack.setCurrentWidget(self.step1_view)
                elif self.current_step == 2 and self.step2_view:
                    self.stack.setCurrentWidget(self.step2_view)
            elif self.workflow_mode == "annotations_only":
                if self.current_step == 1 and self.annotations_file_view:
                    self.stack.setCurrentWidget(self.annotations_file_view)

            self._update_ui_state()

    def _update_ui_state(self) -> None:
        """Update UI elements based on current step."""
        # Disable back button on step 0 (mode selection)
        self.back_button.setEnabled(self.current_step > 0)
