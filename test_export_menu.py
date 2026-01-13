#!/usr/bin/env python3
"""
Test script to verify the new export menu functionality.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import pandas as pd
from PyQt5.QtWidgets import QApplication, QPushButton, QMenu, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

def test_export_menu():
    """Test the export menu functionality."""
    app = QApplication(sys.argv)
    
    # Create a test window
    window = QWidget()
    window.setWindowTitle("Export Menu Test")
    window.setGeometry(100, 100, 300, 200)
    
    layout = QVBoxLayout(window)
    
    # Create export button with menu
    export_button = QPushButton("Export Report")
    export_button.setIcon(app.style().standardIcon(QApplication.style().SP_DialogSaveButton))
    export_button.setFixedWidth(150)
    
    # Create dropdown menu for export options
    export_menu = QMenu(window)
    
    # Excel export action
    export_excel_action = export_menu.addAction("📊 Excel Report")
    export_excel_action.setToolTip("Export to Excel (.xlsx) with summary statistics")
    
    # Word export action  
    export_word_action = export_menu.addAction("📄 Word Report")
    export_word_action.setToolTip("Export to Word (.docx) document")
    
    # PDF export action
    export_pdf_action = export_menu.addAction("📋 PDF Report")
    export_pdf_action.setToolTip("Export to PDF document")
    
    # Set menu to button
    export_button.setMenu(export_menu)
    
    # Add button to layout
    layout.addWidget(export_button)
    
    # Connect actions to test functions
    def on_excel():
        print("Excel export selected!")
        
    def on_word():
        print("Word export selected!")
        
    def on_pdf():
        print("PDF export selected!")
    
    export_excel_action.triggered.connect(on_excel)
    export_word_action.triggered.connect(on_word)
    export_pdf_action.triggered.connect(on_pdf)
    
    window.show()
    
    print("Test window opened. Click the dropdown arrow on the Export Report button to test the menu.")
    print("Menu options should appear:")
    print("- 📊 Excel Report")
    print("- 📄 Word Report") 
    print("- 📋 PDF Report")
    
    return app.exec_()

if __name__ == "__main__":
    test_export_menu()
