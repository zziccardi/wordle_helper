
import unittest

import wordle_helper


class WordleHelperTest(unittest.TestCase):

  def test_get_valid_words_with_first_letter_confirmed(self):
    letters = 'e_o_y'
    valid_words = wordle_helper.get_valid_words(letters)

    self.assertEqual(valid_words, ['ebony', 'epoxy'])

  def test_get_valid_words_with_first_letter_unknown(self):
    letters = '_able'
    valid_words = wordle_helper.get_valid_words(letters)

    self.assertEqual(valid_words, ['cable', 'fable', 'gable', 'sable', 'table'])

  def test_get_valid_words_with_incorrect_letters(self):
    correct_letters = '_able'
    incorrect_letters = 'tsgf'
    result = wordle_helper.get_valid_words(correct_letters, incorrect_letters)

    self.assertEqual(result, ['cable'])

  def test_get_valid_words_with_misplaced_letters(self):
    correct_letters = '_able'
    misplaced_letters = 'c'
    result = wordle_helper.get_valid_words(correct_letters, misplaced_letters=misplaced_letters)

    self.assertEqual(result, ['cable'])

  def test_get_valid_words_with_incorrect_and_misplaced_letters(self):
    correct_letters = '____e'
    incorrect_letters = 'cablyuthsnr'
    misplaced_letters = 'xo'
    result = wordle_helper.get_valid_words(correct_letters, incorrect_letters, misplaced_letters)

    self.assertEqual(result, ['moxie', 'oxide'])

  def test_get_valid_words_with_incorrect_letters_filtered_only_in_unknown_positions(self):
    correct_letters = 'sho__'
    incorrect_letters = 'cableutrnpsok'

    result = wordle_helper.get_valid_words(correct_letters, incorrect_letters)

    self.assertIn('showy', result)

  def test_get_valid_words_with_no_correct_letters(self):
    correct_letters = '_____'

    result = wordle_helper.get_valid_words(correct_letters)

    # All positions being unknown should result in many valid words.
    self.assertGreater(len(result), 0)

    # Expect common words to be included in the results.
    self.assertIn('about', result)
    self.assertIn('zebra', result)


if __name__ == '__main__':
  unittest.main()
