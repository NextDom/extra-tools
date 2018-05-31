# -*- coding: utf-8 -*-

import inspect
import os
import shutil
import sys
import unittest
from unittest.mock import patch

current_path = os.path.abspath(inspect.getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)
from tools import WizardMenu


# noinspection PyUnusedLocal
class TestWizard(unittest.TestCase):

    def tearDown(self):
        if os.path.exists('plugin-PluginName'):
            shutil.rmtree('plugin-PluginName')

    @patch('builtins.input', side_effect=['Plugin Name',
                                          'PluginName',
                                          '',
                                          '',
                                          '',
                                          '',
                                          '',
                                          '4',
                                          'n',
                                          '',
                                          ''])
    def test_default_choices(self, side_effect):
        with self.assertRaises(SystemExit):
            WizardMenu.start_wizard()
            plugin_dir = 'plugin-PluginName'
            info_json = os.path.join(plugin_dir, 'plugin_info', 'info.json')
            self.assertTrue(os.path.exists(os.path.join(plugin_dir, 'core',
                                                        'class',
                                                        'PluginName.class.php')))
            self.assertTrue(os.path.exists(os.path.join(plugin_dir, 'core',
                                                        'class',
                                                        'PluginNameCmd.class.php')))
            self.assertTrue(os.path.exists(info_json))
            with open(info_json, 'r') as info:
                info_content = info.read()
                self.assertIn('"id": "PluginName"', info_content)
                self.assertIn('"name": "Plugin Name', info_content)

    @patch('builtins.input', side_effect=['Plugin Name',
                                          'PluginName',
                                          'A small description',
                                          'AGPL',
                                          'Me',
                                          '2.0',
                                          '1.0.0',
                                          '3',
                                          'n',
                                          'en_US'])
    def test_choices(self, side_effect):
        with self.assertRaises(SystemExit):
            WizardMenu.start_wizard()
            plugin_dir = 'plugin-PluginName'
            info_json = os.path.join(plugin_dir, 'plugin_info', 'info.json')
            self.assertTrue(os.path.exists(os.path.join(plugin_dir, 'desktop',
                                                        'php',
                                                        'PluginName.php')))
            self.assertTrue(
                os.path.exists(os.path.join(plugin_dir, 'core', 'php')))
            self.assertTrue(os.path.exists(info_json))
            with open(info_json, 'r') as info:
                info_content = info.read()
                self.assertIn('"licence": "AGPL"', info_content)
                self.assertIn('"version": "1.0.0', info_content)

    @patch('builtins.input', side_effect=['Plugin Name',
                                          'PluginName',
                                          '',
                                          '',
                                          '',
                                          '',
                                          '',
                                          '5',
                                          'o',
                                          '1',
                                          'Name',
                                          'name',
                                          '2',
                                          'Valid ?',
                                          'valid',
                                          '0',
                                          'fr_FR'])
    def test_choices_with_config(self, side_effect):
        with self.assertRaises(SystemExit):
            WizardMenu.start_wizard()
            plugin_dir = 'plugin-PluginName'
            config = os.path.join(plugin_dir, 'plugin_info',
                                  'configuration.php')
            self.assertTrue(os.path.exists(config))
            with open(config, 'r') as config_file:
                config_content = config_file.read()
                self.assertIn('{{Name}}', config_content)
                self.assertIn(
                    '<input class="configKey form-control" data-l1key="name" '
                    '/>',
                    config_content)
                self.assertIn('{{Valid ?}}', config_content)
                self.assertIn(
                    '<input class="configKey form-control" type="checkbox" '
                    'data-l1key="valid" />',
                    config_content)

    @patch('builtins.input', side_effect=['0',
                                          '0'])
    def test_git_extratemplate(self, side_effect):
        WizardMenu.git_extratemplate()
        self.assertTrue(os.path.exists('plugin-ExtraTemplate'))
        shutil.rmtree('plugin-ExtraTemplate')

    @patch('builtins.input', side_effect=['0',
                                          '0'])
    def test_git_extratemplate(self, side_effect):
        os.system('mkdir plugin-ExtraTemplate')
        WizardMenu.git_extratemplate()
        self.assertFalse(os.path.exists('plugin-ExtraTemplate/plugin_info'))
        shutil.rmtree('plugin-ExtraTemplate')
