from enum import Enum
import random
import string


class LetterState(Enum):
    NONE = 1,
    INCORRECT_LETTER = 2,
    CORRECT_LETTER_INCORRECT_POSITION = 3,
    CORRECT_LETTER_CORRECT_POSITION = 4


letter_states = {letter: LetterState.NONE for letter in string.ascii_lowercase}


def update_letter_state(letter, state):
    # Once a letter is found at the correct position then we don't degrade this
    if letter_states[letter] != LetterState.CORRECT_LETTER_CORRECT_POSITION:
        letter_states[letter] = state


def paint_letter(letter, state):
    # Paint letters using ANSI colour escape sequences
    match state:
        case LetterState.NONE:
            return f"{letter}"
        case LetterState.INCORRECT_LETTER:
            # An incorrect letter is grey
            return f"\033[100m{letter}\033[0m"
        case LetterState.CORRECT_LETTER_INCORRECT_POSITION:
            # A correct letter in the incorrect position is yellow
            return f"\033[43m{letter}\033[0m"
        case LetterState.CORRECT_LETTER_CORRECT_POSITION:
            # A correct letter in the correct position is green
            return f"\033[42m{letter}\033[0m"


def paint_all_letters():
    return " ".join(paint_letter(letter, state) for letter, state in letter_states.items())


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

    # Create the comparison result string with painted letters and update state
    comparison_string = ""
    for (guess_letter, guess_state) in zip(guess, guess_states):
        comparison_string = comparison_string + \
            paint_letter(guess_letter, guess_state)
        update_letter_state(guess_letter, guess_state)

    return comparison_string


def play_game():
    num_guesses = 6
    while num_guesses > 0:
        guess = input().lower()
        if len(guess) != target_length:
            print(f"Guesses must be {target_length} characters (reenter word)")
        elif not guess in word_list:
            print("Guess not in dictionary (reenter word)")
        elif guess == target:
            print("You won!")
            return
        else:
            num_guesses = num_guesses - 1
            if num_guesses > 1:
                print(
                    f"{compare(guess)} ({num_guesses} guesses left) - {paint_all_letters()}")
            elif num_guesses == 1:
                print(f"{compare(guess)} (1 guess left) - {paint_all_letters()}")
            else:
                print(
                    f"{compare(guess)} (word was \"{target}\") - {paint_all_letters()}")
                print("You lost!")


# Load the full list of possible words
word_list = load_word_list("words/words.txt")

# Select a random word for the user to guess
target_index = random.randrange(0, len(word_list))
target = word_list[target_index]
target_length = len(target)

play_game()
