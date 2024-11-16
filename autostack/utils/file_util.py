#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/11/14 17:58
@Author  : Rex
@File    : file_util.py.py
"""


class FileUtil:
    @staticmethod
    def read_template_file(template_file_path):
        """读取文件内容"""
        with open(template_file_path, 'r') as template_file:
            return template_file.read()

    @staticmethod
    def append_file(file_path, content):
        """追加内容到文件"""
        with open(file_path, 'a') as file:
            file.write(content)