"""
database.py - DatabaseManager Class
====================================
Handles all SQLite database operations:
- Creating the database and table
- Saving calculations
- Retrieving history
- Clearing history

SQLite is a lightweight database stored as a single file (history.db).
No server needed - perfect for desktop apps!
"""

import sqlite3
from datetime import datetime


class DatabaseManager:
    """
    Manages all database operations for the calculator.
    
    Uses SQLite - a file-based database (no server needed).
    The database file 'history.db' is created automatically.
    """

    def __init__(self, db_name="history.db"):
        """
        Constructor: Called when DatabaseManager() is created.
        
        Args:
            db_name (str): Name of the SQLite database file
        """
        self.db_name = db_name
        self.connection = None  # Will hold our DB connection
        self.cursor = None      # Will execute SQL commands
        self._connect()         # Connect on startup
        self._create_table()    # Create table if not exists

    def _connect(self):
        """
        Opens connection to SQLite database.
        Creates the file if it doesn't exist yet.
        """
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        print(f"[DB] Connected to {self.db_name}")

    def _create_table(self):
        """
        Creates the 'history' table if it doesn't already exist.
        
        Table structure:
        - id: Auto-incremented unique number (PRIMARY KEY)
        - expression: What the user typed (e.g., "10+20")
        - result: The answer (e.g., "30")
        - timestamp: When it was calculated (auto-set by SQLite)
        """
        create_sql = """
            CREATE TABLE IF NOT EXISTS history (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                expression TEXT NOT NULL,
                result    TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        self.cursor.execute(create_sql)
        self.connection.commit()
        print("[DB] Table 'history' ready.")

    def save_calculation(self, expression, result):
        """
        Saves one calculation to the database.
        
        Args:
            expression (str): e.g., "10+20" or "sqrt(25)"
            result     (str): e.g., "30" or "5.0"
        
        Example:
            db.save_calculation("10+20", "30")
            → INSERT INTO history(expression, result) VALUES ('10+20', '30')
        """
        insert_sql = "INSERT INTO history (expression, result) VALUES (?, ?)"
        # '?' placeholders prevent SQL injection attacks
        self.cursor.execute(insert_sql, (expression, result))
        self.connection.commit()
        print(f"[DB] Saved: {expression} = {result}")

    def get_history(self, limit=100):
        """
        Retrieves calculation history, newest first.
        
        Args:
            limit (int): Maximum number of records to return
        
        Returns:
            List of tuples: [(id, expression, result, timestamp), ...]
        
        Example:
            [(1, '10+20', '30', '2026-01-01 10:00:00'), ...]
        """
        select_sql = """
            SELECT id, expression, result, timestamp
            FROM history
            ORDER BY id DESC
            LIMIT ?
        """
        self.cursor.execute(select_sql, (limit,))
        rows = self.cursor.fetchall()
        return rows

    def clear_history(self):
        """
        Deletes ALL records from the history table.
        Also resets the auto-increment counter.
        """
        self.cursor.execute("DELETE FROM history")
        # Reset the auto-increment counter
        self.cursor.execute("DELETE FROM sqlite_sequence WHERE name='history'")
        self.connection.commit()
        print("[DB] History cleared.")

    def get_total_count(self):
        """Returns the total number of calculations stored."""
        self.cursor.execute("SELECT COUNT(*) FROM history")
        count = self.cursor.fetchone()[0]
        return count

    def close(self):
        """Closes the database connection. Call this when app exits."""
        if self.connection:
            self.connection.close()
            print("[DB] Connection closed.")