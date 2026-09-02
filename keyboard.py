import tkinter as tk

from legends import LEGENDS


# Display a keyboard UI where the user can press or type keys
class Keyboard:
    def __init__(self, window, on_key_pressed):
        self.buttons = {}
        self.on_key_pressed = on_key_pressed

        frame = tk.Frame(window, pady=5)
        frame.pack()

        layout = [
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
            ["Return", "z", "x", "c", "v", "b", "n", "m", "BackSpace"]
        ]

        for row in layout:
            row_frame = tk.Frame(frame)
            row_frame.pack()

            for key in row:
                button = tk.Button(
                    row_frame,
                    text=LEGENDS[key],
                    command=lambda key=key:
                        self.on_key_pressed(key)
                )
                button.pack(side=tk.LEFT)
                window.bind((f"<{key}>"), lambda event,
                            button=button: button.invoke())
                self.buttons[key] = button

    # Change the colour of a key on the keyboard
    def colour_key(self, key, colour):
        self.buttons[key]["bg"] = colour
