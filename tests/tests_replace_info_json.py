# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
import unittest

from scripts.libs.MethodData import MethodData
from scripts.libs.PHPFile import PHPFile


INFO_JSON_CONTENT = "{" + \
                    "\"id\": \"PluginId\"," + \
                    "\"name\": \"PluginName\"," + \
                    "\"data\": \"useless\"" + \
                    "}"

COMMAND = './scripts/replace_info_json.py %s > /dev/null 2>&1'

# noinspection PyUnusedLocal
class TestReplaceInfo(unittest.TestCase):
    test_dir = None
    base_menu = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.mkdir(self.test_dir + os.sep + 'plugin_info')
        self.test_json = os.path.join(self.test_dir, 'plugin_info', 'info.json')
        with open(self.test_json, 'w') as file_content:
            file_content.write(INFO_JSON_CONTENT)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_with_key(self):
        os.system(COMMAND % self.test_dir+' data useful')
        content = ''
        with open(self.test_json, 'r') as file_content:
            content = file_content.read()
        self.assertIn(INFO_JSON_CONTENT.replace('useless', 'useful'), content)

    def test_without_key(self):
        os.system(COMMAND % self.test_dir+' nothing useful')
        content = ''
        with open(self.test_json, 'r') as file_content:
            content = file_content.read()
        self.assertIn(INFO_JSON_CONTENT, content)