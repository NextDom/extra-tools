# -*- coding: utf-8 -*-

import unittest
import tempfile
import os
import shutil
from libs.InfoMenu import InfoMenu

INFO_JSON_CONTENT = "{" + \
      "\"id\": \"PluginId\"," + \
      "\"name\": \"PluginName\"," + \
      "\"data\": \"useless\"" + \
    "}"

class TestTools(unittest.TestCase):
    test_dir = None
    test_json = None
    info_menu = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.mkdir(self.test_dir+os.sep+'plugin_info')
        self.test_json = os.path.join(self.test_dir, 'plugin_info', 'info.json')
        with open(self.test_json, 'w') as file_content:
            file_content.write(INFO_JSON_CONTENT)
        self.info_menu = InfoMenu(self.test_dir, None)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_replace_info_key_found(self):
        self.info_menu.replace_info('data', 'useful')
        content = ''
        with open(self.test_json, 'r') as file_content:
            content = file_content.read()
        self.assertIn(INFO_JSON_CONTENT.replace('useless', 'useful'), content)

    def test_replace_info_key_not_found(self):
        self.info_menu.replace_info('nothing', 'useful')
        content = ''
        with open(self.test_json, 'r') as file_content:
            content = file_content.read()
        self.assertIn(INFO_JSON_CONTENT, content)
