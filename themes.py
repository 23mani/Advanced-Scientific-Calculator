"""
themes.py - ThemeManager Class
================================
Manages Dark Mode and Light Mode for the calculator.

Defines color dictionaries for each theme and applies
them dynamically to all widgets without restarting the app.
"""


class ThemeManager:
    """
    Stores theme color palettes and applies them to widgets.
    
    Two themes available:
    - 'dark'  → Dark background, light text (easy on eyes at night)
    - 'light' → White background, dark text (classic look)
    """

    # ── Theme Color Palettes ─────────────────────────────────────────
    # Each theme is a dict mapping widget roles → hex color codes

    THEMES = {
        "dark": {
            # Window & display
            "bg":              "#1e1e2e",   # Main window background
            "display_bg":      "#181825",   # Calculator screen background
            "display_fg":      "#cdd6f4",   # Display text color

            # Number buttons (0-9, decimal, percent)
            "num_bg":          "#313244",   # Number button background
            "num_fg":          "#cdd6f4",   # Number button text
            "num_active":      "#45475a",   # Color when hovering

            # Operator buttons (+, -, *, /)
            "op_bg":           "#f38ba8",   # Operator button background (pink-red)
            "op_fg":           "#1e1e2e",   # Operator button text (dark)
            "op_active":       "#eba0ac",   # Color when hovering

            # Scientific buttons (sin, cos, sqrt, etc.)
            "sci_bg":          "#89b4fa",   # Scientific button background (blue)
            "sci_fg":          "#1e1e2e",   # Scientific button text
            "sci_active":      "#b4befe",   # Color when hovering

            # Special buttons (=, C, backspace)
            "eq_bg":           "#a6e3a1",   # Equals button (green)
            "eq_fg":           "#1e1e2e",
            "clear_bg":        "#f38ba8",   # Clear button (red)
            "clear_fg":        "#1e1e2e",
            "back_bg":         "#fab387",   # Backspace button (orange)
            "back_fg":         "#1e1e2e",

            # History & utility buttons
            "hist_bg":         "#cba6f7",   # History button (purple)
            "hist_fg":         "#1e1e2e",
            "theme_bg":        "#a6adc8",   # Theme toggle button (gray)
            "theme_fg":        "#1e1e2e",

            # Labels and borders
            "label_fg":        "#6c7086",   # Section label text
            "border":          "#313244",   # Border color
        },

        "light": {
            # Window & display
            "bg":              "#f8f8f2",
            "display_bg":      "#ffffff",
            "display_fg":      "#282a36",

            # Number buttons
            "num_bg":          "#e8e8e8",
            "num_fg":          "#282a36",
            "num_active":      "#d0d0d0",

            # Operator buttons
            "op_bg":           "#ff5555",
            "op_fg":           "#ffffff",
            "op_active":       "#ff7777",

            # Scientific buttons
            "sci_bg":          "#6272a4",
            "sci_fg":          "#ffffff",
            "sci_active":      "#7284b6",

            # Special buttons
            "eq_bg":           "#50fa7b",
            "eq_fg":           "#282a36",
            "clear_bg":        "#ff5555",
            "clear_fg":        "#ffffff",
            "back_bg":         "#ffb86c",
            "back_fg":         "#282a36",

            # History & utility
            "hist_bg":         "#bd93f9",
            "hist_fg":         "#282a36",
            "theme_bg":        "#999999",
            "theme_fg":        "#ffffff",

            # Labels and borders
            "label_fg":        "#888888",
            "border":          "#cccccc",
        }
    }

    def __init__(self, initial_theme="dark"):
        """
        Constructor.
        
        Args:
            initial_theme (str): 'dark' or 'light'
        """
        self.current_theme = initial_theme
        print(f"[Theme] Starting with '{initial_theme}' theme.")

    def get_colors(self):
        """
        Returns the color dictionary for the current theme.
        
        Returns:
            dict: Color palette for current theme
        
        Usage:
            colors = theme_manager.get_colors()
            button.config(bg=colors["op_bg"])
        """
        return self.THEMES[self.current_theme]

    def toggle_theme(self):
        """
        Switches between dark and light theme.
        
        Returns:
            str: The NEW theme name after toggling
        """
        if self.current_theme == "dark":
            self.current_theme = "light"
        else:
            self.current_theme = "dark"
        print(f"[Theme] Switched to '{self.current_theme}' theme.")
        return self.current_theme

    def is_dark(self):
        """Returns True if current theme is dark mode."""
        return self.current_theme == "dark"

    def get_theme_button_label(self):
        """
        Returns the label for the theme toggle button.
        Shows what you'll SWITCH TO, not current theme.
        """
        if self.current_theme == "dark":
            return "☀ Light"
        else:
            return "🌙 Dark"