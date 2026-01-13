"""
Session data management model.

This module contains the main SessionData class that manages all data
for a clinical DBS programming session, including TSV file writing.
"""

import csv
from datetime import datetime
from pathlib import Path
from typing import List, Optional, TextIO

import pytz

from ..config import TSV_COLUMNS, TIMEZONE
from .clinical_scale import ClinicalScale, SessionScale
from .stimulation import StimulationParameters


class SessionData:
    """
    Manages all data for a clinical DBS programming session.

    This class handles:
    - TSV file creation and writing
    - Block ID tracking
    - Clinical and session scales management
    - Stimulation parameters tracking
    """

    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize a new session.

        Args:
            file_path: Path to the TSV file where data will be saved
        """
        self.file_path = file_path
        self.tsv_file: Optional[TextIO] = None
        self.tsv_writer: Optional[csv.DictWriter] = None
        self.block_id: int = 0
        self.session_start_time: Optional[datetime] = None

        if file_path:
            self.open_file(file_path)

    def open_file(self, file_path: str) -> None:
        """
        Open a TSV file for writing and initialize the CSV writer.

        Args:
            file_path: Path to the TSV file
        """
        self.file_path = file_path
        self.tsv_file = open(file_path, "w", newline="", encoding="utf-8")
        self.tsv_writer = csv.DictWriter(
            self.tsv_file, fieldnames=TSV_COLUMNS, delimiter="\t"
        )
        self.tsv_writer.writeheader()
        self.session_start_time = datetime.now()

    def is_file_open(self) -> bool:
        """
        Check if a TSV file is currently open.

        Returns:
            True if file is open, False otherwise
        """
        return self.tsv_file is not None and self.tsv_writer is not None

    def close_file(self) -> None:
        """Close the TSV file if it's open."""
        if self.tsv_file:
            self.tsv_file.close()
            self.tsv_file = None
            self.tsv_writer = None

    def write_clinical_scales(
        self,
        scales: List[ClinicalScale],
        stimulation: StimulationParameters,
        notes: str = "",
    ) -> None:
        """
        Write clinical scales data to the TSV file.

        Args:
            scales: List of clinical scales to write
            stimulation: Stimulation parameters
            notes: Additional notes for this entry
        """
        if not self.tsv_writer:
            raise ValueError("TSV file not opened. Call open_file() first.")

        today = datetime.now().strftime("%Y-%m-%d")
        stim_dict = stimulation.to_dict()

        # If no scales have values, write a single row with null scale data
        valid_scales = [s for s in scales if s.is_valid()]
        if not valid_scales:
            row = {
                "date": today,
                "time": "0",
                "block_id": self.block_id,
                "scale_name": None,
                "scale_value": None,
                "notes": notes,
                **stim_dict,
            }
            self.tsv_writer.writerow(row)
        else:
            # Write one row per scale
            for scale in valid_scales:
                row = {
                    "date": today,
                    "time": "0",
                    "block_id": self.block_id,
                    "scale_name": scale.name,
                    "scale_value": scale.value,
                    "notes": notes,
                    **stim_dict,
                }
                self.tsv_writer.writerow(row)

        self.tsv_file.flush()
        self.block_id += 1

    def write_session_scales(
        self,
        scales: List[SessionScale],
        stimulation: StimulationParameters,
        notes: str = "",
    ) -> None:
        """
        Write session scales data to the TSV file with current timestamp.

        Args:
            scales: List of session scales to write
            stimulation: Stimulation parameters
            notes: Additional notes for this entry
        """
        if not self.tsv_writer:
            raise ValueError("TSV file not opened. Call open_file() first.")

        # Get current time in Eastern timezone
        tz = pytz.timezone(TIMEZONE)
        now_et = datetime.now(tz)
        time_str = now_et.strftime("%H:%M:%S")
        today = datetime.now().strftime("%Y-%m-%d")
        stim_dict = stimulation.to_dict()

        # If no scales have values, write a single row with null scale data
        valid_scales = [s for s in scales if s.has_value()]
        if not valid_scales:
            row = {
                "date": today,
                "time": time_str,
                "block_id": self.block_id,
                "scale_name": None,
                "scale_value": None,
                "notes": notes,
                **stim_dict,
            }
            self.tsv_writer.writerow(row)
        else:
            # Write one row per scale
            for scale in valid_scales:
                row = {
                    "date": today,
                    "time": time_str,
                    "block_id": self.block_id,
                    "scale_name": scale.name,
                    "scale_value": scale.current_value,
                    "notes": notes,
                    **stim_dict,
                }
                self.tsv_writer.writerow(row)

        self.tsv_file.flush()
        self.block_id += 1

    def is_file_open(self) -> bool:
        """Check if a TSV file is currently open."""
        return self.tsv_file is not None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures file is closed."""
        self.close_file()

    def __del__(self):
        """Destructor - ensures file is closed."""
        self.close_file()

    # ============================================
    # Annotations-Only Workflow Methods
    # ============================================

    def initialize_simple_file(self, filepath: str) -> None:
        """
        Initialize a simple TSV file for annotations-only mode.

        Args:
            filepath: Full path to the TSV file to create

        Raises:
            ValueError: If a file is already open
            IOError: If file cannot be created
        """
        if self.is_file_open():
            raise ValueError("A file is already open. Close it before initializing a new one.")

        # Create the file with headers
        self.tsv_file = open(filepath, "w", newline="", encoding="utf-8")

        # Simple header: only time and annotation
        fieldnames = ["time", "annotation"]

        self.tsv_writer = csv.DictWriter(
            self.tsv_file,
            fieldnames=fieldnames,
            delimiter="\t"
        )
        self.tsv_writer.writeheader()
        self.tsv_file.flush()

    def write_simple_annotation(self, annotation: str) -> None:
        """
        Write a simple annotation with timestamp.

        Args:
            annotation: The annotation text to write

        Raises:
            ValueError: If no file is open
        """
        if not self.is_file_open():
            raise ValueError("No file is open. Call initialize_simple_file first.")

        # Get current time
        from datetime import datetime
        import pytz

        time_str = datetime.now(pytz.timezone("Europe/Rome")).strftime("%H:%M:%S")

        # Write row
        row = {
            "time": time_str,
            "annotation": annotation,
        }
        self.tsv_writer.writerow(row)
        self.tsv_file.flush()
