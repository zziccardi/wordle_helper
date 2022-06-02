
# TODO: Add version control
# TODO: Do proper unit testing, optionally in separate file
# TODO: Add test and debug `python3 wordle_helper.py sho__ -i cableutrnpsok` not yielding "showy"
# (should only filter out words containing incorrect letters in positions with underscores, not in
# all positions!); check if -m has this problem too

import argparse
import re
import string
from typing import Dict, List, Optional

import enchant


def get_valid_words(correct_letters: str, incorrect_letters: str = '',
                    misplaced_letters: str = '') -> List[str]:
  """Get valid words matching constraints of confirmed and unknown letters in given positions.

  If present, incorrect letters will be used to filter out possible valid words. If present,
  misplaced letters (correct letters but in the wrong spots) will also be used for filtering. Note
  however that the positions of misplaced letters are not considered.
  
  Args:
    correct_letters: confirmed (green) and unknown letters, where the latter are represented by
      underscores, in specific positions
    incorrect_letters: wrong (black) letters, in any order
    misplaced_letters: misplaced (yellow) letters, in any order
  
  Returns:
    valid words matching constraints (in alphabetical order)
  """

  current_letter_lists: List[List[str]] = []

  for letter in correct_letters:
    if letter != '_':
      if not current_letter_lists:
        current_letter_lists.append([letter])
      else:
        for letter_list in current_letter_lists:
          letter_list.append(letter)
    else:
      if not current_letter_lists:
        for lowercase_letter in string.ascii_lowercase:
          current_letter_lists.append([lowercase_letter])
      else:
        new_letter_lists: List[List[str]] = []

        for letter_list in current_letter_lists:
          for lowercase_letter in string.ascii_lowercase:
            new_letter_lists.append(letter_list + [lowercase_letter])

        current_letter_lists = new_letter_lists

  english_dict = enchant.Dict('en_US')
  letter_combos = map(lambda letter_list: ''.join(letter_list), current_letter_lists)
  valid_words = filter(lambda combo: english_dict.check(combo), letter_combos)

  def word_has_incorrect_letter(word: str) -> bool:
    for incorrect_letter in incorrect_letters:
      if incorrect_letter in word:
        return True
    return False

  def word_has_all_misplaced_letters(word: str) -> bool:
    for misplaced_letter in misplaced_letters:
      if misplaced_letter not in word:
        return False
    return True

  if incorrect_letters:
    valid_words = filter(lambda word: not word_has_incorrect_letter(word), valid_words)

  if misplaced_letters:
    valid_words = filter(lambda word: word_has_all_misplaced_letters(word), valid_words)

  return list(valid_words)


def process_optional_args(args: argparse.Namespace) -> Dict[str, Optional[str]]:
  """Perform identical handling of optional args."""

  arg_map = {'incorrect_letters': None, 'misplaced_letters': None}

  for key in arg_map.keys():
    letters: str = getattr(args, key)

    if letters:
      letters = letters.lower()

      if not re.compile('^[a-z]+$').match(letters):
        raise argparse.ArgumentError(f'`{key}` must contain at least 1 letter')

      arg_map[key] = letters

  return arg_map


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument('correct_letters', type=str,
    help='confirmed letters and underscores, where the latter represent unknown letters')
  parser.add_argument('-i', '--incorrect_letters', type=str, help='incorrect letters, in any order')
  parser.add_argument('-m', '--misplaced_letters', type=str, help='misplaced letters, in any order')

  args: argparse.Namespace = parser.parse_args()
  correct_letters: str = args.correct_letters.lower()

  if not re.compile('^[a-z_]{5}$').match(correct_letters):
    raise argparse.ArgumentError(
      '`correct_letters` must be 5 characters long and contain only letters and underscores')

  if '_' not in correct_letters:
    raise argparse.ArgumentError('`correct_letters` must contain at least one underscore')

  optional_args = process_optional_args(args)

  incorrect_letters: Optional[str] = optional_args['incorrect_letters']
  misplaced_letters: Optional[str] = optional_args['misplaced_letters']

  valid_words = get_valid_words(correct_letters, incorrect_letters, misplaced_letters)

  print(*valid_words, sep='\n')


def test_get_valid_words_with_first_letter_confirmed():
  letters = 'e_o_y'
  valid_words = get_valid_words(letters)

  assert valid_words == ['ebony', 'epoxy']


def test_get_valid_words_with_first_letter_unknown():
  letters = '_able'
  valid_words = get_valid_words(letters)

  assert valid_words == ['cable', 'fable', 'gable', 'sable', 'table']


def test_get_valid_words_with_incorrect_letters():
  correct_letters = '_able'
  incorrect_letters = 'tsgf'
  result = get_valid_words(correct_letters, incorrect_letters)

  assert result == ['cable']


def test_get_valid_words_with_misplaced_letters():
  correct_letters = '_able'
  misplaced_letters = 'c'
  result = get_valid_words(correct_letters, misplaced_letters=misplaced_letters)

  assert result == ['cable']


def test_get_valid_words_with_incorrect_and_misplaced_letters():
  correct_letters = '____e'
  incorrect_letters = 'cablyuthsnr'
  misplaced_letters = 'xo'
  result = get_valid_words(correct_letters, incorrect_letters, misplaced_letters)

  assert result == ['moxie', 'oxide']


if __name__ == '__main__':
  main()
  # test_get_valid_words_with_first_letter_confirmed()
  # test_get_valid_words_with_first_letter_unknown()
  # test_get_valid_words_with_incorrect_letters()
  # test_get_valid_words_with_misplaced_letters()
  # test_get_valid_words_with_incorrect_and_misplaced_letters()
