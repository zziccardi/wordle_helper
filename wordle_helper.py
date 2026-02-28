
import argparse
from enum import Enum
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

  class ConstraintMode(Enum):
    WORD_HAS_NO_INCORRECT_LETTERS = 1
    WORD_HAS_ALL_MISPLACED_LETTERS = 2

  # TODO: write docstring and move to top level
  def word_satisfies_incorrect_or_misplaced_letter_constraints(
      word: str, mode: ConstraintMode) -> bool:
    """"""

    if mode == ConstraintMode.WORD_HAS_NO_INCORRECT_LETTERS:
      letters = incorrect_letters
    elif mode == ConstraintMode.WORD_HAS_ALL_MISPLACED_LETTERS:
      letters = misplaced_letters

    for letter in letters:
      all_positions = []
      start_index = 0

      # Search for repeated letters.
      while (position := word.find(letter, start_index)) != -1:
        all_positions.append(position)
        next_position = position + 1

        if next_position >= len(word):
          break

        start_index = next_position

      # Reject words where an incorrect letter is found at any position with an underscore.
      # Or reject words where a misplaced letter is not found in all positions with underscores.
      if ((mode == ConstraintMode.WORD_HAS_NO_INCORRECT_LETTERS and
           any(map(lambda position: correct_letters[position] == '_', all_positions))) or
          (mode == ConstraintMode.WORD_HAS_ALL_MISPLACED_LETTERS and
           all(map(lambda position: correct_letters[position] != '_', all_positions)))):
        return False

    return True

  if incorrect_letters:
    valid_words = filter(
        lambda word: word_satisfies_incorrect_or_misplaced_letter_constraints(
            word, ConstraintMode.WORD_HAS_NO_INCORRECT_LETTERS),
        valid_words)

  # TODO: add test for misplaced letters and ensure fails without changes
  # def word_has_all_misplaced_letters(word: str) -> bool:
  #   for misplaced_letter in misplaced_letters:
  #     if misplaced_letter not in word:
  #       return False
  #   return True

  if misplaced_letters:
    valid_words = filter(
        lambda word: word_satisfies_incorrect_or_misplaced_letter_constraints(
            word, ConstraintMode.WORD_HAS_ALL_MISPLACED_LETTERS),
        valid_words)

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

  parser.add_argument('correct_letters', type=str, nargs='?', default='_____',
      help='confirmed letters and underscores, where the latter represent unknown letters (default: _____)')
  parser.add_argument('-i', '--incorrect_letters', type=str, help='incorrect letters, in any order')
  parser.add_argument('-m', '--misplaced_letters', type=str, help='misplaced letters, in any order')

  args: argparse.Namespace = parser.parse_args()

  correct_letters: str = args.correct_letters.lower() if args.correct_letters else '_____'

  if not re.compile('^[a-z_]{5}$').match(correct_letters):
    raise argparse.ArgumentError(
      '`correct_letters` must be 5 characters long and contain only letters and underscores')

  optional_args = process_optional_args(args)

  incorrect_letters: Optional[str] = optional_args['incorrect_letters']
  misplaced_letters: Optional[str] = optional_args['misplaced_letters']

  valid_words = get_valid_words(correct_letters, incorrect_letters, misplaced_letters)

  print(*valid_words, sep='\n')


if __name__ == '__main__':
  main()
