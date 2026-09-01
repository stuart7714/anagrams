import random
import string
import tkinter as tk

from enum import Enum
from guesses import Guesses
from info import Info
from keyboard import Keyboard


class LetterState(Enum):
    NONE = 1,
    INCORRECT_LETTER = 2,
    CORRECT_LETTER_INCORRECT_POSITION = 3,
    CORRECT_LETTER_CORRECT_POSITION = 4


letter_states = {letter: LetterState.NONE for letter in string.ascii_lowercase}


def letter_state_colour(state):
    match state:
        case LetterState.NONE:
            return ""
        case LetterState.INCORRECT_LETTER:
            return "grey"
        case LetterState.CORRECT_LETTER_INCORRECT_POSITION:
            return "yellow"
        case LetterState.CORRECT_LETTER_CORRECT_POSITION:
            return "green"


def update_letter_state(letter, state):
    # Once a letter is found at the correct position then we don't degrade this
    if letter_states[letter] != LetterState.CORRECT_LETTER_CORRECT_POSITION:
        letter_states[letter] = state
        keyboard.colour_key(letter, letter_state_colour(state))


def load_word_list(filename):
    word_list = []
    with open(filename) as file:
        word_list = file.readlines()
    stripped_word_list = [word.rstrip() for word in word_list]
    return stripped_word_list


# Compare the guess to the target to see how correct they are
def compare(guess):
    guess_states = [LetterState.NONE] * target_length
    letter_search_pool = []

    # Find correct letters in the correct positions
    for idx, (guess_letter, target_letter) in enumerate(zip(guess, target)):
        if guess_letter == target_letter:
            guess_states[idx] = LetterState.CORRECT_LETTER_CORRECT_POSITION
        else:
            letter_search_pool.append(target_letter)

    # Find any correct letters in the incorrect position
    for idx, (guess_letter, target_letter) in enumerate(zip(guess, target)):
        if guess_states[idx] != LetterState.CORRECT_LETTER_CORRECT_POSITION:
            if guess_letter in letter_search_pool:
                guess_states[idx] = LetterState.CORRECT_LETTER_INCORRECT_POSITION
                letter_search_pool.remove(guess_letter)
            else:
                guess_states[idx] = LetterState.INCORRECT_LETTER

    # Create the comparison result colours and update state
    colours = []
    for (guess_letter, guess_state) in zip(guess, guess_states):
        colours.append(letter_state_colour(guess_state))
        update_letter_state(guess_letter, guess_state)

    guesses.finish_guess(colours)


# The user has pressed a key so update and check their guess
def on_key_pressed(key):
    global guess
    global num_guesses
    if num_guesses > 0:
        info.set_text("")
        if key == "Return":
            if len(guess) < target_length:
                info.set_text(f"Guesses must be {target_length} characters")
            elif not guess in word_list:
                info.set_text("Guess not in dictionary")
            elif guess == target:
                compare(guess)
                info.set_text("You won!")
                num_guesses = 0
            else:
                compare(guess)
                guess = ""
                num_guesses = num_guesses - 1
                if num_guesses == 0:
                    info.set_text(f"You lost! Word was '{target}'")
        elif key == "BackSpace":
            if len(guess) > 0:
                guess = guess[:-1]
                guesses.set_guess(guess)
        else:
            if len(guess) < target_length:
                guess += key
                guesses.set_guess(guess)


# Load the full list of possible words
word_list = load_word_list("words/words.txt")

# Select a random word for the user to guess
target_index = random.randrange(0, len(word_list))
target = word_list[target_index]
target_length = len(target)

# The user has a number of chances to guess the word
num_guesses = 6
guess = ""

# Create the UI
window = tk.Tk()
window.title("Anagrams Game")
window.geometry("300x250")

info = Info(window)
guesses = Guesses(window, target_length, num_guesses)
keyboard = Keyboard(window, on_key_pressed)

window.mainloop()
