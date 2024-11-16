#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/11/14 18:00
@Author  : Rex
@File    : nest_template_handler.py.py
"""

from autostack.template_handler import BaseTemplateHandler
from string import Template
from autostack.utils import NameRuleConverter, FileUtil
from autostack.const import ROOT
import os

print("abspath", os.path.abspath(__file__))
BACKEND_TEMPLATE_DIR_PATH = ROOT / 'templates/backend/'

TEMPLATE_PATHS = {
    'controller': '${entity_lower_underline}.controller.ts.templ',
    'controller_spec': '${entity_lower_underline}.controller.spec.ts.templ',
    'service': '${entity_lower_underline}.service.ts.templ',
    'service_spec': '${entity_lower_underline}.service.spec.ts.templ',
    'module': '${entity_lower_underline}.module.ts.templ',
    'create_dto': 'dto' + os.sep + 'create-${entity_lower_underline}.dto.ts.templ',
    'update_dto': 'dto' + os.sep + 'update-${entity_lower_underline}.dto.ts.templ',
    'entity': 'model' + os.sep + '${entity_lower_underline}.entity.ts.templ'
}
PRISMA_FILE_TEMPLATE = "prisma/schema.prisma"


class NestModuleTemplateHandle(BaseTemplateHandler):
    def __init__(self, entity_info, project_dir):
        super(NestModuleTemplateHandle, self).__init__(entity_info, project_dir)
        # 初始化模块目录
        module_name = NameRuleConverter.to_underline(self.entity_info['entity_name'])
        module_dir = os.path.join(self.project_dir, "src", module_name)
        print("module_dir", module_dir)
        self.project_dir = project_dir
        # 检查文件夹是否存在，不存在则创建
        self.module_dir = module_dir
        if not os.path.exists(self.module_dir):
            os.makedirs(self.module_dir)
            print(f'Created directory: {self.module_dir}')

    def create_module(self):
        # 将实体信息导入prisma
        self.generate_prisma_model(self.entity_info)
        info = {
            "entity_lower_camel": NameRuleConverter.to_lower_camel_case(self.entity_info.get("entity_name")),
            "entity_upper_camel": NameRuleConverter.to_upper_camel_case(self.entity_info.get("entity_name")),
            "entity_lower_underline": NameRuleConverter.to_underline(self.entity_info.get("entity_name")),
            "entity_attribute": "",  # TODO 生成entity对应的属性信息
            "create_entity_dto_attribute": "",  # TODO 生成create-dto对应的属性信息
            "update_entity_dto_attribute": ""  # TODO 生成update-dto对应的属性信息
        }
        # 创建文件
        simple_file_list = ['controller', 'controller_spec', 'service', 'service_spec', 'module']
        for file_type in TEMPLATE_PATHS.keys():
            try:
                self.create_file(file_type, info)
                print(f"write {file_type} is finished")
            except Exception as e:
                print(f"write error in {file_type}: ", e)

    def create_file(self, file_type, info):
        # 获取模板文件相对路径
        template_path = TEMPLATE_PATHS[file_type]
        # 更改模板文件名
        new_file_path_template = Template(template_path[:-6])
        new_file_path = new_file_path_template.substitute(info)
        # 更改模板文件内容
        template_absolute_path = os.path.join(BACKEND_TEMPLATE_DIR_PATH, "src", "demo", template_path)
        template = self.get_template(template_absolute_path)
        content = template.substitute(info)
        new_file_absolute_path = os.path.join(self.module_dir, new_file_path)
        self.write_file(new_file_absolute_path, content)

    def generate_prisma_model(self, entity_info):
        # 添加注释
        entity_name = entity_info.get("entity_name")
        description = entity_info.get("description")
        prisma_model_text = "\n// " + description + "\n"
        prisma_model_text += "model " + entity_info.get('entity_name') + " {\n"
        attributes = entity_info.get("attributes")
        if attributes is not None:
            for attribute in attributes:
                attribute_name = attribute.get("name")
                attribute_type = attribute.get("type")
                attribute_required = attribute.get("required")
                attribute_comment = attribute.get("comment")
                attribute_text = "    "
                attribute_text += attribute_name + " " + attribute_type
                # 若属性非必填，则添加问号
                if not attribute_required:
                    attribute_text += "?"
                # 若属性为id，则添加默认值
                if attribute_name == "id":
                    attribute_text += " @id @default(cuid())"
                # 添加注释
                attribute_text += " //" + attribute_comment
                attribute_text += "\n"
                prisma_model_text += attribute_text
        prisma_model_text += "}"
        # 将以上内容
        prisma_file_path = os.path.join(self.project_dir, PRISMA_FILE_TEMPLATE)
        FileUtil.append_file(prisma_file_path, prisma_model_text)
        return prisma_model_text
