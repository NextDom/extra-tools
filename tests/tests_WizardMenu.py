# -*- coding: utf-8 -*-
import json
import os
import shutil
import tempfile
import unittest

from unittest.mock import call
from unittest.mock import patch

from libs.WizardMenu import WizardMenu

WIZARD_ANSWERS = ['Plugin Name',
                  'PluginName',
                  'A small description',
                  'AGPL',
                  'Me',
                  '2.0',
                  '1.0.0',
                  '3',
                  'n',
                  'en_US']

WIZARD_ALL_DEFAULT_ANSWERS = ['Plugin Name',
                              'Plugin_name',
                              '',
                              '',
                              '',
                              '',
                              '',
                              '4',
                              '',
                              '',
                              '']

WIZARD_CONFIGURATION = ['Plugin Name',
                        'PluginName',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '5',
                        'o',
                        1,
                        'Name',
                        'name',
                        2,
                        'Valid ?',
                        'valid',
                        0,
                        'fr_FR']

PLUGIN_CONFIGURATION = {'author': '',
                        'category': 'weather',
                        'configuration': [
                            {'code': 'name', 'label': 'Name', 'type': 'text'},
                            {'code': 'valid', 'label': 'Valid ?',
                             'type': 'checkbox'}],
                        'core_path': 'plugin-PluginName' + os.sep + 'core' + os.sep,
                        'description': '',
                        'desktop_path': 'plugin-PluginName' + os.sep + 'desktop' + os.sep,
                        'documentation_language': 'fr_FR',
                        'id': 'PluginName',
                        'license': 'GPL',
                        'name': 'Plugin Name',
                        'plugin_info_path': 'plugin-PluginName' + os.sep + 'plugin_info' + os.sep,
                        'require': '3.0',
                        'version': '1.0'}


