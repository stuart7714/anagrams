import re
import argparse

# Extract all five letter words from a larger list of words

parser = argparse.ArgumentParser(
    prog="Words",
    description="Extract five letter words from word list")
parser.add_argument("all_words_filename")
parser.add_argument("five_letter_words_filename")
args = parser.parse_args()

all_words_filename = args.all_words_filename
five_letter_words_filename = args.five_letter_words_filename

five_letter_word_re = re.compile("[a-z]{5}")

five_letter_words = []
with open(all_words_filename, encoding="utf-8") as file:
    for line in file:
        five_letter_word = five_letter_word_re.match(line)
        if five_letter_word:
            five_letter_words.append(five_letter_word.group(0))
five_letter_words = sorted(five_letter_words)

with open(five_letter_words_filename, "w") as file:
    for five_letter_word in five_letter_words:
        file.writelines(five_letter_word + "\n")
