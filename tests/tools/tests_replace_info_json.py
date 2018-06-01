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
from tools import InfoMenu


INFO_JSON_CONTENT = "{" + \
                    "\"id\": \"PluginId\"," + \
                    "\"name\": \"PluginName\"," + \
                    "\"data\": \"useless\"" + \
                    "}"


# noinspection PyUnusedLocal
class TestReplaceInfo(unittest.TestCase):
    test_dir = None
    test_json = None
    info_menu = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.mkdir(self.test_dir + os.sep + 'plugin_info')
        self.info_menu = InfoMenu(self.test_dir, 'Test')
        self.test_json = os.path.join(self.test_dir, 'plugin_info', 'info.json')
        with open(self.test_json, 'w') as file_content:
            file_content.write(INFO_JSON_CONTENT)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_with_key(self):
        self.info_menu.replace_info_json('data', 'useful')
        content = ''
        with open(self.test_json, 'r') as file_content:
            content = file_content.read()
        self.assertIn(INFO_JSON_CONTENT.replace('useless', 'useful'), content)

    def test_without_key(self):
        self.info_menu.replace_info_json('nothing', 'useful')
        content = ''
        with open(self.test_json, 'r') as file_content:
            content = file_content.read()
        self.assertIn(INFO_JSON_CONTENT, content)
