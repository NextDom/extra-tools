# -*- coding: utf-8 -*-

import inspect
import os
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

current_path = os.path.abspath(inspect.getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)
from tools import I18nMenu


# noinspection PyUnusedLocal
class TestAddLanguage(unittest.TestCase):
    test_dir = None
    plugin_dir = None
    core_dir = None
    i18n_menu = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.plugin_dir = self.test_dir + os.sep + 'plugin-Test'
        self.core_dir = os.path.join(self.plugin_dir, 'core')
        self.i18n_menu = I18nMenu(self.plugin_dir, 'Test')
        os.mkdir(self.plugin_dir)
        os.mkdir(self.core_dir)
        os.mkdir(self.plugin_dir + os.sep + 'desktop')
        with open(os.path.join(self.plugin_dir, 'desktop', 'test.php'),
                  'w') as to_translate:
            to_translate.write('A small {{content}} to {{translate}}.')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch('builtins.input', side_effect=['fr_FR'])
    def test_add_simple_language(self, side_effect):
        os.mkdir(self.core_dir + os.sep + 'i18n')
        self.i18n_menu.add_language()
        dest_file_path = os.path.join(self.core_dir, 'i18n', 'fr_FR.json')
        self.assertTrue(os.path.exists(dest_file_path))
        with open(dest_file_path, 'r') as dest_file:
            content = dest_file.read()
            self.assertIn('content', content)
            self.assertIn('translate', content)

    @patch('builtins.input', side_effect=['o', 'fr_FR'])
    def test_without_i18n_add_language(self, side_effect):
        self.i18n_menu.add_language()
        dest_file_path = os.path.join(self.core_dir, 'i18n', 'fr_FR.json')
        self.assertTrue(os.path.exists(dest_file_path))
        with open(dest_file_path, 'r') as dest_file:
            content = dest_file.read()
            self.assertIn('content', content)
            self.assertIn('translate', content)
