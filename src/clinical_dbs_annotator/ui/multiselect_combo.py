"""
Multi-select combo box widget.

A custom combo box that allows multiple selections with checkboxes.
"""

from typing import List

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QComboBox


class MultiSelectComboBox(QComboBox):
    """
    A combo box that supports multiple selections using checkboxes.

    Displays selected items as comma-separated text in the combo box.
    """

    selectionChanged = pyqtSignal()

    def __init__(self, parent=None):
        """Initialize the multi-select combo box."""
        super().__init__(parent)

        # Make combo box editable to show custom text
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)

        # Create model for items
        self.model_items = QStandardItemModel(self)
        self.setModel(self.model_items)

        # Set view properties
        view = self.view()
        view.pressed.connect(self.on_item_pressed)

        # Install event filter to detect clicks outside
        view.viewport().installEventFilter(self)

        # Store item list
        self.items = []
        self._skip_next_hide = False

    def addItems(self, items: List[str]) -> None:
        """
        Add items to the combo box.

        Args:
            items: List of item strings to add
        """
        self.items = items
        for item_text in items:
            item = QStandardItem(item_text)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setData(Qt.Unchecked, Qt.CheckStateRole)
            self.model_items.appendRow(item)

    def on_item_pressed(self, index) -> None:
        """
        Handle item press event to toggle checkbox.

        Args:
            index: Model index of the pressed item
        """
        item = self.model_items.itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
        self.update_text()
        self.selectionChanged.emit()
        # Don't close popup when selecting items
        self._skip_next_hide = True

    def update_text(self) -> None:
        """Update the combo box display text with selected items."""
        selected = []
        for i in range(self.model_items.rowCount()):
            item = self.model_items.item(i)
            if item.checkState() == Qt.Checked:
                selected.append(item.text())

        if selected:
            # Show selections with underscore separator for clarity
            self.setEditText("_".join(selected))
        else:
            self.setEditText("")

    def get_selected_items(self) -> List[str]:
        """
        Get list of selected item texts.

        Returns:
            List of selected item strings
        """
        selected = []
        for i in range(self.model_items.rowCount()):
            item = self.model_items.item(i)
            if item.checkState() == Qt.Checked:
                selected.append(item.text())
        return selected

    def get_selected_text(self) -> str:
        """
        Get selected items joined with underscore.

        Returns:
            String with selected items joined by underscore (e.g., "0_1-all")
        """
        selected = self.get_selected_items()
        return "_".join(selected) if selected else ""

    def set_selected_items(self, items: List[str]) -> None:
        """
        Set which items are selected.

        Args:
            items: List of item texts to select
        """
        # Clear all selections
        for i in range(self.model_items.rowCount()):
            item = self.model_items.item(i)
            item.setCheckState(Qt.Unchecked)

        # Set specified selections
        for i in range(self.model_items.rowCount()):
            item = self.model_items.item(i)
            if item.text() in items:
                item.setCheckState(Qt.Checked)

        self.update_text()

    def set_selected_from_string(self, value: str) -> None:
        """
        Set selected items from underscore-separated string.

        Args:
            value: String with items separated by underscore (e.g., "0_1-all")
        """
        if not value:
            self.set_selected_items([])
        else:
            items = value.split("_")
            self.set_selected_items(items)

    def hidePopup(self) -> None:
        """Override to control when popup closes."""
        # If we're in the middle of selecting an item, don't close
        if self._skip_next_hide:
            self._skip_next_hide = False
            return
        # Otherwise, allow normal closing behavior
        super().hidePopup()

    def showPopup(self) -> None:
        """Show the popup."""
        super().showPopup()

    def eventFilter(self, obj, event) -> bool:
        """
        Event filter to handle clicks and key presses.

        Args:
            obj: Object that triggered the event
            event: The event

        Returns:
            True if event was handled, False otherwise
        """
        # Allow closing with Escape key
        if event.type() == event.KeyPress and event.key() == Qt.Key_Escape:
            self.hidePopup()
            return True

        return False
