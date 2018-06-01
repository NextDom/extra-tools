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
from tools import FeaturesMenu

# noinspection PyUnusedLocal
class TestCron(unittest.TestCase):
    test_dir = None
    plugin_dir = None
    class_dir = None
    core_file_path = None
    features_menu = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.plugin_dir = self.test_dir + os.sep + 'plugin-Test'
        self.class_dir = os.path.join(self.plugin_dir, 'core', 'class')
        self.features_menu = FeaturesMenu(self.plugin_dir, 'Test')
        os.mkdir(self.plugin_dir)
        os.mkdir(self.plugin_dir + os.sep + 'core')
        os.mkdir(self.class_dir)
        self.core_file_path = self.class_dir + os.sep + 'Test.class.php'

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch('builtins.input', side_effect=['1'])
    def test_without_cron_in_core_class(self, side_effect):
        with open(self.core_file_path, 'w') as core_file:
            core_file.write('require_once dirname(__FILE__)\nclass Test '
                            'extends eqLogic {\n\n}\n')
        self.features_menu.add_cron()
        with open(self.core_file_path, 'r') as core_file:
            self.assertIn('public static function cron(', core_file.read())

    @patch('builtins.input', side_effect=['2'])
    def test_with_cron_in_core_class(self, side_effect):
        with open(self.core_file_path, 'w') as test_file:
            test_file.write('require_once dirname(__FILE__)\nclass Test '
                            'extends eqLogic {\npublic static function '
                            'cron() {\n}\n}\n')
        self.features_menu.add_cron()
        with open(self.core_file_path, 'r') as test_file:
            test_file_content = test_file.read()
            self.assertIn('public static function cron()', test_file_content)
            self.assertIn('public static function cron5()', test_file_content)

    @patch('builtins.input', side_effect=['3'])
    def test_with_same_cron_in_core_class(self, side_effect):
        with open(self.core_file_path, 'w') as test_file:
            test_file.write('require_once dirname(__FILE__)\nclass Test '
                            'extends eqLogic {\npublic static function '
                            'cron() {\n}\n}\n')
        self.features_menu.add_cron()
        with open(self.core_file_path, 'r') as test_file:
            test_file_content = test_file.read()
            self.assertIn('public static function cron()', test_file_content)
            self.assertEqual(1, test_file_content.count('cron()'))
