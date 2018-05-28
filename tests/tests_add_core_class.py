# -*- coding: utf-8 -*-

import inspect
import os
import shutil
import sys
import tempfile
import unittest

current_path = os.path.abspath(inspect.getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)
from tools import FeaturesMenu

COMMAND = './scripts/add_core_class.py %s %s > /dev/null 2>&1'


# noinspection PyUnusedLocal
class TestAddCoreClass(unittest.TestCase):
    test_dir = None
    plugin_dir = None
    class_dir = None
    features_menu = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.plugin_dir = self.test_dir + os.sep + 'plugin-Test'
        self.class_dir = os.path.join(self.plugin_dir, 'core', 'class')
        self.features_menu = FeaturesMenu(self.plugin_dir, 'Test')
        os.mkdir(self.plugin_dir)
        os.mkdir(self.plugin_dir + os.sep + 'core')
        os.mkdir(self.class_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_without_core_class(self):
        self.features_menu.add_core_class()
        #        os.system(COMMAND % (self.plugin_dir, 'Test'))
        self.assertTrue(os.path.exists(self.class_dir + os.sep +
                                       'Test.class.php'))
        with open(self.class_dir + os.sep + 'Test.class.php', 'r') as test_file:
            self.assertIn('Test extends eqLogic', test_file.read())

    def test_with_core_class(self):
        with open(self.class_dir + os.sep + 'Test.class.php', 'w') as test_file:
            test_file.write('Keep this content')
        self.features_menu.add_core_class()
        #        os.system(COMMAND % (self.plugin_dir, 'Test'))
        self.assertTrue(os.path.exists(self.class_dir + os.sep +
                                       'Test.class.php'))
        with open(self.class_dir + os.sep + 'Test.class.php', 'r') as test_file:
            self.assertIn('Keep this content', test_file.read())
