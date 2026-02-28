# wordle_helper

A simple program to help with solving [Wordle](https://www.nytimes.com/games/wordle/index.html) puzzles

## Installation

The only dependency is [PyEnchant](https://pyenchant.github.io/pyenchant/), which can be retrieved with
`pipenv install`.

## Usage

```
$ python3 wordle_helper.py -h
usage: wordle_helper.py [-h] [-i INCORRECT_LETTERS] [-m MISPLACED_LETTERS] correct_letters

positional arguments:
  correct_letters       confirmed letters and underscores, where the latter represent unknown letters

optional arguments:
  -h, --help            show this help message and exit
  -i INCORRECT_LETTERS, --incorrect_letters INCORRECT_LETTERS
                        incorrect letters, in any order
  -m MISPLACED_LETTERS, --misplaced_letters MISPLACED_LETTERS
                        misplaced letters, in any order
```

Simple example, with the first letter unknown:

```
$ python3 wordle_helper.py _able
cable
fable
gable
sable
table
```

See the test cases for additional examples.
