# anagrams
A basic anagram game in Python used for programming practice

## Overview

A target word is selected from a dictionary and the user has six attempts to guess the target word.

When the user makes a guess then the letters of their guess are coloured according to the key:

* A green letter is correct
* A yellow letter is in the target word but is in a different position
* A grey letter is not in the target word

## Getting Started

This repository does not contain a dictionary and it expects a dictionary file to be located at `words/words.txt`

A Python script located at `words/words.py` may be used to extract all words of five letters from a larger dictionary file.

For example, the PowerShell command:

```python.exe .\words.py $env:APPDATA\Notepad++\Plugins\Config\Hunspell\en_GB.dic .\words.txt```

This will create a dictionary of five letter words from the Notepad++ spell check dictionary.

## Code Structure

The code consists of a main file `anagrams.py` and then other files containing UI classes.

The layout of the UI is an `Info` section at the top, which shows feedback to the user, then a `Guesses` section which contains the user's guesses to date, and lastly a `Keyboard` section which is an on-screen keyboard which the user can click (or they can simply type letters).

As the user enters letters, the function `on_key_pressed` is called which builds up the guess string. When the user presses "Return" then their guess string is compared against the target word string. The result of this comparison is a sequence of `LetterState` values which is used to update the colour of the guess and the on-screen keyboard.