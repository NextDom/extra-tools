# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
import unittest


COMMAND = './scripts/add_cron.py %s %s > /dev/null 2>&1'


# noinspection PyUnusedLocal
class TestCron(unittest.TestCase):
    test_dir = None
    target_ajax_directory = None
    target_ajax_file = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.plugin_dir = self.test_dir + os.sep + 'plugin-Test'
        self.class_dir = os.path.join(self.plugin_dir, 'core', 'class')
        os.mkdir(self.plugin_dir)
        os.mkdir(self.plugin_dir + os.sep + 'core')
        os.mkdir(self.class_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_without_cron_in_core_class(self):
        with open(self.class_dir + os.sep + 'Test.class.php', 'w') as test_file:
            test_file.write('require_once dirname(__FILE__)\nclass Test '
                            'extends eqLogic {\n\n}\n')
        os.system('printf "1\n" |'+COMMAND % (self.plugin_dir, 'Test'))
        with open(self.class_dir + os.sep + 'Test.class.php', 'r') as test_file:
            self.assertIn('public static function cron15', test_file.read())

    def test_with_cron_in_core_class(self):
        with open(self.class_dir + os.sep + 'Test.class.php', 'w') as test_file:
            test_file.write('require_once dirname(__FILE__)\nclass Test '
                            'extends eqLogic {\npublic static function '
                            'cron() {\n}\n}\n')
        os.system('printf "2\n" |'+COMMAND % (self.plugin_dir, 'Test'))
        with open(self.class_dir + os.sep + 'Test.class.php', 'r') as test_file:
            test_file_content = test_file.read()
            self.assertIn('public static function cron()', test_file_content)
            self.assertIn('public static function cron5()', test_file_content)

    def test_with_same_cron_in_core_class(self):
        with open(self.class_dir + os.sep + 'Test.class.php', 'w') as test_file:
            test_file.write('require_once dirname(__FILE__)\nclass Test '
                            'extends eqLogic {\npublic static function '
                            'cron() {\n}\n}\n')
        os.system('printf "3\n" |'+COMMAND % (self.plugin_dir, 'Test'))
        with open(self.class_dir + os.sep + 'Test.class.php', 'r') as test_file:
            test_file_content = test_file.read()
            self.assertIn('public static function cron()', test_file_content)
            self.assertEqual(1, test_file_content.count('cron()'))