class TestWizardMenu(unittest.TestCase):
    test_dir = None
    wizard_menu = None
    plugin_data = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.wizard_menu = WizardMenu([['plugin-alpha', 'Alpha'],
                                       ['plugin-beta', 'Beta']])

        self.plugin_data = PLUGIN_CONFIGURATION.copy()
        self.plugin_data['core_path'] = self.plugin_data['core_path'].replace(
            'plugin-PluginName', self.test_dir)
        self.plugin_data['desktop_path'] = self.plugin_data[
            'desktop_path'].replace('plugin-PluginName', self.test_dir)
        self.plugin_data['plugin_info_path'] = self.plugin_data[
            'plugin_info_path'].replace('plugin-PluginName', self.test_dir)
        os.mkdir(self.test_dir + os.sep + 'plugin_info')
        os.mkdir(self.test_dir + os.sep + 'core')
        os.mkdir(self.test_dir + os.sep + 'core' + os.sep + 'class')
        os.mkdir(self.test_dir + os.sep + 'desktop')
        os.mkdir(self.test_dir + os.sep + 'desktop' + os.sep + 'php')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_constructor(self):
        self.assertEqual(self.wizard_menu.menu,
                         ['Démarrer l\'assistant',
                          'Télécharger le plugin Template',
                          'Modifier le plugin Alpha',
                          'Modifier le plugin Beta'])

    def test_constructor_with_template(self):
        self.wizard_menu = WizardMenu([['plugin-alpha', 'Alpha'],
                                       ['plugin-beta', 'Beta'],
                                       ['plugin-template', 'Template']])
        self.assertEqual(self.wizard_menu.menu,
                         ['Démarrer l\'assistant',
                          'Modifier le plugin Alpha',
                          'Modifier le plugin Beta',
                          'Modifier le plugin Template'])

    @patch('builtins.input', side_effect=WIZARD_ANSWERS)
    def test_ask_plugin_informations(self, side_effect):
        result = self.wizard_menu.ask_plugin_informations()
        self.assertEqual('Plugin Name', result['name'])
        self.assertEqual('PluginName', result['id'])
        self.assertEqual('A small description', result['description'])
        self.assertEqual('AGPL', result['license'])
        self.assertEqual('Me', result['author'])
        self.assertEqual('2.0', result['require'])
        self.assertEqual('1.0.0', result['version'])
        self.assertEqual('programming', result['category'])
        self.assertIsNone(result['configuration'])
        self.assertEqual('plugin-PluginName' + os.sep + 'core' + os.sep,
                         result['core_path'])

    @patch('builtins.input', side_effect=WIZARD_ALL_DEFAULT_ANSWERS)
    def test_ask_plugin_informations_default(self, side_effect):
        result = self.wizard_menu.ask_plugin_informations()
        self.assertEqual('Plugin Name', result['name'])
        self.assertEqual('Plugin_name', result['id'])
        self.assertEqual('', result['description'])
        self.assertEqual('GPL', result['license'])
        self.assertEqual('', result['author'])
        self.assertEqual('3.0', result['require'])
        self.assertEqual('1.0', result['version'])
        self.assertEqual('organization', result['category'])
        self.assertEqual([], result['configuration'])
        self.assertEqual('plugin-Plugin_name' + os.sep + 'desktop' + os.sep,
                         result['desktop_path'])

    @patch('builtins.input', side_effect=WIZARD_CONFIGURATION)
    def test_ask_plugin_configuration(self, side_effect):
        result = self.wizard_menu.ask_plugin_informations()
        self.assertEqual('weather', result['category'])
        self.assertEqual(result['configuration'], [{
            'type': 'text',
            'label': 'Name',
            'code': 'name'
        }, {
            'type': 'checkbox',
            'label': 'Valid ?',
            'code': 'valid'

        }])

    @patch('os.mkdir')
    @patch('builtins.open')
    def test_create_folder_struct(self, mocked_open, mocked_mkdir):
        self.wizard_menu.create_folder_struct(PLUGIN_CONFIGURATION)
        mkdir_calls = [
            call('plugin-PluginName'),
            call('plugin-PluginName' + os.sep + 'core'),
            call('plugin-PluginName' + os.sep + 'desktop'),
            call('plugin-PluginName' + os.sep + 'docs'),
            call('plugin-PluginName' + os.sep + 'plugin_info'),
            call(
                'plugin-PluginName' + os.sep + 'desktop' + os.sep + 'css'),
            call(
                'plugin-PluginName' + os.sep + 'desktop' + os.sep + 'js'),
            call(
                'plugin-PluginName' + os.sep + 'desktop' + os.sep + 'modal'),
            call(
                'plugin-PluginName' + os.sep + 'desktop' + os.sep + 'php'),
            call(
                'plugin-PluginName' + os.sep + 'core' + os.sep + 'ajax'),
            call(
                'plugin-PluginName' + os.sep + 'core' + os.sep + 'class'),
            call(
                'plugin-PluginName' + os.sep + 'core' + os.sep + 'php'),
            call(
                'plugin-PluginName' + os.sep + 'docs' + os.sep + 'fr_FR')]
        mocked_mkdir.assert_has_calls(mkdir_calls)
        open_calls = [call('plugin-PluginName' + os.sep + 'LICENSE', 'w'),
                      call().close()]
        mocked_open.assert_has_calls(open_calls)

    def test_gen_info_json(self):
        self.plugin_data['author'] = 'Me'
        self.plugin_data['description'] = 'A small description'

        self.wizard_menu.gen_info_json(self.plugin_data)

        with open(self.plugin_data['plugin_info_path'] + 'info.json',
                  'r') as info:
            json_info = json.loads(info.read())
            self.assertEqual(json_info['author'], 'Me')
            self.assertEqual(json_info['category'], 'weather')
            self.assertEqual(json_info['description'], 'A small description')
            self.assertEqual(json_info['id'], 'PluginName')
            self.assertEqual(json_info['licence'], 'GPL')
            self.assertEqual(json_info['require'], '3.0')
            self.assertEqual(json_info['version'], '1.0')

    def test_gen_installation_php(self):
        self.wizard_menu.gen_installation_php(self.plugin_data)

        with open(self.plugin_data['plugin_info_path'] + 'installation.php',
                  'r') as configuration:
            content = configuration.read()
            self.assertIn('function PluginName_install', content)
            self.assertIn('function PluginName_update', content)
            self.assertIn('function PluginName_remove', content)

    def test_gen_configuration(self):
        self.wizard_menu.gen_configuration(self.plugin_data)

        with open(self.plugin_data['plugin_info_path'] + 'configuration.php',
                  'r') as configuration:
            content = configuration.read()
            self.assertIn(
                '<input class="configKey form-control" data-l1key="name" />',
                content)
            self.assertIn(
                '<input class="configKey form-control" type="checkbox" '
                'data-l1key="valid" />', content)

    def test_gen_desktop_php(self):
        self.wizard_menu.gen_desktop_php(self.plugin_data)

        with open(os.path.join(self.plugin_data['desktop_path'], 'php',
                               'PluginName.php'),
                  'r') as desktop:
            content = desktop.read()
        self.assertIn('<?php', content)

    def test_gen_core_php(self):
        self.wizard_menu.gen_core_php(self.plugin_data)

        with open(os.path.join(self.plugin_data['core_path'], 'class',
                               'PluginName.class.php'),
                  'r') as desktop:
            content = desktop.read()
            self.assertIn('class PluginName extends eqLogic', content)
            self.assertIn('class PluginNameCmd extends cmd', content)
            self.assertIn('function execute(', content)
