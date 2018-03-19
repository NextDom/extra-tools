# -*- coding: utf-8 -*-
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from libs.BaseMenu import BaseMenu

SIMPLE_MENU = ['First choice',
               'Second choice']


# noinspection PyUnusedLocal
class TestBaseMenu(unittest.TestCase):
    test_dir = None
    base_menu = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.base_menu = BaseMenu()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_is_string_with_string(self):
        self.assertTrue(BaseMenu.is_string('a small string'))

    def test_is_string_with_int(self):
        self.assertFalse(BaseMenu.is_string(2))

    def test_is_string_with_list(self):
        self.assertFalse(BaseMenu.is_string(['A string']))

    def test_is_string_with_dict(self):
        self.assertFalse(BaseMenu.is_string({'ok': 'ok'}))

    @patch('builtins.input', side_effect=[1])
    def test_get_menu_choice_good_choice(self, side_effect):
        result = self.base_menu.get_menu_choice(SIMPLE_MENU)
        self.assertEqual(result, 0)

    @patch('builtins.input', side_effect=[7, 0])
    # pylint: disable=unused-argument
    def test_get_menu_choice_bad_choice(self, side_effect):
        # Test un mauvais choix puis quitte
        result = self.base_menu.get_menu_choice(SIMPLE_MENU)
        self.assertEqual(result, -1)

    @patch('builtins.input', side_effect=['A', 0])
    # pylint: disable=unused-argument
    def test_get_menu_choice_bad_input(self, side_effect):
        # Test un mauvais caractère puis quitte
        result = self.base_menu.get_menu_choice(SIMPLE_MENU)
        self.assertEqual(result, -1)

    @patch('builtins.input', side_effect=[0])
    # pylint: disable=unused-argument
    def test_get_menu_choice_cancel_with_choice(self, side_effect):
        result = self.base_menu.get_menu_choice(SIMPLE_MENU)
        self.assertEqual(result, -1)

    @patch('builtins.input', side_effect=[''])
    # pylint: disable=unused-argument
    def test_get_menu_choice_cancel_without_choice(self, side_effect):
        result = self.base_menu.get_menu_choice(SIMPLE_MENU)
        self.assertEqual(result, -1)

    @patch('builtins.input', side_effect=[0, 1])
    def test_get_menu_choice_cancel_when_cant(self, side_effect):
        result = self.base_menu.get_menu_choice(SIMPLE_MENU, False)
        self.assertEqual(result, 0)

    @patch('builtins.input', side_effect=['', 1])
    def test_get_menu_choice_cancel_when_cant_without_choice(self, side_effect):
        result = self.base_menu.get_menu_choice(SIMPLE_MENU, False)
        self.assertEqual(result, 0)

    @patch('builtins.input', side_effect=['o'])
    def test_ask_y_n_answer_y(self, side_effect):
        result = BaseMenu.ask_y_n('Question')
        self.assertEqual(result, 'o')

    @patch('builtins.input', side_effect=['n'])
    def test_ask_y_n_answer_n(self, side_effect):
        result = BaseMenu.ask_y_n('Question')
        self.assertEqual(result, 'n')

    @patch('builtins.input', side_effect=[''])
    def test_ask_y_n_without_answer(self, side_effect):
        result = BaseMenu.ask_y_n('Question')
        self.assertEqual(result, 'o')

    @patch('builtins.input', side_effect=[''])
    def test_ask_y_n_without_answer_default_n(self, side_effect):
        result = BaseMenu.ask_y_n('Question', 'n')
        self.assertEqual(result, 'n')

    @patch('builtins.input', side_effect=['Another answer'])
    def test_ask_with_default_with_other_answer(self, side_effect):
        result = BaseMenu.ask_with_default('Question', 'First answer')
        self.assertEqual(result, 'Another answer')

    @patch('builtins.input', side_effect=[''])
    def test_ask_with_default_without_answer(self, side_effect):
        result = BaseMenu.ask_with_default('Question', 'First answer')
        self.assertEqual(result, 'First answer')

    def test_is_content_in_file_without_file(self):
        file_to_test = self.test_dir + os.sep + 'FileNotFound'
        result = BaseMenu.is_content_in_file(file_to_test, 'test string')
        self.assertFalse(result)

    def test_is_content_in_file_without_the_content(self):
        file_to_test = self.test_dir + os.sep + 'WithoutTheContent'
        with open(file_to_test, 'w') as dest:
            dest.write('Nothing in this file')
        result = BaseMenu.is_content_in_file(file_to_test, 'content')
        self.assertFalse(result)

    def test_is_content_in_file_without_content(self):
        file_to_test = self.test_dir + os.sep + 'WithContent'
        with open(file_to_test, 'w') as dest:
            dest.write('Small content in a file')
        result = BaseMenu.is_content_in_file(file_to_test, 'content')
        self.assertTrue(result)

    def test_sed_replace_with_match(self):
        sed_file_path = self.test_dir + os.sep + 'sed_test'
        with open(sed_file_path, 'w') as sed_file:
            sed_file.write('AABBBCCCC')
        BaseMenu.sed_replace('BBB', 'DDDDD', sed_file_path)
        file_content = ''
        with open(sed_file_path, 'r') as sed_file:
            file_content = sed_file.read()
        self.assertIn('AADDDDDCCCC', file_content)


    def test_sed_replace_without_match(self):
        sed_file_path = self.test_dir + os.sep + 'sed_test'
        with open(sed_file_path, 'w') as sed_file:
            sed_file.write('AABBBCCCC')
        BaseMenu.sed_replace('ZZZ', 'DDDDD', sed_file_path)
        file_content = ''
        with open(sed_file_path, 'r') as sed_file:
            file_content = sed_file.read()
        self.assertIn('AABBBCCCC', file_content)
