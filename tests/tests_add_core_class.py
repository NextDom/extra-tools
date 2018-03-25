# -*- coding: utf-8 -*-

import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__) + '/../scripts')
from scripts.add_core_class import add_core_class

COMMAND = './scripts/add_core_class.py %s %s > /dev/null 2>&1'


# noinspection PyUnusedLocal
class TestAddCoreClass(unittest.TestCase):
    test_dir = None
    plugin_dir = None
    class_dir = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.plugin_dir = self.test_dir + os.sep + 'plugin-Test'
        self.class_dir = os.path.join(self.plugin_dir, 'core', 'class')
        os.mkdir(self.plugin_dir)
        os.mkdir(self.plugin_dir + os.sep + 'core')
        os.mkdir(self.class_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_without_core_class(self):
        add_core_class(self.plugin_dir, 'Test')
        #        os.system(COMMAND % (self.plugin_dir, 'Test'))
        self.assertTrue(os.path.exists(self.class_dir + os.sep +
                                       'Test.class.php'))
        with open(self.class_dir + os.sep + 'Test.class.php', 'r') as test_file:
            self.assertIn('Test extends eqLogic', test_file.read())

    def test_with_core_class(self):
        with open(self.class_dir + os.sep + 'Test.class.php', 'w') as test_file:
            test_file.write('Keep this content')
        add_core_class(self.plugin_dir, 'Test')
        #        os.system(COMMAND % (self.plugin_dir, 'Test'))
        self.assertTrue(os.path.exists(self.class_dir + os.sep +
                                       'Test.class.php'))
        with open(self.class_dir + os.sep + 'Test.class.php', 'r') as test_file:
            self.assertIn('Keep this content', test_file.read())
