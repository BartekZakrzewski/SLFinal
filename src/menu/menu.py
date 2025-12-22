from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from src.menu.components.custombutton import CustomButton


FONT = "Helvetiva"
WHITE = '#ffffff'
BG = '#2b2b2b'
LG = '#dddddd'
GREEN = '#4CAF50'

def menu():
    root = tk.Tk()
    root.title("Super Python Bros - Menu")
    root.geometry("600x800")
    root.configure(bg=BG)

    style = ttk.Style()
    style.theme_use('default')
    # style.configure("Heading", foreground='white', background='transparent', font=(FONT, 24))
    style.configure("Heading", foreground='white', background='#2b2b2b', font=(FONT, 24))
    # style.configure("Label", foreground='lightgray', background='transparent', font=(FONT,  18))
    style.configure("Label", foreground='lightgray', background='#2b2b2b', font=(FONT,  18))
    style.configure("TSeparator", foreground='black', background='white')

    username = {'username': None}

    readfile = open('./scores/scores.txt').read()
    readscores = []
    readfile = readfile.split('\n')
    readscores = [s.split(' ') for s in readfile]
    readscores = readscores[:-1]
    if len(readscores):
        readscores.sort(key=lambda x: int(x[1]), reverse=True)
    print(readscores)
    scores = readscores[:5]

    def on_play():
        name = entry.get()
        if name:
            username['username'] = name
            root.destroy()
        else:
            messagebox.showwarning("Error", "You have to input an username")

    top_label = tk.Label(root, text="Top 5 scores", font=(FONT, 24), bg=BG, fg=WHITE)
    top_label.pack(pady=(20, 5))

    if len(scores) > 0 and scores[0] != []:
        for i, s in enumerate(scores):
            score = tk.Label(root, text=f"{i+1}. {s[0]}: {s[1]}", font=(FONT, 18), bg=BG, fg=LG)
            score.pack(anchor='w', padx=(200, 0), pady=(20, 5))
    else:
        score = tk.Label(root, text="n/d", font=(FONT, 18), bg=BG, fg=LG)
        score.pack(pady=(20, 5))

    separator = ttk.Separator(root, orient='horizontal')
    separator.pack(fill='x', padx=(20, 20), pady=(10, 10))

    # user_label = ttk.Label(root, text="Username", font=("Arial", 12))
    user_label = tk.Label(root, text="Username", font=(FONT, 24), bg=BG, fg=WHITE)
    user_label.pack(pady=(5, 5))

    entry = tk.Entry(root,
                      font=(FONT, 12),
                        justify='center',
                        bg="#404040",
                        fg="white",
                        insertbackground="white",
                        bd=0,
                        highlightthickness=1,
                        highlightcolor=GREEN,
                        highlightbackground="#555",
                      )
    entry.pack(pady=5, ipadx=5, ipady=5)
    entry.focus_set()

    # play_btn = ttk.Button(root, text="PLAY", command=on_play, bg='green', fg='white', font=('Arial', 10, 'bold'))
    btn_play = CustomButton(root, 
                        text="PLAY", 
                        command=on_play,
                        bg='#404040',
                        fg="white",
                        hover_bg=GREEN)
    btn_play.pack(pady=40)

    root.mainloop()

    return username['username']

