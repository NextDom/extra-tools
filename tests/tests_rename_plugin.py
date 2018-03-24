# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
import unittest

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
    test_file1 = None
    test_file2 = None
    test_file3 = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.plugin_dir = self.test_dir + os.sep + 'plugin-Test'
        os.mkdir(self.plugin_dir)
        self.folder1 = self.plugin_dir + os.sep + 'Folder'
        self.folder2 = self.plugin_dir + os.sep + 'TestFolder'
        self.test_file1 = self.folder1 + os.sep + 'Content'
        self.test_file2 = self.folder1 + os.sep + 'testContent'
        self.test_file3 = self.folder2 + os.sep + 'Testcontent'
        os.mkdir(self.folder1)
        os.mkdir(self.folder2)
        with open(self.test_file1, 'w') as dest_file:
            dest_file.write(TEST_FILE1_CONTENT)
        with open(self.test_file2, 'w') as dest_file:
            dest_file.write(TEST_FILE2_CONTENT)
        with open(self.test_file3, 'w') as dest_file:
            dest_file.write(TEST_FILE3_CONTENT)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_rename_folders_and_files_NewName(self):
        os.system(COMMAND % (self.plugin_dir, 'Test', 'NewName'))

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
        os.system(COMMAND % (self.plugin_dir, 'Test', 'newname'))

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
