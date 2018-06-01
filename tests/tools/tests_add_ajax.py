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

INFO_JSON_CONTENT = "{" + \
                    "\"id\": \"PluginId\"," + \
                    "\"name\": \"PluginName\"," + \
                    "\"data\": \"useless\"" + \
                    "}"


# noinspection PyUnusedLocal
class TestAddAjax(unittest.TestCase):
    test_dir = None
    target_ajax_directory = None
    target_ajax_file = None
    feature_menu = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.target_ajax_directory = os.path.join(self.test_dir, 'core', 'ajax')
        self.target_ajax_file = os.path.join(self.test_dir, 'core', 'ajax',
                                             'TestPlugin.ajax.php')
        self.feature_menu = FeaturesMenu(self.test_dir, 'TestPlugin')
        os.mkdir(self.test_dir + os.sep + 'core')
        os.mkdir(self.target_ajax_directory)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_file_without_directory(self):
        os.rmdir(self.target_ajax_directory)

        self.feature_menu.add_ajax()
        self.assertTrue(os.path.exists(self.target_ajax_directory))
        self.assertTrue(os.path.exists(self.target_ajax_file))

    def test_file_with_good_content(self):
        with open(self.target_ajax_file, 'w') as test_dest:
            test_dest.write('ajax::init();')
        self.feature_menu.add_ajax()
        content = ''
        with open(self.target_ajax_file, 'r') as test_dest:
            content = test_dest.read()
        self.assertNotIn('<?php', content)
        self.assertNotIn('try', content)

    def test_without_file(self):
        self.feature_menu.add_ajax()
        content = ''
        with open(self.target_ajax_file, 'r') as test_dest:
            content = test_dest.read()
        self.assertIn('<?php', content)
        self.assertIn('try', content)
        self.assertIn('ajax::init()', content)

    def test_without_bad_content(self):
        with open(self.target_ajax_file, 'w') as test_dest:
            test_dest.write('Test content')
            self.feature_menu.add_ajax()
        content = ''
        with open(self.target_ajax_file, 'r') as test_dest:
            content = test_dest.read()
        self.assertNotIn('<?php', content)
        self.assertNotIn('try', content)
        self.assertNotIn('ajax::init()', content)
