"""
export.py - ExportManager Class
=================================
Handles exporting calculation history to CSV format.

CSV (Comma-Separated Values) is a plain text format that opens
in Excel, Google Sheets, or any spreadsheet app.

Output looks like:
    ID,Expression,Result,Timestamp
    1,10+20,30,2026-01-01 10:00:00
    2,sqrt(25),5.0,2026-01-01 10:01:00
"""

import csv
import os
from datetime import datetime
from tkinter import filedialog, messagebox


class ExportManager:
    """
    Manages exporting calculator history to CSV files.
    
    Uses Python's built-in 'csv' module - no pip install needed!
    Opens a file-save dialog so the user picks where to save.
    """

    def __init__(self, db_manager):
        """
        Constructor.
        
        Args:
            db_manager: DatabaseManager instance to read history from
        """
        self.db = db_manager

    def export_to_csv(self, parent_window=None):
        """
        Exports full calculation history to a CSV file.
        
        Steps:
        1. Open a "Save File" dialog for user to choose location
        2. Fetch all history from database
        3. Write to CSV with headers
        4. Show success or error message
        
        Args:
            parent_window: Tkinter window (for dialog positioning)
        
        Returns:
            str or None: Path to saved file, or None if cancelled/error
        """
        # ── Step 1: Ask user where to save the file ──────────────────
        # Default filename includes today's date
        default_name = f"calculator_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        file_path = filedialog.asksaveasfilename(
            parent=parent_window,
            defaultextension=".csv",
            initialfile=default_name,
            filetypes=[
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ],
            title="Export History as CSV"
        )

        # User cancelled the dialog
        if not file_path:
            print("[Export] User cancelled export.")
            return None

        # ── Step 2: Fetch data from database ─────────────────────────
        history = self.db.get_history(limit=10000)  # Get all records

        if not history:
            messagebox.showinfo(
                "No Data",
                "No calculation history to export.\nMake some calculations first!",
                parent=parent_window
            )
            return None

        # ── Step 3: Write CSV file ────────────────────────────────────
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)

                # Write header row
                writer.writerow(["ID", "Expression", "Result", "Timestamp"])

                # Write each calculation row
                for row in history:
                    writer.writerow(row)

            # ── Step 4: Show success message ──────────────────────────
            record_count = len(history)
            messagebox.showinfo(
                "Export Successful! ✓",
                f"Successfully exported {record_count} calculation(s)!\n\n"
                f"Saved to:\n{file_path}",
                parent=parent_window
            )
            print(f"[Export] Exported {record_count} records to {file_path}")
            return file_path

        except PermissionError:
            messagebox.showerror(
                "Permission Error",
                "Cannot save to that location.\nTry a different folder (e.g., Desktop).",
                parent=parent_window
            )
            return None
        except Exception as e:
            messagebox.showerror(
                "Export Error",
                f"Failed to export history:\n{str(e)}",
                parent=parent_window
            )
            return None

    def get_export_summary(self):
        """
        Returns a summary string about the export data.
        Used to show the user what will be exported.
        
        Returns:
            str: Summary like "100 calculations ready to export"
        """
        count = self.db.get_total_count()
        if count == 0:
            return "No calculations to export yet."
        elif count == 1:
            return "1 calculation ready to export."
        else:
            return f"{count} calculations ready to export."