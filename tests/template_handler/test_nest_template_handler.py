#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/11/14 18:15
@Author  : Rex
@File    : test_nest_template_handler.py.py
"""
import unittest
from autostack.template_handler import NestModuleTemplateHandler, NestProjectTemplateHandler
from autostack.common.const import ROOT


class TestNestTemplateHandler(unittest.TestCase):

    def test_create_module(self):
        entity_info = {
            "entity_name": "Student",
            "description": "学生类",
            "attributes": [{
                "name": "id",
                "type": "String",
                "required": True,
                "comment": "用户ID"
            }, {
                "name": "name",
                "type": "String",
                "required": True,
                "comment": "姓名"
            }, {
                "name": "age",
                "type": "Int",
                "required": True,
                "comment": "年龄"
            }, {
                "name": "gender",
                "type": "String",
                "required": True,
                "comment": "性别"
            }, {
                "name": "address",
                "type": "String",
                "required": False,
                "comment": "地址"
            }, {
                "name": "phone",
                "type": "String",
                "required": False,
                "comment": "电话号码"
            }]
        }
        project_dir = ROOT / "workspace / demo01"
        template_handler = NestModuleTemplateHandler(entity_info, project_dir=project_dir)
        template_handler.create_module()

    def test_nest_project_template_handler(self):
        project_info = {
            "project_name": "student_management_backend",
            "project_description": "学生管理系统",
            "author": "Rex",
            "modules": [{
                "entity_name": "Student",
                "description": "学生类",
                "attributes": [{
                    "name": "id",
                    "type": "String",
                    "required": True,
                    "comment": "用户ID"
                }, {
                    "name": "name",
                    "type": "String",
                    "required": True,
                    "comment": "姓名"
                }, {
                    "name": "age",
                    "type": "Int",
                    "required": True,
                    "comment": "年龄"
                }, {
                    "name": "gender",
                    "type": "String",
                    "required": True,
                    "comment": "性别"
                }, {
                    "name": "address",
                    "type": "String",
                    "required": False,
                    "comment": "地址"
                }, {
                    "name": "phone",
                    "type": "String",
                    "required": False,
                    "comment": "电话号码"
                }]
            }, {
                "entity_name": "Teacher",
                "description": "教师类",
                "attributes": [{
                    "name": "id",
                    "type": "String",
                    "required": True,
                    "comment": "教师ID"
                }, {
                    "name": "name",
                    "type": "String",
                    "required": True,
                    "comment": "姓名"
                }, {
                    "name": "age",
                    "type": "Int",
                    "required": True,
                    "comment": "年龄"
                }, {
                    "name": "gender",
                    "type": "String",
                    "required": True,
                    "comment": "性别"
                }, {
                    "name": "specialization",
                    "type": "String",
                    "required": True,
                    "comment": "专业领域"
                }, {
                    "name": "phone",
                    "type": "String",
                    "required": False,
                    "comment": "电话号码"
                }, {
                    "name": "email",
                    "type": "String",
                    "required": False,
                    "comment": "电子邮件"
                }]
            }]
        }
        nest_project_template_handler = NestProjectTemplateHandler(project_info)
        nest_project_template_handler.create_project()


if __name__ == "__main__":
    unittest.main()
