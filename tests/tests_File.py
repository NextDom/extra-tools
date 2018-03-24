# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from scripts.libs.File import File

TEST_FILE1_CONTENT = 'Test\nSomething\nTEST\nSomewhere\ntest'
TEST_FILE2_CONTENT = 'A\nUseless\nFile'
TEST_FILE3_CONTENT = 'i test a file'


# noinspection PyUnusedLocal
class TestFile(unittest.TestCase):
    test_dir = None
    base_menu = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file1 = self.test_dir + os.sep + 'file1'
        self.test_file2 = self.test_dir + os.sep + 'file2'
        self.test_file3 = self.test_dir + os.sep + 'file3'
        with open(self.test_file1, 'w') as dest_file:
            dest_file.write(TEST_FILE1_CONTENT)
        with open(self.test_file2, 'w') as dest_file:
            dest_file.write(TEST_FILE2_CONTENT)
        with open(self.test_file3, 'w') as dest_file:
            dest_file.write(TEST_FILE3_CONTENT)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_is_content_in_file_without_file(self):
        file_to_test = self.test_dir + os.sep + 'FileNotFound'
        result = File.is_content_in_file(file_to_test, 'test string')
        self.assertFalse(result)

    def test_is_content_in_file_without_the_content(self):
        file_to_test = self.test_dir + os.sep + 'WithoutTheContent'
        with open(file_to_test, 'w') as dest:
            dest.write('Nothing in this file')
        result = File.is_content_in_file(file_to_test, 'content')
        self.assertFalse(result)

    def test_is_content_in_file_without_content(self):
        file_to_test = self.test_dir + os.sep + 'WithContent'
        with open(file_to_test, 'w') as dest:
            dest.write('Small content in a file')
        result = File.is_content_in_file(file_to_test, 'content')
        self.assertTrue(result)

    def test_sed_replace_with_match(self):
        sed_file_path = self.test_dir + os.sep + 'sed_test'
        with open(sed_file_path, 'w') as sed_file:
            sed_file.write('AABBBCCCC')
        File.sed_replace('BBB', 'DDDDD', sed_file_path)
        file_content = ''
        with open(sed_file_path, 'r') as sed_file:
            file_content = sed_file.read()
        self.assertIn('AADDDDDCCCC', file_content)

    def test_sed_replace_without_match(self):
        sed_file_path = self.test_dir + os.sep + 'sed_test'
        with open(sed_file_path, 'w') as sed_file:
            sed_file.write('AABBBCCCC')
        File.sed_replace('ZZZ', 'DDDDD', sed_file_path)
        file_content = ''
        with open(sed_file_path, 'r') as sed_file:
            file_content = sed_file.read()
        self.assertIn('AABBBCCCC', file_content)

    def test_replace_in_file_NewName(self):
        File.replace_in_file(self.test_file1, 'Test', 'NewName')
        content = ''
        with open(self.test_file1, 'r') as file_content:
            content = file_content.read()
        self.assertIn('NewName\nSomething\nNEWNAME\nSomewhere\nnewName',
                      content)
        File.replace_in_file(self.test_file2, 'Test', 'NewName')
        with open(self.test_file2, 'r') as file_content:
            content = file_content.read()
        self.assertIn(TEST_FILE2_CONTENT,
                      content)
        File.replace_in_file(self.test_file3, 'Test', 'NewName')
        with open(self.test_file3, 'r') as file_content:
            content = file_content.read()
        self.assertIn('i newName a file',
                      content)

    def test_replace_in_file_newname(self):
        File.replace_in_file(self.test_file1, 'Test', 'newname')
        content = ''
        with open(self.test_file1, 'r') as file_content:
            content = file_content.read()
        self.assertIn('newname\nSomething\nNEWNAME\nSomewhere\nnewname',
                      content)
        File.replace_in_file(self.test_file2, 'Test', 'newname')
        with open(self.test_file2, 'r') as file_content:
            content = file_content.read()
        self.assertIn(TEST_FILE2_CONTENT,
                      content)
        File.replace_in_file(self.test_file3, 'Test', 'newname')
        with open(self.test_file3, 'r') as file_content:
            content = file_content.read()
        self.assertIn('i newname a file',
                      content)

    def test_write_json_file(self):
        data = {
            '\\/coucou\\/': 'Plouf',
            'bla': 'è&ça °'
        }
        to_compare = '{\n    "\\/coucou\\/": "Plouf",\n    "bla": "è&ça °"\n}\n'
        test_file_path = self.test_dir + os.sep + 'json_test'
        result = File.write_json_file(test_file_path, data)
        self.assertTrue(result)
        content = ''
        with open(test_file_path, 'r') as test_file:
            content = test_file.read()
        self.assertEqual(content, to_compare)

