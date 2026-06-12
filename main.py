"""
main.py - Application Entry Point
====================================
This is the file you RUN to start the calculator.

    python main.py

It creates the Tkinter root window and hands it to
the Calculator class which builds everything else.

Think of this as the "ignition key" of the app.
"""

import tkinter as tk
from calculator import Calculator


def main():
    """
    Main function - starts the application.
    
    Steps:
    1. Create the root Tkinter window (the OS window frame)
    2. Pass it to Calculator which builds all the UI inside it
    3. Set the close handler
    4. Start the event loop (mainloop) - this waits for user input
    """
    # ── Step 1: Create Root Window ────────────────────────────────────
    root = tk.Tk()

    # Window title and icon setup
    root.title("Advanced Scientific Calculator")

    # Minimum window size
    root.minsize(400, 600)

    # ── Step 2: Create Calculator ─────────────────────────────────────
    # Calculator.__init__() builds the entire UI
    app = Calculator(root)

    # ── Step 3: Set Close Handler ─────────────────────────────────────
    # When user clicks the X button, call app.on_close()
    # This ensures the database connection is closed cleanly
    root.protocol("WM_DELETE_WINDOW", app.on_close)

    # ── Step 4: Start Event Loop ──────────────────────────────────────
    # mainloop() keeps the window open and listens for:
    # - Button clicks
    # - Key presses
    # - Window resize
    # - Any other events
    # It runs until the window is closed.
    print("[App] Starting event loop...")
    root.mainloop()
    print("[App] Application closed.")


# This block only runs when you execute: python main.py
# It does NOT run if someone imports this file as a module
if __name__ == "__main__":
    main()