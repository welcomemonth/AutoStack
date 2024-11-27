#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
提示词工具类
@Time    : 2024/11/27 21:33
@Author  : Rex
@File    : prompt_util.py
"""
from string import Template
from autostack.common.const import PROMPT_ROOT


class PromptUtil:
    """
    提示词处理类
    """

    @staticmethod
    def prompt_handle(prompt_name, *args):
        """
        读取 prompt 文件内容
        :param prompt_name: 提示词文件名
        :param args: 提示词待替换待内容
        :return: 替换后的提示词
        """
        with open(PROMPT_ROOT / prompt_name, 'r', encoding='utf-8') as file:
            prompt_template = Template(file.read())

        prompt = prompt_template.substitute(*args)
        return prompt
