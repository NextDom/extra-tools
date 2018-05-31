# -*- coding: utf-8 -*-

import inspect
import os
import sys
import shutil
import tempfile
import unittest
from unittest import mock
from unittest.mock import patch

current_path = os.path.abspath(inspect.getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)
import tools


class TestToolsScript(unittest.TestCase):
    @patch('builtins.input', side_effect=['2',
                                          '0',
                                          '0'])
    def test_start_tools(self, side_effect):
        sys.argv = ['./tools.py']
        tools.start()
        self.assertTrue(os.path.exists('plugin-ExtraTemplate'))
        shutil.rmtree('plugin-ExtraTemplate')

