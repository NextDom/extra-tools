# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from scripts.libs.Jeedom import Jeedom


# noinspection PyUnusedLocal
class TestJeedom(unittest.TestCase):
    test_dir = None
    plugin_dir = None
    core_dir = None
    file_to_test1_path = None
    file_to_test2_path = None
    file_to_test3_path = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.plugin_dir = self.test_dir + os.sep + 'PluginName'
        self.core_dir = self.plugin_dir + os.sep + 'core'
        os.mkdir(self.plugin_dir)
        os.mkdir(self.core_dir)
        os.mkdir(self.plugin_dir + os.sep + 'desktop')
        os.mkdir(os.path.join(self.plugin_dir, 'desktop', 'php'))
        self.file_to_test1_path = self.plugin_dir + os.sep + 'file_to_test1.php'
        with open(self.file_to_test1_path, 'w') as file_to_test:
            file_to_test.write('A superb multi-line\ncontent\nwithout ' \
                               'things to translate, but\nonly useless text.')
        self.file_to_test2_path = self.core_dir + os.sep + 'file_to_test2.php'
        with open(self.file_to_test2_path, 'w') as file_to_test:
            file_to_test.write('A {{superb}} multi-line\ncontent\nwitho ' \
                               'things to {{translate}}, and\n useless text.')
        self.file_to_test3_path = os.path.join(self.plugin_dir, 'desktop',
                                               'php',
                                               'file_to_test3.php')
        with open(self.file_to_test3_path, 'w') as file_to_test:
            file_to_test.write('{{Another}} file with {{Another}} __('
                               '\'content\') __("Final")')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_transform_path_to_i18n_path(self):
        result = Jeedom.transform_path_to_i18n_path(
            self.plugin_dir, self.file_to_test2_path)
        self.assertEqual(result,
                         'plugins\\/PluginName\\/core\\/file_to_test2.php')

    def test_get_18n_path(self):
        result = Jeedom.get_i18n_path(self.plugin_dir)
        self.assertEqual(self.core_dir + os.sep + 'i18n', result)

    def test_is_valid_18n_name_valid_good(self):
        result = Jeedom.is_valid_i18n_name('fr_FR')
        self.assertTrue(result)
        result = Jeedom.is_valid_i18n_name('en_US')
        self.assertTrue(result)

    def test_is_valid_18n_name_valid_bad(self):
        result = Jeedom.is_valid_i18n_name('fra_FR')
        self.assertFalse(result)
        result = Jeedom.is_valid_i18n_name('fr_fr')
        self.assertFalse(result)
        result = Jeedom.is_valid_i18n_name('fr_FRA')
        self.assertFalse(result)
        result = Jeedom.is_valid_i18n_name('frFR')
        self.assertFalse(result)
        result = Jeedom.is_valid_i18n_name('1')
        self.assertFalse(result)

    def test_scan_file_from_string_without_string_to_translate(self):
        result = Jeedom.scan_file_for_strings(self.file_to_test1_path)
        self.assertEqual(result, [])

    def test_scan_file_from_string_with_strings_to_translate(self):
        result = Jeedom.scan_file_for_strings(self.file_to_test2_path)
        self.assertEqual(result, ['superb', 'translate'])

    def test_scan_for_strings(self):
        result = Jeedom.scan_for_strings(self.plugin_dir)
        self.assertEqual(self.file_to_test2_path, result[0]['file_path'])
        self.assertIn('translate', result[0]['items'])
        self.assertIn('superb', result[0]['items'])
        self.assertEqual(2, len(result[0]['items']))
        self.assertEqual(self.file_to_test3_path, result[1]['file_path'])
        self.assertIn('Another', result[1]['items'])
        self.assertIn('content', result[1]['items'])
        self.assertIn('Final', result[1]['items'])
        self.assertEqual(3, len(result[1]['items']))

    def test_merge_i18n_json_with_initial_data(self):
        initial_data = {'plugins\\/PluginName\\/file1.php': {'Item1': 'Item1'}}
        result_data = [{'file_path': 'file1.php',
                        'items': ['Item1', 'Item2']},
                       {
                           'file_path': 'core/file2.php',
                           'items': ['Bim',
                                     'Bam',
                                     'Boum']
                       }]
        result = Jeedom.merge_i18n_json('PluginName', initial_data, result_data)
        self.assertIn('plugins\\/PluginName\\/file1.php', result.keys())
        self.assertIn('Item2', result[
            'plugins\\/PluginName\\/file1.php'].keys())
        self.assertIn('plugins\\/PluginName\\/core\\/file2.php', result.keys())
        self.assertIn('Bam', result[
            'plugins\\/PluginName\\/core\\/file2.php'].keys())

    def test_merge_i18n_json_without_initial_data(self):
        result = Jeedom.merge_i18n_json(self.plugin_dir, {}, [
            {
                'file_path': 'file1.php',
                'items': ['Item1', 'Item2']
            },
            {
                'file_path': 'core/file2.php',
                'items': ['Bim', 'Bam', 'Boum']
            }])
        self.assertIn('plugins\\/PluginName\\/file1.php', result.keys())
        self.assertIn('Item1', result[
            'plugins\\/PluginName\\/file1.php'].keys())
        self.assertIn('plugins\\/PluginName\\/core\\/file2.php', result.keys())
        self.assertIn('Bim', result[
            'plugins\\/PluginName\\/core\\/file2.php'].keys())

    @patch('builtins.input', side_effect=['o'])
    def test_ask_for_i18n_folder_creation_y(self, side_effect):
        i18n_path = self.test_dir + os.sep + 'i18n'
        Jeedom.ask_for_i18n_folder_creation(i18n_path)
        self.assertTrue(os.path.exists(i18n_path))

    @patch('builtins.input', side_effect=['n'])
    def test_ask_for_i18n_folder_creation_n(self, side_effect):
        i18n_path = self.test_dir + os.sep + 'i18n'
        Jeedom.ask_for_i18n_folder_creation(i18n_path)
        self.assertFalse(os.path.exists(i18n_path))

    @patch('builtins.input', side_effect=['fr_FR'])
    def test_add_language(self, side_effect):
        i18n_path = self.core_dir + os.sep + 'i18n'
        os.mkdir(i18n_path)
        Jeedom.add_language(self.plugin_dir)
        self.assertTrue(os.path.exists(i18n_path + os.sep + 'fr_FR.json'))

    @patch('builtins.input', side_effect=['fr_FR', 'ee_EE'])
    def test_add_language_already_exists(self, side_effect):
        i18n_path = self.core_dir + os.sep + 'i18n'
        os.mkdir(i18n_path)
        open(i18n_path + os.sep + 'fr_FR.json', 'a').close()
        Jeedom.add_language(self.plugin_dir)
        self.assertTrue(os.path.exists(i18n_path + os.sep + 'fr_FR.json'))
        self.assertTrue(os.path.exists(i18n_path + os.sep + 'ee_EE.json'))

    @patch('builtins.input', side_effect=['fr', 'french', 'FR', 'FR_FR',
                                          'en_US'])
    def test_add_language_with_misstakes(self, side_effect):
        i18n_path = self.core_dir + os.sep + 'i18n'
        os.mkdir(i18n_path)
        Jeedom.add_language(self.plugin_dir)
        self.assertFalse(os.path.exists(i18n_path + os.sep + 'fr.json'))
        self.assertFalse(os.path.exists(i18n_path + os.sep + 'french.json'))
        self.assertFalse(os.path.exists(i18n_path + os.sep + 'FR.json'))
        self.assertFalse(os.path.exists(i18n_path + os.sep + 'FR_FR.json'))
        self.assertTrue(os.path.exists(i18n_path + os.sep + 'en_US.json'))
