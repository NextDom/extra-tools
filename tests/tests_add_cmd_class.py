# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
import unittest


COMMAND = './scripts/add_cmd_class.py %s %s > /dev/null 2>&1'


# noinspection PyUnusedLocal
class TestAddCmdClass(unittest.TestCase):
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

    def test_without_core_class_and_separate_files(self):
        os.system('printf "o\no\n" |'+COMMAND % (self.plugin_dir, 'Test'))
        self.assertTrue(os.path.exists(self.class_dir + os.sep +
                                        'Test.class.php'))
        with open(self.class_dir + os.sep + 'Test.class.php', 'r') as test_file:
            self.assertIn('require_once \'./TestCmd', test_file.read())
        self.assertTrue(os.path.exists(self.class_dir + os.sep +
                                        'TestCmd.class.php'))

    def test_without_core_class_and_one_file(self):
        os.system('printf "o\nn\n" |'+COMMAND % (self.plugin_dir, 'Test'))
        self.assertTrue(os.path.exists(self.class_dir + os.sep +
                                        'Test.class.php'))
        with open(self.class_dir + os.sep + 'Test.class.php', 'r') as test_file:
            test_file_content = test_file.read()
            self.assertNotIn('require_once \'./TestCmd', test_file_content)
            self.assertIn('TestCmd', test_file_content)

    def test_with_core_class_and_separate_files(self):
        with open(self.class_dir + os.sep + 'Test.class.php', 'w') as test_file:
            test_file.write('require_once dirname(__FILE__)\nclass Test '
                            'extends eqLogic {\n\n}\n')
        os.system('printf "o\n" |'+COMMAND % (self.plugin_dir, 'Test'))
        with open(self.class_dir + os.sep + 'Test.class.php', 'r') as test_file:
            self.assertIn('require_once \'./TestCmd', test_file.read())
        self.assertTrue(os.path.exists(self.class_dir + os.sep +
                                        'TestCmd.class.php'))

    def test_with_core_class_and_one_file(self):
        with open(self.class_dir + os.sep + 'Test.class.php', 'w') as test_file:
            test_file.write('require_once dirname(__FILE__)\nclass Test '
                            'extends eqLogic {\n\n}\n')
        os.system('printf "n\n" |'+COMMAND % (self.plugin_dir, 'Test'))
        with open(self.class_dir + os.sep + 'Test.class.php', 'r') as test_file:
            test_file_content = test_file.read()
            self.assertNotIn('require_once \'./TestCmd', test_file_content)
            self.assertIn('TestCmd', test_file_content)

