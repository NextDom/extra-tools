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
class TestInterface(unittest.TestCase):
    wizard_menu = None
    skip_download = False

    @classmethod
    def setUpClass(cls):
        os.system('mkdir tmp')
        if os.path.exists('for_tests/plugin-ExtraTemplate'):
            os.system('cp -fr for_tests/plugin-ExtraTemplate tmp')
        else:
            os.system(
                'git clone https://github.com/NextDom/plugin-ExtraTemplate > '
                '/dev/null 2>&1')
            os.system('mv plugin-ExtraTemplate tmp')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree('tmp')

    def setUp(self):
        os.system('cp -fr tmp/plugin-ExtraTemplate .')
        plugins_list = [['plugin-ExtraTemplate', 'ExtraTemplate']]
        self.wizard_menu = WizardMenu(plugins_list)

    def tearDown(self):
        if os.path.exists('plugin-ExtraTemplate'):
            shutil.rmtree('plugin-ExtraTemplate')

    @patch('builtins.input', side_effect=['2',
                                          '',
                                          ''])
    def test_git_download(self, side_effect):
        shutil.rmtree('plugin-ExtraTemplate')
        self.wizard_menu = WizardMenu([])
        self.wizard_menu.start()
        self.assertTrue(os.path.exists('plugin-ExtraTemplate'))

    @patch('builtins.input', side_effect=['2',
                                          '1',
                                          'Test',
                                          '',
                                          ''])
    def test_change_id(self, side_effect):
        self.wizard_menu.start()
        self.assertTrue(os.path.exists('plugin-Test'))
        shutil.rmtree('plugin-Test')

    @patch('builtins.input', side_effect=['2',
                                          '2',
                                          '1',
                                          'Test',
                                          '',
                                          '',
                                          ''])
    def test_change_name(self, side_effect):
        self.wizard_menu.start()
        with open('plugin-ExtraTemplate/plugin_info/info.json', 'r') as info_file:
            content = info_file.read()
            self.assertIn('"name": "Test",', content)

    @patch('builtins.input', side_effect=['2',
                                          '2',
                                          '2',
                                          'Test',
                                          '',
                                          '',
                                          ''])
    def test_change_description(self, side_effect):
        self.wizard_menu.start()
        with open('plugin-ExtraTemplate/plugin_info/info.json', 'r') as \
                info_file:
            content = info_file.read()
            self.assertIn('"description": "Test",', content)

    @patch('builtins.input', side_effect=['2',
                                          '2',
                                          '3',
                                          'AGPL',
                                          '',
                                          '',
                                          ''])
    def test_change_license(self, side_effect):
        self.wizard_menu.start()
        with open('plugin-ExtraTemplate/plugin_info/info.json', 'r') as info_file:
            content = info_file.read()
            self.assertIn('"licence": "AGPL",', content)

    @patch('builtins.input', side_effect=['2',
                                          '2',
                                          '4',
                                          'Me',
                                          '',
                                          '',
                                          ''])
    def test_change_author(self, side_effect):
        self.wizard_menu.start()
        with open('plugin-ExtraTemplate/plugin_info/info.json', 'r') as info_file:
            content = info_file.read()
            self.assertIn('"author": "Me",', content)

