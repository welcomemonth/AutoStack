#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/11/14 17:57
@Author  : Rex
@File    : base_template_handler.py
"""
from string import Template
import os


class BaseTemplateHandler:
    def __init__(self, entity_info, project_dir):
        """
        初始化模板
        :param entity_info: 实体信息

        :param project_dir: 项目文件夹
        """
        self.entity_info = entity_info
        self.project_dir = project_dir

    def get_template(self, template_file_path):
        """
        获取模板文件
        :param template_file_path: 模板文件地址
        :return: 模板文件文本
        """
        template_str = None
        with open(template_file_path, 'r') as template_file:
            template_str = template_file.read()

        return Template(template_str)

    def write_file(self, file_path, content):
        """
        写入文件
        :param file_path: 文件路径
        :param content: 文件内容
        :return:
        """
        # 获取文件路径中的目录部分
        directory = os.path.dirname(file_path)
        # 如果目录不存在，则创建它
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(file_path, 'w') as file:
            file.write(content)
