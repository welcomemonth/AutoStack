#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/11/14 18:15
@Author  : Rex
@File    : test_nest_template_handler.py.py
"""
import unittest
from autostack.template_handler import NestModuleTemplateHandle
from autostack.const import ROOT


class TestNestTemplateHandler(unittest.TestCase):

    def test_create_module(self):
        entity_info = {
            "entity_name": "Student",
            "attribution": [{
                "name": "id",
                "type": "number",
                "required": True,
                "comment": "用户ID"
            }, {
                "name": "name",
                "type": "string",
                "required": True,
                "comment": "姓名"
            }, {
                "name": "age",
                "type": "number",
                "required": True,
                "comment": "年龄"
            }, {
                "name": "gender",
                "type": "string",
                "required": True,
                "comment": "性别"
            }, {
                "name": "address",
                "type": "string",
                "required": True,
                "comment": "地址"
            }, {
                "name": "phone",
                "type": "string",
                "required": True,
                "comment": "电话号码"
            }]
        }
        project_dir = ROOT / "autostack/workspace/demo01"
        template_handler = NestModuleTemplateHandle(entity_info, project_dir=project_dir)
        template_handler.create_module()


if __name__ == "__main__":
    unittest.main()
