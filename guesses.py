import tkinter as tk
from legends import LEGENDS


# Display the user's guesses
class Guesses:
    def __init__(self, window, num_letters, num_guesses):
        self.current_guess = 0
        self.labels = {}
        self.num_letters = num_letters

        frame = tk.Frame(window, pady=5)
        frame.pack()

        for guess_idx in range(num_guesses):
            guess_frame = tk.Frame(frame)
            guess_frame.pack()

            for letter_idx in range(self.num_letters):
                label = tk.Label(guess_frame, text="",
                                 relief=tk.SOLID, borderwidth=1, width=2)
                label.pack(side=tk.LEFT, padx=1, pady=1)
                self.labels[(guess_idx, letter_idx)] = label

    # Set the (partial) current guess the user is in the process of making
    # This will expand and contract as the user enters and deletes letters
    def set_guess(self, guess):
        letter_idx = 0
        for letter in guess:
            self.labels[(self.current_guess, letter_idx)
                        ]["text"] = LEGENDS[letter]
            letter_idx = letter_idx + 1
        while letter_idx < self.num_letters:
            self.labels[(self.current_guess, letter_idx)]["text"] = ""
            letter_idx = letter_idx + 1

    # The users has finished their guess
    # Set the colours of the individual letters of their guess to give the user clues
    def finish_guess(self, colours):
        letter_idx = 0
        for colour in colours:
            self.labels[(self.current_guess, letter_idx)]["bg"] = colour
            letter_idx = letter_idx + 1
        self.current_guess = self.current_guess + 1
