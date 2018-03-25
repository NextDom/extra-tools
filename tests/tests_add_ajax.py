# -*- coding: utf-8 -*-

import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__) + '/../scripts')
from scripts.add_ajax import add_ajax

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

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.target_ajax_directory = os.path.join(self.test_dir, 'core', 'ajax')
        self.target_ajax_file = os.path.join(self.test_dir, 'core', 'ajax',
                                             'TestPlugin.php')
        os.mkdir(self.test_dir + os.sep + 'core')
        os.mkdir(self.target_ajax_directory)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_file_without_directory(self):
        os.rmdir(self.target_ajax_directory)

        add_ajax(self.test_dir, 'TestPlugin')
        self.assertTrue(os.path.exists(self.target_ajax_file))

    def test_file_with_content_file(self):
        test_file_path = os.path.join(self.test_dir, 'core', 'ajax',
                                      'TestPlugin.ajax.php')
        with open(test_file_path, 'w') as test_dest:
            test_dest.write('ajax::init();')
        add_ajax(self.test_dir, 'TestPlugin')
        content = ''
        with open(test_file_path, 'r') as test_dest:
            content = test_dest.read()
        self.assertNotIn('<?php', content)
        self.assertNotIn('try', content)

    def test_without_file(self):
        test_file_path = os.path.join(self.test_dir, 'core', 'ajax',
                                      'TestPlugin.php')
        add_ajax(self.test_dir, 'TestPlugin')
        content = ''
        with open(test_file_path, 'r') as test_dest:
            content = test_dest.read()
        self.assertIn('<?php', content)
        self.assertIn('try', content)
        self.assertIn('ajax::init()', content)

    def test_without_good_content(self):
        test_file_path = os.path.join(self.test_dir, 'core', 'ajax',
                                      'TestPlugin.php')
        with open(test_file_path, 'w') as test_dest:
            test_dest.write('Test content')
        add_ajax(self.test_dir, 'TestPlugin')
        content = ''
        with open(test_file_path, 'r') as test_dest:
            content = test_dest.read()
        self.assertIn('<?php', content)
        self.assertIn('try', content)
        self.assertIn('ajax::init()', content)
