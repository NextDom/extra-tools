# -*- coding: utf-8 -*-

import os
import shutil
import unittest

from unittest.mock import call
from unittest.mock import patch

from scripts.libs.RootMenu import RootMenu

TEST_FILE1_CONTENT = 'Test\nSomething\nTEST\nSomewhere\ntest'
TEST_FILE2_CONTENT = 'A\nUseless\nFile'
TEST_FILE3_CONTENT = 'i test a file'


class TestRootMenu(unittest.TestCase):
    test_dir = None
    folder1 = None
    folder2 = None
    test_file1 = None
    test_file2 = None
    test_file3 = None
    root_menu = None

    def setUp(self):
        self.test_dir = 'temp'
        os.mkdir('temp')  # tempfile.mkdtemp()
        self.folder1 = self.test_dir + os.sep + 'Folder'
        self.folder2 = self.test_dir + os.sep + 'TestFolder'
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
        self.root_menu = RootMenu('', '')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch('os.rename')
    def test_rename_plugin_files_NewName(self, mocked_rename):
        mocked_rename_calls = [call(self.folder1 + os.sep + 'testContent',
                                    self.folder1 + os.sep + 'newnameContent'),
                               call(self.folder2 + os.sep + 'TestContent',
                                    self.folder2 + os.sep + 'NewNameContent')]

        self.root_menu.rename_item(self.folder1 + os.sep, 'Content',
                                   'Test', 'NewName')
        self.root_menu.rename_item(self.folder1 + os.sep, 'testContent',
                                   'Test', 'NewName')
        self.root_menu.rename_item(self.folder2 + os.sep, 'TestContent',
                                   'Test', 'NewName')
        mocked_rename.assert_has_calls(mocked_rename_calls)

    @patch('os.rename')
    def test_rename_plugin_files_newname(self, mocked_rename):
        mocked_rename_calls = [call(self.folder1 + os.sep + 'testContent',
                                    self.folder1 + os.sep + 'newnameContent'),
                               call(self.folder2 + os.sep + 'TestContent',
                                    self.folder2 + os.sep + 'newnameContent')]
        self.root_menu.rename_item(self.folder1 + os.sep, 'Content',
                                   'Test', 'newname')
        self.root_menu.rename_item(self.folder1 + os.sep, 'testContent',
                                   'Test', 'newname')
        self.root_menu.rename_item(self.folder2 + os.sep, 'TestContent',
                                   'Test', 'newname')
        mocked_rename.assert_has_calls(mocked_rename_calls)

    def test_rename_plugin_folders_NewName(self):
        self.root_menu.rename_item(self.test_dir + os.sep, 'Folder',
                                   'Test', 'NewName')
        self.root_menu.rename_item(self.test_dir + os.sep, 'TestFolder',
                                   'Test', 'NewName')
        self.assertTrue(os.path.exists(self.test_dir + os.sep + 'Folder'))
        self.assertTrue(
            os.path.exists(self.test_dir + os.sep + 'NewNameFolder'))

    def test_replace_in_file_NewName(self):
        self.root_menu.replace_in_file(self.test_file1, 'Test', 'NewName')
        content = ''
        with open(self.test_file1, 'r') as file_content:
            content = file_content.read()
        self.assertIn('NewName\nSomething\nNEWNAME\nSomewhere\nnewname',
                      content)
        self.root_menu.replace_in_file(self.test_file2, 'Test', 'NewName')
        with open(self.test_file2, 'r') as file_content:
            content = file_content.read()
        self.assertIn(TEST_FILE2_CONTENT,
                      content)
        self.root_menu.replace_in_file(self.test_file3, 'Test', 'NewName')
        with open(self.test_file3, 'r') as file_content:
            content = file_content.read()
        self.assertIn('i newname a file',
                      content)

    def test_replace_in_file_newname(self):
        self.root_menu.replace_in_file(self.test_file1, 'Test', 'newname')
        content = ''
        with open(self.test_file1, 'r') as file_content:
            content = file_content.read()
        self.assertIn('newname\nSomething\nNEWNAME\nSomewhere\nnewname',
                      content)
        self.root_menu.replace_in_file(self.test_file2, 'Test', 'newname')
        with open(self.test_file2, 'r') as file_content:
            content = file_content.read()
        self.assertIn(TEST_FILE2_CONTENT,
                      content)
        self.root_menu.replace_in_file(self.test_file3, 'Test', 'newname')
        with open(self.test_file3, 'r') as file_content:
            content = file_content.read()
        self.assertIn('i newname a file',
                      content)

    def test_rename_plugin_folders(self):
        self.root_menu.rename_plugin(self.test_dir, 'Test', 'NewName')
        self.assertTrue(os.path.exists(self.test_dir + os.sep + 'Folder'))
        self.assertTrue(
            os.path.exists(self.test_dir + os.sep + 'NewNameFolder'))
        print('TEST 1')

    def test_rename_plugin_file_content(self):
        self.root_menu.rename_plugin(self.test_dir, 'Test', 'NewName')
        content = ''
        with open(self.test_file1, 'r') as file_content:
            content = file_content.read()
        self.assertIn('NewName\nSomething\nNEWNAME\nSomewhere\nnewname',
                      content)

    def test_rename_plugin_file_content_without_change(self):
        self.root_menu.rename_plugin(self.test_dir, 'Test', 'NewName')
        content = ''

        test_file2 = self.folder1 + os.sep + 'newnameContent'
        with open(test_file2, 'r') as file_content:
            content = file_content.read()
        self.assertIn(TEST_FILE2_CONTENT,
                      content)

    def test_rename_plugin_file_content_with_name_and_content(self):
        self.root_menu.rename_plugin(self.test_dir, 'Test', 'NewName')
        content = ''

        test_file3 = os.path.join(self.test_dir, 'NewNameFolder',
                                  'NewNamecontent')
        with open(test_file3, 'r') as file_content:
            content = file_content.read()
        self.assertIn('i newname a file',
                      content)
