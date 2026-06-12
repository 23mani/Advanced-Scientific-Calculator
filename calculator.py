"""
calculator.py - Calculator Class (Main GUI)
=============================================
The heart of the application.

This class builds the entire Tkinter GUI:
- Display screen
- Number & operator buttons
- Scientific function buttons
- History window
- Keyboard shortcuts
- Theme switching

It connects to DatabaseManager, ThemeManager, and ExportManager.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math

from database import DatabaseManager
from themes import ThemeManager
from export import ExportManager


class Calculator:
    """
    Main Calculator class.
    
    Builds the GUI and handles all user interactions.
    Uses composition (has-a relationship) to use other manager classes.
    """

    def __init__(self, root):
        """
        Constructor - sets up everything when app starts.
        
        Args:
            root: The Tkinter root window (tk.Tk())
        """
        self.root = root
        self.root.title("Advanced Scientific Calculator")
        self.root.resizable(False, False)

        # ── Initialize Manager Classes ────────────────────────────────
        self.db      = DatabaseManager("history.db")     # Database
        self.theme   = ThemeManager("dark")              # Themes
        self.export  = ExportManager(self.db)            # CSV Export

        # ── Calculator State Variables ────────────────────────────────
        self.expression = ""        # Current expression string
        self.memory     = 0.0       # Memory storage (M+, M-, MR)
        self.result_shown = False   # True after = is pressed

        # ── Build the GUI ─────────────────────────────────────────────
        self._build_ui()
        self._bind_keyboard()

        # ── Apply Initial Theme ───────────────────────────────────────
        self._apply_theme()

        # Center the window on screen
        self._center_window()

        print("[App] Calculator started successfully!")

    # ═══════════════════════════════════════════════════════════════════
    # UI BUILDING METHODS
    # ═══════════════════════════════════════════════════════════════════

    def _build_ui(self):
        """Builds all UI components in order."""
        self._build_display()
        self._build_buttons()
        self._build_utility_bar()

    def _build_display(self):
        """
        Creates the calculator display (the screen at the top).
        Uses two labels:
        - expression_label: shows what you're typing (smaller, gray)
        - display: shows the current number/result (large, bright)
        """
        c = self.theme.get_colors()

        # Outer frame for the display area
        self.display_frame = tk.Frame(
            self.root,
            bg=c["display_bg"],
            pady=10, padx=10
        )
        self.display_frame.pack(fill="x")

        # Small label showing the full expression (e.g., "10+20=")
        self.expr_var = tk.StringVar(value="")
        self.expression_label = tk.Label(
            self.display_frame,
            textvariable=self.expr_var,
            bg=c["display_bg"],
            fg=c["label_fg"],
            font=("Consolas", 11),
            anchor="e",          # Right-align
            width=30
        )
        self.expression_label.pack(fill="x")

        # Main display - shows current input or result
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Label(
            self.display_frame,
            textvariable=self.display_var,
            bg=c["display_bg"],
            fg=c["display_fg"],
            font=("Consolas", 28, "bold"),
            anchor="e",          # Right-align (like real calculators)
            width=20,
            height=2
        )
        self.display.pack(fill="x")

    def _build_buttons(self):
        """
        Creates all calculator buttons in a grid layout.
        
        Button layout:
        Row 0: [MC] [MR] [M+] [M-]     ← Memory buttons
        Row 1: [sin][cos][tan][log][√]  ← Scientific row 1
        Row 2: [x²][x^y][!] [π] [e]    ← Scientific row 2
        Row 3: [C]  [⌫] [%]  [÷]       ← Clear/ops
        Row 4: [7]  [8]  [9]  [×]       ← Numbers
        Row 5: [4]  [5]  [6]  [-]       ← Numbers
        Row 6: [1]  [2]  [3]  [+]       ← Numbers
        Row 7: [0]       [.]  [=]       ← Numbers + equals
        """
        c = self.theme.get_colors()

        # Container frame for all buttons
        self.btn_frame = tk.Frame(self.root, bg=c["bg"], pady=5)
        self.btn_frame.pack(fill="both", expand=True)

        # We'll store ALL buttons in this list for theme switching
        self.all_buttons = []

        # ── Button definitions ────────────────────────────────────────
        # Format: (text, row, col, colspan, color_key, command)
        buttons = [
            # Memory row
            ("MC",   0, 0, 1, "hist_bg",  self.memory_clear),
            ("MR",   0, 1, 1, "hist_bg",  self.memory_recall),
            ("M+",   0, 2, 1, "hist_bg",  self.memory_add),
            ("M-",   0, 3, 1, "hist_bg",  self.memory_subtract),

            # Scientific row 1
            ("sin",  1, 0, 1, "sci_bg",   lambda: self._sci_func("sin")),
            ("cos",  1, 1, 1, "sci_bg",   lambda: self._sci_func("cos")),
            ("tan",  1, 2, 1, "sci_bg",   lambda: self._sci_func("tan")),
            ("log",  1, 3, 1, "sci_bg",   lambda: self._sci_func("log")),
            ("√",    1, 4, 1, "sci_bg",   lambda: self._sci_func("sqrt")),

            # Scientific row 2
            ("x²",   2, 0, 1, "sci_bg",   lambda: self._sci_func("sq")),
            ("xʸ",   2, 1, 1, "sci_bg",   lambda: self.click("**")),
            ("n!",   2, 2, 1, "sci_bg",   lambda: self._sci_func("fact")),
            ("π",    2, 3, 1, "sci_bg",   lambda: self.click(str(round(math.pi, 8)))),
            ("e",    2, 4, 1, "sci_bg",   lambda: self.click(str(round(math.e, 8)))),

            # Control row
            ("C",    3, 0, 1, "clear_bg", self.clear),
            ("⌫",    3, 1, 1, "back_bg",  self.backspace),
            ("%",    3, 2, 1, "op_bg",    lambda: self.click("%")),
            ("÷",    3, 3, 1, "op_bg",    lambda: self.click("/")),
            ("±",    3, 4, 1, "op_bg",    self.negate),

            # Number rows
            ("7",    4, 0, 1, "num_bg",   lambda: self.click("7")),
            ("8",    4, 1, 1, "num_bg",   lambda: self.click("8")),
            ("9",    4, 2, 1, "num_bg",   lambda: self.click("9")),
            ("×",    4, 3, 1, "op_bg",    lambda: self.click("*")),
            ("ln",   4, 4, 1, "sci_bg",   lambda: self._sci_func("ln")),

            ("4",    5, 0, 1, "num_bg",   lambda: self.click("4")),
            ("5",    5, 1, 1, "num_bg",   lambda: self.click("5")),
            ("6",    5, 2, 1, "num_bg",   lambda: self.click("6")),
            ("-",    5, 3, 1, "op_bg",    lambda: self.click("-")),
            ("(",    5, 4, 1, "sci_bg",   lambda: self.click("(")),

            ("1",    6, 0, 1, "num_bg",   lambda: self.click("1")),
            ("2",    6, 1, 1, "num_bg",   lambda: self.click("2")),
            ("3",    6, 2, 1, "num_bg",   lambda: self.click("3")),
            ("+",    6, 3, 1, "op_bg",    lambda: self.click("+")),
            (")",    6, 4, 1, "sci_bg",   lambda: self.click(")")),

            ("0",    7, 0, 2, "num_bg",   lambda: self.click("0")),  # colspan=2
            (".",    7, 2, 1, "num_bg",   lambda: self.click(".")),
            ("=",    7, 3, 2, "eq_bg",    self.calculate),           # colspan=2
        ]

        # ── Create each button ────────────────────────────────────────
        for (text, row, col, colspan, color_key, cmd) in buttons:
            self._make_button(text, row, col, colspan, color_key, cmd)

    def _make_button(self, text, row, col, colspan, color_key, cmd):
        """
        Helper: Creates a single styled button and adds it to the grid.
        
        Args:
            text      (str): Button label
            row       (int): Grid row
            col       (int): Grid column
            colspan   (int): How many columns the button spans
            color_key (str): Theme color key (e.g., "num_bg")
            cmd       : Function to call when clicked
        """
        c = self.theme.get_colors()

        btn = tk.Button(
            self.btn_frame,
            text=text,
            font=("Segoe UI", 13, "bold"),
            bg=c[color_key],
            fg=c[color_key.replace("_bg", "_fg")],
            activebackground=c.get(color_key.replace("_bg", "_active"), c[color_key]),
            activeforeground=c[color_key.replace("_bg", "_fg")],
            relief="flat",          # No 3D border - modern look
            bd=0,
            cursor="hand2",         # Hand cursor on hover
            width=5 if colspan == 1 else 11,
            height=2,
            command=cmd
        )
        btn.grid(
            row=row, column=col,
            columnspan=colspan,
            padx=3, pady=3,
            sticky="nsew"           # Stretch to fill cell
        )

        # Configure grid weights so buttons resize proportionally
        self.btn_frame.grid_columnconfigure(col, weight=1)
        self.btn_frame.grid_rowconfigure(row, weight=1)

        # Store button info for theme switching
        self.all_buttons.append((btn, color_key))

    def _build_utility_bar(self):
        """
        Creates the bottom utility bar with:
        - History button
        - Export button
        - Theme toggle button
        """
        c = self.theme.get_colors()

        self.util_frame = tk.Frame(self.root, bg=c["bg"], pady=5)
        self.util_frame.pack(fill="x", padx=5)

        # History button
        self.hist_btn = tk.Button(
            self.util_frame,
            text="📋 History",
            font=("Segoe UI", 10),
            bg=c["hist_bg"], fg=c["hist_fg"],
            relief="flat", bd=0, cursor="hand2",
            command=self.show_history
        )
        self.hist_btn.pack(side="left", padx=5)

        # Export CSV button
        self.export_btn = tk.Button(
            self.util_frame,
            text="💾 Export CSV",
            font=("Segoe UI", 10),
            bg=c["sci_bg"], fg=c["sci_fg"],
            relief="flat", bd=0, cursor="hand2",
            command=lambda: self.export.export_to_csv(self.root)
        )
        self.export_btn.pack(side="left", padx=5)

        # Theme toggle button
        self.theme_btn = tk.Button(
            self.util_frame,
            text=self.theme.get_theme_button_label(),
            font=("Segoe UI", 10),
            bg=c["theme_bg"], fg=c["theme_fg"],
            relief="flat", bd=0, cursor="hand2",
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="right", padx=5)

    # ═══════════════════════════════════════════════════════════════════
    # CORE CALCULATOR LOGIC
    # ═══════════════════════════════════════════════════════════════════

    def click(self, value):
        """
        Called when any number or operator button is pressed.
        Appends the value to the current expression.
        
        Args:
            value (str): Character to add (e.g., "5", "+", ".")
        """
        # If a result was just shown and user types a number, start fresh
        if self.result_shown and value not in ('+', '-', '*', '/', '**', '%'):
            self.expression = ""
            self.result_shown = False

        self.expression += str(value)
        self.display_var.set(self.expression)

    def clear(self):
        """Clears the display and resets everything."""
        self.expression = ""
        self.display_var.set("0")
        self.expr_var.set("")
        self.result_shown = False
        print("[Calc] Cleared.")

    def backspace(self):
        """Removes the last character from the expression."""
        if self.expression:
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression if self.expression else "0")

    def negate(self):
        """Toggles positive/negative sign."""
        if self.expression and self.expression != "0":
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression
            self.display_var.set(self.expression)

    def calculate(self):
        """
        THE MAIN FUNCTION: Evaluates the expression and shows result.
        
        Process:
        1. Save original expression for display/history
        2. Prepare expression (replace ÷ with /, etc.)
        3. Evaluate using Python's eval()
        4. Show result and save to database
        5. Handle all error types gracefully
        
        ⚠️ Security note: eval() can be dangerous in web apps,
           but is fine for a local desktop calculator.
        """
        if not self.expression:
            return

        original_expr = self.expression

        try:
            # ── Prepare the expression for Python's eval() ────────────
            eval_expr = self.expression
            
            # Replace display symbols with Python operators
            eval_expr = eval_expr.replace("÷", "/")
            eval_expr = eval_expr.replace("×", "*")
            eval_expr = eval_expr.replace("^", "**")

            # ── Evaluate the expression ───────────────────────────────
            # We pass math functions as context so sqrt(4) works!
            math_context = {
                "sin":   lambda x: math.sin(math.radians(x)),
                "cos":   lambda x: math.cos(math.radians(x)),
                "tan":   lambda x: math.tan(math.radians(x)),
                "sqrt":  math.sqrt,
                "log":   math.log10,
                "ln":    math.log,
                "abs":   abs,
                "pi":    math.pi,
                "e":     math.e,
                "__builtins__": {}   # Disable dangerous builtins
            }
            
            result = eval(eval_expr, math_context)

            # ── Format the result ─────────────────────────────────────
            # If result is a whole number, show without decimal
            if isinstance(result, float) and result.is_integer():
                result_str = str(int(result))
            else:
                # Round to 10 decimal places to avoid floating point noise
                result_str = str(round(float(result), 10)).rstrip('0').rstrip('.')

            # ── Update Display ────────────────────────────────────────
            self.expr_var.set(f"{original_expr} =")
            self.display_var.set(result_str)
            self.expression = result_str  # Allow chaining calculations
            self.result_shown = True

            # ── Save to Database ──────────────────────────────────────
            self.db.save_calculation(original_expr, result_str)
            print(f"[Calc] {original_expr} = {result_str}")

        # ── Error Handling ────────────────────────────────────────────
        except ZeroDivisionError:
            self._show_error("Cannot ÷ by Zero!")
        except ValueError as e:
            if "math domain" in str(e):
                self._show_error("Math Domain Error!")
            else:
                self._show_error("Invalid Input!")
        except OverflowError:
            self._show_error("Number Too Large!")
        except SyntaxError:
            self._show_error("Invalid Expression!")
        except Exception as e:
            self._show_error(f"Error!")
            print(f"[Calc] Error: {e}")

    def _show_error(self, message):
        """
        Displays an error message in the calculator display.
        
        Args:
            message (str): Error text to show
        """
        self.display_var.set(message)
        self.expr_var.set(self.expression)
        self.expression = ""
        self.result_shown = False

    def _sci_func(self, func_name):
        """
        Handles scientific function button clicks.
        
        For sin/cos/tan/log/sqrt: wraps current expression in function call.
        For sq (x²): squares the current value.
        For fact (n!): computes factorial.
        
        Args:
            func_name (str): 'sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'sq', 'fact'
        """
        if not self.expression:
            # If no input, show function template
            templates = {
                "sin": "sin(", "cos": "cos(", "tan": "tan(",
                "log": "log(", "ln": "ln(", "sqrt": "sqrt("
            }
            if func_name in templates:
                self.expression = templates[func_name]
                self.display_var.set(self.expression)
            return

        current = self.expression

        if func_name in ("sin", "cos", "tan", "log", "ln", "sqrt"):
            # Wrap in function: "30" → "sin(30)"
            self.expression = f"{func_name}({current})"
            self.display_var.set(self.expression)
            self.calculate()

        elif func_name == "sq":
            # Square: "5" → "5**2"
            self.expression = f"({current})**2"
            self.display_var.set(self.expression)
            self.calculate()

        elif func_name == "fact":
            # Factorial: "5" → "120"
            try:
                n = int(float(current))
                if n < 0:
                    self._show_error("No negative factorial!")
                    return
                if n > 170:
                    self._show_error("Too large for factorial!")
                    return
                result = math.factorial(n)
                expr_display = f"{n}!"
                self.expr_var.set(f"{expr_display} =")
                self.display_var.set(str(result))
                self.expression = str(result)
                self.result_shown = True
                self.db.save_calculation(expr_display, str(result))
            except ValueError:
                self._show_error("Factorial needs integer!")

    # ═══════════════════════════════════════════════════════════════════
    # MEMORY FUNCTIONS
    # ═══════════════════════════════════════════════════════════════════

    def memory_add(self):
        """M+ : Adds current display value to memory."""
        try:
            self.memory += float(self.display_var.get())
            self.expr_var.set(f"M+ (Memory: {self.memory})")
        except ValueError:
            pass

    def memory_subtract(self):
        """M- : Subtracts current display value from memory."""
        try:
            self.memory -= float(self.display_var.get())
            self.expr_var.set(f"M- (Memory: {self.memory})")
        except ValueError:
            pass

    def memory_recall(self):
        """MR : Shows the value stored in memory."""
        mem_str = str(int(self.memory) if float(self.memory).is_integer() else self.memory)
        self.expression = mem_str
        self.display_var.set(mem_str)
        self.expr_var.set(f"Memory Recall: {mem_str}")

    def memory_clear(self):
        """MC : Clears the memory (sets to 0)."""
        self.memory = 0.0
        self.expr_var.set("Memory Cleared")

    # ═══════════════════════════════════════════════════════════════════
    # HISTORY WINDOW
    # ═══════════════════════════════════════════════════════════════════

    def show_history(self):
        """
        Opens a new window showing calculation history.
        
        Uses tk.Toplevel() to create a child window.
        Displays history in a scrollable Listbox.
        """
        c = self.theme.get_colors()
        history = self.db.get_history(limit=200)

        # ── Create History Window ─────────────────────────────────────
        hist_window = tk.Toplevel(self.root)
        hist_window.title("Calculation History")
        hist_window.geometry("450x500")
        hist_window.config(bg=c["bg"])
        hist_window.resizable(True, True)

        # Make it a child window (stays on top of calculator)
        hist_window.transient(self.root)

        # ── Title Label ───────────────────────────────────────────────
        tk.Label(
            hist_window,
            text="📋 Calculation History",
            font=("Segoe UI", 14, "bold"),
            bg=c["bg"], fg=c["display_fg"]
        ).pack(pady=10)

        tk.Label(
            hist_window,
            text=f"Total: {len(history)} calculation(s)",
            font=("Segoe UI", 9),
            bg=c["bg"], fg=c["label_fg"]
        ).pack()

        # ── Scrollable Listbox ────────────────────────────────────────
        frame = tk.Frame(hist_window, bg=c["bg"])
        frame.pack(fill="both", expand=True, padx=15, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(
            frame,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 11),
            bg=c["display_bg"],
            fg=c["display_fg"],
            selectbackground=c["op_bg"],
            selectforeground=c["op_fg"],
            relief="flat",
            bd=5
        )
        listbox.pack(fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        # ── Populate Listbox ──────────────────────────────────────────
        if history:
            for row in history:
                # row = (id, expression, result, timestamp)
                id_, expr, result, ts = row
                # Format: "  #1  |  10+20 = 30  |  2026-01-01 10:00"
                ts_short = ts[:16] if ts else ""
                display_text = f"  #{id_:<4}  {expr} = {result}   [{ts_short}]"
                listbox.insert(tk.END, display_text)
        else:
            listbox.insert(tk.END, "  No calculations yet.")
            listbox.insert(tk.END, "  Start calculating to see history!")

        # ── Bottom Buttons ────────────────────────────────────────────
        btn_frame = tk.Frame(hist_window, bg=c["bg"])
        btn_frame.pack(pady=10)

        # Use selected calculation
        def use_selected():
            selection = listbox.curselection()
            if selection and history:
                idx = selection[0]
                if idx < len(history):
                    _, expr, result, _ = history[idx]
                    self.expression = result
                    self.display_var.set(result)
                    hist_window.destroy()

        tk.Button(
            btn_frame, text="Use Result",
            bg=c["eq_bg"], fg=c["eq_fg"],
            font=("Segoe UI", 10), relief="flat",
            command=use_selected
        ).pack(side="left", padx=5)

        # Export button
        tk.Button(
            btn_frame, text="💾 Export CSV",
            bg=c["sci_bg"], fg=c["sci_fg"],
            font=("Segoe UI", 10), relief="flat",
            command=lambda: self.export.export_to_csv(hist_window)
        ).pack(side="left", padx=5)

        # Clear history button
        def clear_history():
            if messagebox.askyesno(
                "Clear History",
                "Delete ALL calculation history?\nThis cannot be undone!",
                parent=hist_window
            ):
                self.db.clear_history()
                hist_window.destroy()
                messagebox.showinfo("Done", "History cleared!", parent=self.root)

        tk.Button(
            btn_frame, text="🗑 Clear All",
            bg=c["clear_bg"], fg=c["clear_fg"],
            font=("Segoe UI", 10), relief="flat",
            command=clear_history
        ).pack(side="left", padx=5)

        # Close button
        tk.Button(
            btn_frame, text="Close",
            bg=c["theme_bg"], fg=c["theme_fg"],
            font=("Segoe UI", 10), relief="flat",
            command=hist_window.destroy
        ).pack(side="left", padx=5)

    # ═══════════════════════════════════════════════════════════════════
    # THEME SWITCHING
    # ═══════════════════════════════════════════════════════════════════

    def toggle_theme(self):
        """
        Switches between dark and light theme.
        Updates ALL widgets dynamically without restart.
        """
        self.theme.toggle_theme()
        self._apply_theme()

    def _apply_theme(self):
        """
        Applies current theme colors to every widget.
        Called on startup and after theme toggle.
        """
        c = self.theme.get_colors()

        # Root window
        self.root.config(bg=c["bg"])

        # Display area
        self.display_frame.config(bg=c["display_bg"])
        self.expression_label.config(bg=c["display_bg"], fg=c["label_fg"])
        self.display.config(bg=c["display_bg"], fg=c["display_fg"])

        # Button frame
        self.btn_frame.config(bg=c["bg"])

        # All calculator buttons
        for btn, color_key in self.all_buttons:
            fg_key = color_key.replace("_bg", "_fg")
            active_key = color_key.replace("_bg", "_active")
            btn.config(
                bg=c[color_key],
                fg=c.get(fg_key, c["display_fg"]),
                activebackground=c.get(active_key, c[color_key])
            )

        # Utility bar
        self.util_frame.config(bg=c["bg"])
        self.hist_btn.config(bg=c["hist_bg"], fg=c["hist_fg"])
        self.export_btn.config(bg=c["sci_bg"], fg=c["sci_fg"])
        self.theme_btn.config(
            bg=c["theme_bg"], fg=c["theme_fg"],
            text=self.theme.get_theme_button_label()
        )

    # ═══════════════════════════════════════════════════════════════════
    # KEYBOARD SHORTCUTS
    # ═══════════════════════════════════════════════════════════════════

    def _bind_keyboard(self):
        """
        Sets up keyboard shortcuts.
        
        root.bind(key, function) attaches a key press to a function.
        '<Return>'    = Enter key
        '<BackSpace>' = Backspace key
        '<Escape>'    = Escape key
        """
        # Number and operator keys
        for key in "0123456789":
            self.root.bind(key, lambda e, k=key: self.click(k))

        for key in "+-*./%()":
            self.root.bind(key, lambda e, k=key: self.click(k))

        self.root.bind(".", lambda e: self.click("."))

        # Special keys
        self.root.bind("<Return>",    lambda e: self.calculate())    # Enter = calculate
        self.root.bind("<KP_Enter>",  lambda e: self.calculate())    # Numpad Enter
        self.root.bind("<BackSpace>", lambda e: self.backspace())    # Delete last char
        self.root.bind("<Escape>",    lambda e: self.clear())        # Escape = clear
        self.root.bind("<Delete>",    lambda e: self.clear())        # Delete = clear

        # Power key
        self.root.bind("^",           lambda e: self.click("**"))

        print("[App] Keyboard shortcuts registered.")

    # ═══════════════════════════════════════════════════════════════════
    # WINDOW UTILITIES
    # ═══════════════════════════════════════════════════════════════════

    def _center_window(self):
        """Centers the calculator window on the screen."""
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"+{x}+{y}")

    def on_close(self):
        """
        Called when user closes the window (X button).
        Properly closes database connection before exiting.
        """
        print("[App] Closing calculator...")
        self.db.close()
        self.root.destroy()