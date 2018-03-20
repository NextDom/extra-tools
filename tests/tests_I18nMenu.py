# -*- coding: utf-8 -*-
import os
import shutil
import tempfile
import unittest

from libs.I18nMenu import I18nMenu


class TestI18nMenu(unittest.TestCase):
    test_dir = None
    i18n_menu = None
    plugin_dir = None
    file_to_test1_path = None
    file_to_test2_path = None
    file_to_test3_path = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.plugin_dir = self.test_dir + os.sep + 'PluginName'
        self.i18n_menu = I18nMenu(self.plugin_dir, 'PluginName')
        os.mkdir(self.plugin_dir)
        os.mkdir(self.plugin_dir + os.sep + 'core')
        os.mkdir(self.plugin_dir + os.sep + 'desktop')
        os.mkdir(os.path.join(self.plugin_dir, 'desktop', 'php'))
        self.file_to_test1_path = self.plugin_dir + os.sep + 'file_to_test1.php'
        with open(self.file_to_test1_path, 'w') as file_to_test:
            file_to_test.write('A superb multi-line\ncontent\nwithout ' \
                               'things to translate, but\nonly useless text.')
        self.file_to_test2_path = os.path.join(self.plugin_dir, 'core',
                                               'file_to_test2.php')
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
        shutil.rmtree(self.plugin_dir)

    def test_get_18n_path(self):
        result = self.i18n_menu.get_i18n_path()
        self.assertEqual(os.path.join(self.plugin_dir, 'core', 'i18n'), result)

    def test_write_json_file(self):
        data = {
            '\\/coucou\\/': 'Plouf',
            'bla': 'è&ça °'
        }
        to_compare = '{\n    "\\/coucou\\/": "Plouf",\n    "bla": "è&ça °"\n}\n'
        test_file_path = self.test_dir + os.sep + 'json_test'
        result = I18nMenu.write_json_file(test_file_path, data)
        self.assertTrue(result)
        content = ''
        with open(test_file_path, 'r') as test_file:
            content = test_file.read()
        self.assertEqual(content, to_compare)

    def test_is_valid_18n_name_valid_good(self):
        result = I18nMenu.is_valid_i18n_name('fr_FR')
        self.assertTrue(result)
        result = I18nMenu.is_valid_i18n_name('en_US')
        self.assertTrue(result)

    def test_is_valid_18n_name_valid_bad(self):
        result = I18nMenu.is_valid_i18n_name('fra_FR')
        self.assertFalse(result)
        result = I18nMenu.is_valid_i18n_name('fr_fr')
        self.assertFalse(result)
        result = I18nMenu.is_valid_i18n_name('fr_FRA')
        self.assertFalse(result)
        result = I18nMenu.is_valid_i18n_name('frFR')
        self.assertFalse(result)
        result = I18nMenu.is_valid_i18n_name('1')
        self.assertFalse(result)

    def test_scan_file_from_string_without_string_to_translate(self):
        result = I18nMenu.scan_file_for_strings(self.file_to_test1_path)
        self.assertEqual(result, [])

    def test_scan_file_from_string_with_strings_to_translate(self):
        result = I18nMenu.scan_file_for_strings(self.file_to_test2_path)
        self.assertEqual(result, ['superb', 'translate'])

    def test_scan_for_strings(self):
        result = I18nMenu.scan_for_strings(self.plugin_dir)
        self.assertEqual(self.file_to_test2_path, result[0]['file_path'])
        self.assertIn('translate', result[0]['items'])
        self.assertIn('superb', result[0]['items'])
        self.assertEqual(2, len(result[0]['items']))
        self.assertEqual(self.file_to_test3_path, result[1]['file_path'])
        self.assertIn('Another', result[1]['items'])
        self.assertIn('content', result[1]['items'])
        self.assertIn('Final', result[1]['items'])
        self.assertEqual(3, len(result[1]['items']))

    def test_transform_path_to_i18n_path(self):
        result = self.i18n_menu.transform_path_to_i18n_path(
            self.file_to_test2_path)
        self.assertEqual(result,
                         'plugins\\/PluginName\\/core\\/file_to_test2.php')

    def test_merge_i18n_json_without_initial_data(self):
        result = self.i18n_menu.merge_i18n_json({}, [
            {
                'file_path': self.plugin_dir + os.sep + 'file1.php',
                'items': ['Item1', 'Item2']
            },
            {
                'file_path': self.plugin_dir + os.sep + 'core' + os.sep
                             + 'file2.php',
                'items': ['Bim', 'Bam', 'Boum']
            }])
        self.assertIn('plugins\\/PluginName\\/file1.php', result.keys())
        self.assertIn('Item1', result[
            'plugins\\/PluginName\\/file1.php'].keys())
        self.assertIn('plugins\\/PluginName\\/core\\/file2.php', result.keys())
        self.assertIn('Bim', result[
            'plugins\\/PluginName\\/core\\/file2.php'].keys())

    def test_merge_i18n_json_with_initial_data(self):
        result = self.i18n_menu.merge_i18n_json({
            'plugins\\/PluginName\\/file1.php': {
                'Item1': 'Item1'
            }
        }, [{
            'file_path': self.plugin_dir + os.sep + 'file1.php',
            'items': ['Item1', 'Item2']
        }, {
            'file_path': self.plugin_dir + os.sep + 'core' + os.sep
                         + 'file2.php',
            'items': ['Bim', 'Bam', 'Boum']
        }])
        self.assertIn('plugins\\/PluginName\\/file1.php', result.keys())
        self.assertIn('Item2', result[
            'plugins\\/PluginName\\/file1.php'].keys())
        self.assertIn('plugins\\/PluginName\\/core\\/file2.php', result.keys())
        self.assertIn('Bam', result[
            'plugins\\/PluginName\\/core\\/file2.php'].keys())
