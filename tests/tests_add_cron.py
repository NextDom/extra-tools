# -*- coding: utf-8 -*-

import os
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(__file__) + '/../scripts')
from scripts.add_cron import add_cron


# noinspection PyUnusedLocal
class TestCron(unittest.TestCase):
    test_dir = None
    plugin_dir = None
    class_dir = None
    core_file_path = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.plugin_dir = self.test_dir + os.sep + 'plugin-Test'
        self.class_dir = os.path.join(self.plugin_dir, 'core', 'class')
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
        add_cron(self.plugin_dir, 'Test')
        with open(self.core_file_path, 'r') as core_file:
            self.assertIn('public static function cron(', core_file.read())

    @patch('builtins.input', side_effect=['2'])
    def test_with_cron_in_core_class(self, side_effect):
        with open(self.core_file_path, 'w') as test_file:
            test_file.write('require_once dirname(__FILE__)\nclass Test '
                            'extends eqLogic {\npublic static function '
                            'cron() {\n}\n}\n')
        add_cron(self.plugin_dir, 'Test')
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
        add_cron(self.plugin_dir, 'Test')
        with open(self.core_file_path, 'r') as test_file:
            test_file_content = test_file.read()
            self.assertIn('public static function cron()', test_file_content)
            self.assertEqual(1, test_file_content.count('cron()'))
