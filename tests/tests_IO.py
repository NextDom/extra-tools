# -*- coding: utf-8 -*-

import shutil
import tempfile
import unittest
from unittest.mock import patch

from scripts.libs.IO import IO

SIMPLE_MENU = ['First choice',
               'Second choice']


# noinspection PyUnusedLocal
class TestIO(unittest.TestCase):
    test_dir = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_is_string_with_string(self):
        self.assertTrue(IO.is_string('a small string'))

    def test_is_string_with_int(self):
        self.assertFalse(IO.is_string(2))

    def test_is_string_with_list(self):
        self.assertFalse(IO.is_string(['A string']))

    def test_is_string_with_dict(self):
        self.assertFalse(IO.is_string({'ok': 'ok'}))

    @patch('builtins.input', side_effect=[1])
    def test_get_menu_choice_good_choice(self, side_effect):
        result = IO.get_menu_choice(SIMPLE_MENU)
        self.assertEqual(result, 0)

    @patch('builtins.input', side_effect=[7, 0])
    # pylint: disable=unused-argument
    def test_get_menu_choice_bad_choice(self, side_effect):
        # Test un mauvais choix puis quitte
        result = IO.get_menu_choice(SIMPLE_MENU)
        self.assertEqual(result, -1)

    @patch('builtins.input', side_effect=['A', 0])
    # pylint: disable=unused-argument
    def test_get_menu_choice_bad_input(self, side_effect):
        # Test un mauvais caractère puis quitte
        result = IO.get_menu_choice(SIMPLE_MENU)
        self.assertEqual(result, -1)

    @patch('builtins.input', side_effect=[0])
    # pylint: disable=unused-argument
    def test_get_menu_choice_cancel_with_choice(self, side_effect):
        result = IO.get_menu_choice(SIMPLE_MENU)
        self.assertEqual(result, -1)

    @patch('builtins.input', side_effect=[''])
    # pylint: disable=unused-argument
    def test_get_menu_choice_cancel_without_choice(self, side_effect):
        result = IO.get_menu_choice(SIMPLE_MENU)
        self.assertEqual(result, -1)

    @patch('builtins.input', side_effect=[0, 1])
    def test_get_menu_choice_cancel_when_cant(self, side_effect):
        result = IO.get_menu_choice(SIMPLE_MENU, show_cancel=False)
        self.assertEqual(result, 0)

    @patch('builtins.input', side_effect=['', 1])
    def test_get_menu_choice_cancel_when_cant_without_choice(self, side_effect):
        result = IO.get_menu_choice(SIMPLE_MENU, show_cancel=False)
        self.assertEqual(result, 0)

    @patch('builtins.input', side_effect=['o'])
    def test_ask_y_n_answer_y(self, side_effect):
        result = IO.ask_y_n('Question')
        self.assertEqual(result, 'o')

    @patch('builtins.input', side_effect=['n'])
    def test_ask_y_n_answer_n(self, side_effect):
        result = IO.ask_y_n('Question')
        self.assertEqual(result, 'n')

    @patch('builtins.input', side_effect=[''])
    def test_ask_y_n_without_answer(self, side_effect):
        result = IO.ask_y_n('Question')
        self.assertEqual(result, 'o')

    @patch('builtins.input', side_effect=[''])
    def test_ask_y_n_without_answer_default_n(self, side_effect):
        result = IO.ask_y_n('Question', 'n')
        self.assertEqual(result, 'n')

    @patch('builtins.input', side_effect=['Another answer'])
    def test_ask_with_default_with_other_answer(self, side_effect):
        result = IO.ask_with_default('Question', 'First answer')
        self.assertEqual(result, 'Another answer')

    @patch('builtins.input', side_effect=[''])
    def test_ask_with_default_without_answer(self, side_effect):
        result = IO.ask_with_default('Question', 'First answer')
        self.assertEqual(result, 'First answer')
