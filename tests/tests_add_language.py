# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
import unittest

COMMAND = './scripts/add_language.py %s > /dev/null 2>&1'


# noinspection PyUnusedLocal
class TestAddLanguage(unittest.TestCase):
    test_dir = None
    plugin_dir = None
    core_dir = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.plugin_dir = self.test_dir + os.sep + 'plugin-Test'
        self.core_dir = os.path.join(self.plugin_dir, 'core')
        os.mkdir(self.plugin_dir)
        os.mkdir(self.core_dir)
        os.mkdir(self.plugin_dir + os.sep + 'desktop')
        with open(os.path.join(self.plugin_dir, 'desktop', 'test.php'),
                  'w') as to_translate:
            to_translate.write('A small {{content}} to {{translate}}.')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_add_simple_language(self):
        os.mkdir(self.core_dir + os.sep + 'i18n')
        os.system('printf "fr_FR\n" |' + COMMAND % self.plugin_dir)
        dest_file_path = os.path.join(self.core_dir, 'i18n', 'fr_FR.json')
        self.assertTrue(os.path.exists(dest_file_path))
        with open(dest_file_path, 'r') as dest_file:
            content = dest_file.read()
            self.assertIn('content', content)
            self.assertIn('translate', content)

    def test_without_i18n_add_language(self):
        os.system('printf "o\nfr_FR\n" |' + COMMAND % self.plugin_dir)
        dest_file_path = os.path.join(self.core_dir, 'i18n', 'fr_FR.json')
        self.assertTrue(os.path.exists(dest_file_path))
        with open(dest_file_path, 'r') as dest_file:
            content = dest_file.read()
            self.assertIn('content', content)
            self.assertIn('translate', content)
