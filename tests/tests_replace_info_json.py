# -*- coding: utf-8 -*-

import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__) + '/../scripts')
from scripts.replace_info_json import replace_info_json

INFO_JSON_CONTENT = "{" + \
                    "\"id\": \"PluginId\"," + \
                    "\"name\": \"PluginName\"," + \
                    "\"data\": \"useless\"" + \
                    "}"


# noinspection PyUnusedLocal
class TestReplaceInfo(unittest.TestCase):
    test_dir = None
    test_json = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.mkdir(self.test_dir + os.sep + 'plugin_info')
        self.test_json = os.path.join(self.test_dir, 'plugin_info', 'info.json')
        with open(self.test_json, 'w') as file_content:
            file_content.write(INFO_JSON_CONTENT)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_with_key(self):
        replace_info_json(self.test_dir, 'data', 'useful')
        content = ''
        with open(self.test_json, 'r') as file_content:
            content = file_content.read()
        self.assertIn(INFO_JSON_CONTENT.replace('useless', 'useful'), content)

    def test_without_key(self):
        replace_info_json(self.test_dir, 'nothing', 'useful')
        content = ''
        with open(self.test_json, 'r') as file_content:
            content = file_content.read()
        self.assertIn(INFO_JSON_CONTENT, content)
