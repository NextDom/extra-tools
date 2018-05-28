# -*- coding: utf-8 -*-

import json
import os
import inspect
import shutil
import sys
import tempfile
import unittest

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
    i18n_dir = None
    i18n_menu = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.plugin_dir = self.test_dir + os.sep + 'plugin-Test'
        self.core_dir = os.path.join(self.plugin_dir, 'core')
        self.i18n_dir = os.path.join(self.core_dir, 'i18n')
        self.i18n_menu = I18nMenu(self.plugin_dir, 'Test')
        os.mkdir(self.plugin_dir)
        os.mkdir(self.core_dir)
        os.mkdir(self.i18n_dir)
        os.mkdir(self.plugin_dir + os.sep + 'desktop')
        with open(os.path.join(self.plugin_dir, 'desktop', 'test.php'),
                  'w') as to_translate:
            to_translate.write('A small {{content}} to {{translate}}.')
        with open(os.path.join(self.plugin_dir, 'desktop', 'test2.php'),
                  'w') as to_translate:
            to_translate.write('Another {{thing}}.')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_added_file_to_translate(self):
        base_fr = '{ \
            "plugins\\/plugin-Test\\/desktop\\/test.php": { \
                "content": "content", \
                "translate": "translate" \
            } \
        }'
        with open(self.i18n_dir + os.sep + 'fr_FR.json', 'w') as sample:
            sample.write(base_fr)
        # os.system(COMMAND % self.plugin_dir)
        self.i18n_menu.update_languages()
        with open(self.i18n_dir + os.sep + 'fr_FR.json', 'r') as sample:
            content = json.load(sample)
            self.assertIn('plugins/plugin-Test/desktop/test2.php',
                          content.keys())
            self.assertEqual('thing', content[
                'plugins/plugin-Test/desktop/test2.php']['thing'])

    def test_new_content(self):
        base_fr = '{ \
            "plugins\\/plugin-Test\\/desktop\\/test.php": { \
                "content": "content" \
            } \
        }'
        with open(self.i18n_dir + os.sep + 'fr_FR.json', 'w') as sample:
            sample.write(base_fr)
        self.i18n_menu.update_languages()
        with open(self.i18n_dir + os.sep + 'fr_FR.json', 'r') as sample:
            content = json.load(sample)
            self.assertEqual('translate', content[
                'plugins/plugin-Test/desktop/test.php']['translate'])

    def test_new_language(self):
        base_fr = '{ \
            "plugins\\/plugin-Test\\/desktop\\/test.php": { \
                "content": "content", \
                "translate": "translate" \
            } \
        }'

        with open(self.i18n_dir + os.sep + 'fr_FR.json', 'w') as sample:
            sample.write(base_fr)
        open(self.i18n_dir + os.sep + 'en_US.json', 'a').close()
        self.i18n_menu.update_languages()
        with open(self.i18n_dir + os.sep + 'en_US.json', 'r') as sample:
            content = json.load(sample)
            self.assertIn('plugins/plugin-Test/desktop/test2.php',
                          content.keys())
            self.assertEqual('thing', content[
                'plugins/plugin-Test/desktop/test2.php']['thing'])
