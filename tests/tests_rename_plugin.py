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
from tools import RootMenu

TEST_FILE1_CONTENT = 'Test\nSomething\nTEST\nSomewhere\ntest'
TEST_FILE2_CONTENT = 'A\nUseless\nFile'
TEST_FILE3_CONTENT = 'i test a file'
COMMAND = './scripts/rename_plugin.py %s %s %s > /dev/null 2>&1'


# noinspection PyUnusedLocal
class TestRenamePlugin(unittest.TestCase):
    test_dir = None
    plugin_dir = None
    folder1 = None
    folder2 = None
    root_menu = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.plugin_dir = self.test_dir + os.sep + 'plugin-Test'
        os.mkdir(self.plugin_dir)
        self.folder1 = self.plugin_dir + os.sep + 'Folder'
        self.folder2 = self.plugin_dir + os.sep + 'TestFolder'
        test_file1 = self.folder1 + os.sep + 'Content'
        test_file2 = self.folder1 + os.sep + 'testContent'
        test_file3 = self.folder2 + os.sep + 'Testcontent'
        self.root_menu = RootMenu(self.plugin_dir, 'Test')
        os.mkdir(self.folder1)
        os.mkdir(self.folder2)
        with open(test_file1, 'w') as dest_file:
            dest_file.write(TEST_FILE1_CONTENT)
        with open(test_file2, 'w') as dest_file:
            dest_file.write(TEST_FILE2_CONTENT)
        with open(test_file3, 'w') as dest_file:
            dest_file.write(TEST_FILE3_CONTENT)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_rename_folders_and_files_NewName(self):
        self.root_menu.rename_plugin('NewName')
        plugin_dir = self.test_dir + os.sep + 'plugin-NewName'
        folder1 = plugin_dir + os.sep + 'Folder'
        folder2 = plugin_dir + os.sep + 'NewNameFolder'
        test_file1 = folder1 + os.sep + 'Content'
        test_file2 = folder1 + os.sep + 'newnameContent'
        test_file3 = folder2 + os.sep + 'NewNamecontent'

        self.assertTrue(os.path.exists(plugin_dir))
        self.assertTrue(os.path.exists(test_file1))
        self.assertTrue(os.path.exists(test_file2))
        self.assertTrue(os.path.exists(test_file3))
        content = ''
        with open(test_file1, 'r') as file_content:
            content = file_content.read()
        self.assertIn('NewName\nSomething\nNEWNAME\nSomewhere\nnewName',
                      content)
        with open(test_file2, 'r') as file_content:
            content = file_content.read()
        self.assertIn(TEST_FILE2_CONTENT, content)
        with open(test_file3, 'r') as file_content:
            content = file_content.read()
        self.assertIn('i newName a file', content)

    def test_rename_folders_and_files_newname(self):
        self.root_menu.rename_plugin('newname')

        plugin_dir = self.test_dir + os.sep + 'plugin-newname'
        folder1 = plugin_dir + os.sep + 'Folder'
        folder2 = plugin_dir + os.sep + 'newnameFolder'
        test_file1 = folder1 + os.sep + 'Content'
        test_file2 = folder1 + os.sep + 'newnameContent'
        test_file3 = folder2 + os.sep + 'newnamecontent'

        self.assertTrue(os.path.exists(plugin_dir))
        self.assertTrue(os.path.exists(test_file1))
        self.assertTrue(os.path.exists(test_file2))
        self.assertTrue(os.path.exists(test_file3))
        with open(test_file1, 'r') as file_content:
            content = file_content.read()
        self.assertIn('newname\nSomething\nNEWNAME\nSomewhere\nnewname',
                      content)
        with open(test_file2, 'r') as file_content:
            content = file_content.read()
        self.assertIn(TEST_FILE2_CONTENT, content)
        with open(test_file3, 'r') as file_content:
            content = file_content.read()
        self.assertIn('i newname a file', content)
