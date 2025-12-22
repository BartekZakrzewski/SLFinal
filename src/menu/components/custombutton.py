import tkinter as tk


class CustomButton(tk.Label):
    def __init__(self, parent, text, command, bg, fg, hover_bg, width=20, height=2, font=("Helvetica", 14, "bold")):
        super().__init__(parent, text=text, bg=bg, fg=fg, font=font, width=width, height=height, cursor="hand2")
        
        self.command = command
        self.default_bg = bg
        self.hover_bg = hover_bg
        
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_click(self, event):
        if self.command:
            self.command()

    def on_enter(self, event):
        self.configure(bg=self.hover_bg)

    def on_leave(self, event):
        self.configure(bg=self.default_bg)
