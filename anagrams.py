from enum import Enum

target_word = "plink"
target_length = len(target_word)


class Result(Enum):
    NONE = 1,
    INCORRECT_CHARACTER = 2,
    CORRECT_CHARACTER_INCORRECT_POSITION = 3,
    CORRECT_CHARACTER_CORRECT_POSITION = 4


# Create a string which shows the comparison of the user word and the target word:
# - An incorrect character is grey
# - A correct character in the incorrect position is yellow
# - A correct character in the correct position is green
def compare(user_word):
    char_results = [Result.NONE] * target_length
    char_search_pool = []

    # Find correct characters in the correct positions
    for idx, (user_char, target_char) in enumerate(zip(user_word, target_word)):
        if user_char == target_char:
            char_results[idx] = Result.CORRECT_CHARACTER_CORRECT_POSITION
        else:
            char_search_pool.append(target_char)

    # Find any correct characters in the incorrect position
    for idx, (user_char, target_char) in enumerate(zip(user_word, target_word)):
        if char_results[idx] != Result.CORRECT_CHARACTER_CORRECT_POSITION:
            if user_char in char_search_pool:
                char_results[idx] = Result.CORRECT_CHARACTER_INCORRECT_POSITION
                char_search_pool.remove(user_char)
            else:
                char_results[idx] = Result.INCORRECT_CHARACTER

    # Create the string with ANSI color escape sequences
    comparison_string = ""
    for (user_char, char_result) in zip(user_word, char_results):
        match char_result:
            case Result.INCORRECT_CHARACTER:
                comparison_string = comparison_string + \
                    f"\033[47m {user_char} \033[0m"
            case Result.CORRECT_CHARACTER_INCORRECT_POSITION:
                comparison_string = comparison_string + \
                    f"\033[43m {user_char} \033[0m"
            case Result.CORRECT_CHARACTER_CORRECT_POSITION:
                comparison_string = comparison_string + \
                    f"\033[42m {user_char} \033[0m"
    return comparison_string


def play_game():
    num_guesses = 6
    while num_guesses > 0:
        user_word = input()
        if len(user_word) != target_length:
            print(f"Guesses must be {target_length} characters (reenter word)")
        elif user_word == target_word:
            print("You won!")
            return
        else:
            num_guesses = num_guesses - 1
            if num_guesses > 1:
                print(f"{compare(user_word)} ({num_guesses} guesses left)")
            elif num_guesses == 1:
                print(f"{compare(user_word)} (1 guess left)")
            else:
                print(f"{compare(user_word)} (word was \"{target_word}\")")
                print("You lost!")


play_game()
