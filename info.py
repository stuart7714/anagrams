import tkinter as tk


# Display text which gives the user game information
class Info:
    def __init__(self, window):
        frame = tk.Frame(window)
        frame.pack()

        self.label = tk.Label(frame, text="")
        self.label.pack()

    def set_text(self, text):
        self.label.config(text=text)
