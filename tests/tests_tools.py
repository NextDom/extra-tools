# -*- coding: utf-8 -*-

import unittest
import tempfile
from unittest.mock import patch
from unittest import mock
import os
import tools
import shutil

INFO_JSON_CONTENT = "{" + \
      "\"id\": \"PluginId\"," + \
      "\"name\": \"PluginName\"" + \
    "}"

class TestTools(unittest.TestCase):
    test_dir = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_parse_args_simple_help(self):
        argv = ['script_path', '--help']
        result = tools.parse_args(argv)
        self.assertIsNone(result)

    def test_parse_args_help_with_too_much_args(self):
        argv = ['script_path', '--help', 'test']
        result = tools.parse_args(argv)
        self.assertIsNone(result)

    def test_parse_args_too_much_args(self):
        argv = ['script_path', 'first', 'second']
        result = tools.parse_args(argv)
        self.assertIsNone(result)

    def test_parse_args_with_plugin_name(self):
        argv = ['script_path', 'myPlugin']
        result = tools.parse_args(argv)
        self.assertEqual(result, 'myPlugin')

    @patch('os.path.exists')
    def test_is_plugin_dir_good(self, mock_exists):
        mock_exists.return_value = True
        self.assertTrue(tools.is_plugin_dir('.'))

    @patch('os.path.exists')
    def test_is_plugin_dir_bad(self, mock_exists):
        mock_exists.return_value = False
        self.assertFalse(tools.is_plugin_dir('.'))

    @patch('builtins.open', new_callable=mock.mock_open,
                            read_data=INFO_JSON_CONTENT)
    def test_get_plugin_data_good_data(self, mock_file):
        result = tools.get_plugin_data('PluginIdPath')
        self.assertEqual(result, ['PluginIdPath', 'PluginId'])

    @patch('builtins.open', new_callable=mock.mock_open,
                            read_data="")
    def test_get_plugin_data_no_data(self, mock_file):
        result = tools.get_plugin_data('PluginIdPath')
        self.assertIsNone(result)

    def test_get_plugins_in_dir_with_one(self):
        # Création de fichiers temporaires
        plugin_dir = self.test_dir + os.sep + 'plugin_dir'
        os.mkdir(self.test_dir + os.sep + 'useless_dir')
        os.mkdir(self.test_dir + os.sep + 'plugin_dir')
        os.mkdir(self.test_dir + os.sep + 'another_useless_dir')
        os.mkdir(plugin_dir + os.sep + 'plugin_info')
        with open(os.path.join(plugin_dir, 'plugin_info',
                               'info.json'), 'w') as info_file:
            info_file.write(INFO_JSON_CONTENT)
        result = tools.get_plugins_in_dir(self.test_dir)
        self.assertEqual(result, [[plugin_dir, 'PluginId']])

    def test_get_plugins_in_dir_with_no_one(self):
        # Création de fichiers temporaires
        plugin_dir = self.test_dir + os.sep + 'plugin_dir'
        os.mkdir(self.test_dir + os.sep + 'useless_dir')
        result = tools.get_plugins_in_dir(self.test_dir)
        self.assertEqual(result, [])
