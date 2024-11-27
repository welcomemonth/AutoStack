#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/11/27 21:17
@Author  : Rex
@File    : test_file_tree.py.py
"""
import unittest
from autostack.utils import FileTreeUtil
from autostack.common.const import ROOT


class TestFileTreeUtil(unittest.TestCase):

    def test_tree(self):
        tree = FileTreeUtil.tree(ROOT)
        print(tree)