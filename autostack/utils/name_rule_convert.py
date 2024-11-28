#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/11/14 17:59
@Author  : Rex
@File    : name_rule_convert.py.py
"""

import re


class NameRuleConverter:
    """
    命名规则转换 Tips：大小驼峰及下划线互转
    @descript 大驼峰: 首字母大写其余每一个逻辑断点（单词）都用大写字母标记,同帕斯卡命名法
    @descript 小驼峰: 首字母小写其余每一个逻辑断点（单词）都用大写字母标记
    @descript 下划线: 逻辑断点（单词）用的是下划线隔开
    """

    @staticmethod
    def to_underline(x):
        """转下划线命名"""
        return re.sub(r'(?<=[a-z])[A-Z]|(?<!^)[A-Z](?=[a-z])', r'_\g<0>', x).lower()

    @staticmethod
    def underline_to_upper_camel_case(x):
        """转大驼峰法命名"""
        s = re.sub(r'_([a-zA-Z])', lambda m: m.group(1).upper(), x.lower())
        return s[0].upper() + s[1:]

    @staticmethod
    def upper_camel_case_to_lower_camel_case(x):
        """转小驼峰法命名"""
        if not x:
            return x
        return x[0].lower() + x[1:]

    @staticmethod
    def underline_to_lower_camel_case(x):
        """转小驼峰法命名"""
        s = re.sub(r'_([a-zA-Z])', lambda m: m.group(1).upper(), x.lower())
        return s[0].lower() + s[1:]


# 示例用法
if __name__ == "__main__":
    example_str = "ScholarshipApplication"
    print(NameRuleConverter.to_underline(example_str))  # 输出: example_string
    print(NameRuleConverter.underline_to_upper_camel_case(example_str))  # 输出: ExampleString
    print(NameRuleConverter.upper_camel_case_to_lower_camel_case(example_str))  # 输出: exampleString
