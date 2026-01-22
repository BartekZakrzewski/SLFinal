"""
Custom button component.

This module provides a custom button widget using Tkinter Label,
supporting hover effects and click events.
"""
import tkinter as tk


class CustomButton(tk.Label):
    """
    A custom button widget inheriting from tk.Label.

    Attributes:
        command (callable): Function to execute on click.
        default_bg (str): Default background color.
        hover_bg (str): Background color when hovered.
    """

    def __init__(self, parent,
                 text, command,
                 bg, fg,
                 hover_bg, width=20,
                 height=2, font=("Helvetica", 14, "bold")):
        """
        Initialize the custom button.

        Args:
            parent (tk.Widget): The parent widget.
            text (str): Button text.
            command (callable): Callback function for button click.
            bg (str): Background color.
            fg (str): Foreground text color.
            hover_bg (str): Background color on hover.
            width (int): Width of the button.
            height (int): Height of the button.
            font (tuple): Font settings.
        """
        super().__init__(parent, text=text,
                         bg=bg, fg=fg,
                         font=font, width=width,
                         height=height, cursor="hand2")

        self.command = command
        self.default_bg = bg
        self.hover_bg = hover_bg

        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_click(self, event):
        """Handle mouse click event."""
        if self.command:
            self.command()

    def on_enter(self, event):
        """Handle mouse enter event (hover start)."""
        self.configure(bg=self.hover_bg)

    def on_leave(self, event):
        """Handle mouse leave event (hover end)."""
        self.configure(bg=self.default_bg)
