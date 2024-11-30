#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Nest模板处理器
@Time    : 2024/11/14 18:00
@Author  : Rex
@File    : nest_template_handler.py.py
"""

from string import Template
from autostack.utils import NameRuleConverter, FileUtil
from autostack.common.const import ROOT
from autostack.common.logs import logger
import os

BACKEND_TEMPLATE_DIR_PATH = ROOT / 'templates/backend/'
WORKSPACE_ROOT_PATH = ROOT / 'workspace'
PROJECT_TEMPLATE_PATHS = {
    'package': 'package.json.templ',
    "app.module": 'src/app.module.ts.templ'
}
MODULE_TEMPLATE_PATHS = {
    'controller': '${entity_lower_underline}.controller.ts.templ',
    'controller_spec': '${entity_lower_underline}.controller.spec.ts.templ',
    'service': '${entity_lower_underline}.service.ts.templ',
    'service_spec': '${entity_lower_underline}.service.spec.ts.templ',
    'module': '${entity_lower_underline}.module.ts.templ',
    'create_dto': 'dto' + os.sep + 'create-${entity_lower_underline}.dto.ts.templ',
    'update_dto': 'dto' + os.sep + 'update-${entity_lower_underline}.dto.ts.templ',
}
# 定义 Prisma 类型到 TypeScript 类型的映射关系
PRISMA_TO_TS = {
  "String": 'string',            # Prisma String -> TypeScript string
  "Int": 'number',               # Prisma Int -> TypeScript number
  "BigInt": 'number',            # Prisma BigInt -> TypeScript string (or BigInt, depending on usage)
  "Decimal": 'number',           # Prisma Decimal -> TypeScript string (use decimal.js for precision)
  "Float": 'number',             # Prisma Float -> TypeScript number
  "Boolean": 'boolean',          # Prisma Boolean -> TypeScript boolean
  "DateTime": 'Date | string',   # Prisma DateTime -> TypeScript Date or string
  "Json": 'any',                 # Prisma Json -> TypeScript any (or more specific types based on usage)
  "Enum": 'enum',                # Prisma Enum -> TypeScript enum
  "Bytes": 'Buffer',             # Prisma Bytes -> TypeScript Buffer (for binary data)
  # "Relation": 'Model',           # Prisma Relation -> TypeScript corresponding DTO or Model
  "StringArray": 'string[]',     # Prisma String[] -> TypeScript string[]
  "IntArray": 'number[]',        # Prisma Int[] -> TypeScript number[]
  "FloatArray": 'number[]',      # Prisma Float[] -> TypeScript number[]
  "DecimalArray": 'number[]',    # Prisma Decimal[] -> TypeScript string[] (use decimal.js for precision)
  "BooleanArray": 'boolean[]',   # Prisma Boolean[] -> TypeScript boolean[]
  "DateTimeArray": 'Date[]',     # Prisma DateTime[] -> TypeScript Date[]
  "JsonArray": 'any[]',          # Prisma Json[] -> TypeScript any[]
}

PRISMA_FILE_TEMPLATE = "prisma/schema.prisma"


def generate_nest_attributions(attributions, validate=True):
    """
    根据给定的prisma属性生成nest属性
    :param attributions: 属性列表
    :param validate 是否需要校验
    :return:
    """
    if attributions is None:
        return ""
    attribution_context = ""
    for attribute in attributions:
        attribute_name = attribute.get("name")
        attribute_type = attribute.get("type")
        attribute_required = attribute.get("required")
        attribute_comment = attribute.get("comment")
        # 如果attribute_type不在PRISMA_TO_TS中，则continue
        if attribute_type not in PRISMA_TO_TS.keys():
            # TODO 复杂类型处理
            continue
        ts_attribute_type = PRISMA_TO_TS.get(attribute_type)
        attribution_context += f"\n    /**\n     * {attribute_comment}\n     */\n"
        if validate is True:
            attribution_context += f"    @ApiProperty()\n"
            if ts_attribute_type == "string":
                attribution_context += f"    @IsString()\n"
            elif ts_attribute_type == "number":
                attribution_context += f"    @IsNumber()\n"
            elif ts_attribute_type == "bigint":
                attribution_context += f"    @IsNumber()\n"
            elif ts_attribute_type == "boolean":
                attribution_context += f"    @IsBoolean()\n"
            elif ts_attribute_type == "Date":
                attribution_context += f"    @IsDate()\n"
            if attribution_context is not True:
                attribution_context += f"    @IsOptional()\n"
        attribution_context += f"    {attribute_name}"
        if attribute_required is not True:
            attribution_context += "?"
        attribution_context += f": {ts_attribute_type}"
    return attribution_context


def generate_file_by_template(target_path, template_path, info):
    """
    根据模板文件、实体信息生成文件
    :param target_path: 目标文件地址
    :param template_path: 模板文件地址
    :param info: 实体信息
    :return: 无返回值
    """

    # 更改模板文件内容
    try:
        template = FileUtil.get_template(template_path)
        content = template.substitute(info)

        FileUtil.write_file(target_path, content)
        logger.info(f"文件 {target_path} 生成完成")
    except FileNotFoundError:
        logger.error(f"模板文件未找到: {template_path}")
    except KeyError as e:
        logger.error(f"模板变量缺失: {e}")
    except Exception as e:
        logger.error(f"文件 {target_path} 生成失败: {e}")


def create_module(project_path, module_info):
    """
    创建模块
    """
    # 将实体信息导入prisma
    entity_name = module_info.get("name")
    attributions = module_info.get("attributes", [])
    info = {
        "entity_lower_camel": NameRuleConverter.upper_camel_case_to_lower_camel_case(entity_name),
        "entity_upper_camel": entity_name,
        "entity_lower_underline": NameRuleConverter.to_underline(entity_name),
        "entity_attribute": generate_nest_attributions(attributions, validate=False),
        "create_entity_dto_attribute": generate_nest_attributions(attributions),
        "update_entity_dto_attribute": generate_nest_attributions(attributions)
    }
    module_dir = project_path / "src" / NameRuleConverter.to_underline(entity_name)
    # 创建文件
    for file_type in MODULE_TEMPLATE_PATHS.keys():
        # 获取模板文件相对路径
        template_path = MODULE_TEMPLATE_PATHS[file_type]
        # 更改模板文件名
        new_file_path_template = Template(template_path[:-6])
        new_file_path = new_file_path_template.substitute(info)
        new_file_absolute_path = module_dir / new_file_path
        template_absolute_path = BACKEND_TEMPLATE_DIR_PATH / "src" / "demo" / template_path
        generate_file_by_template(new_file_absolute_path, template_absolute_path, info)
    # 添加模块至app.module.ts
    add_module_to_app(project_path, entity_name)


def create_project(project_path, project_info):
    project_name = project_info["project_name"]
    """
    创建项目
    """
    # 若文件目录不存在，则创建目录
    if not os.path.exists(project_path):
        os.makedirs(project_path)
        logger.info(f"项目目录创建完成，项目目录：{project_path} ")

    # 复制项目
    FileUtil.copy_all_files(BACKEND_TEMPLATE_DIR_PATH, project_path)

    # 生成package.json
    package_info = {
        "project_name": project_info.get("project_name"),
        "project_description": project_info.get('project_description')
    }
    generate_file_by_template(
        project_path / "package.json",
        BACKEND_TEMPLATE_DIR_PATH / "package.json.templ",
        package_info
    )

    # 文件删除，删除模板文件
    FileUtil.remove_file(project_path / ".env")
    FileUtil.remove_dir(project_path / "src/demo")
    FileUtil.remove_file(project_path / "package.json.templ")
    FileUtil.remove_file(project_path / "src/app.module.ts.templ")

    # 生成.env文件
    default_env = {
        "POSTGRES_USER": "postgres",
        "POSTGRES_PASSWORD": "postgres",
        "POSTGRES_DB": project_name,
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_SCHEMA": project_name,
        "DATABASE_URL": "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DB_HOST}:${DB_PORT}/${"
                        "POSTGRES_DB}?schema=${DB_SCHEMA}&sslmode=prefer "
    }
    # 生成.env文件, 数据库配置。⚠️ 不能使用模板替换，里面包含${}
    FileUtil.generate_env(default_env, project_path / ".env")


def add_module_to_app(project_path, module_name):
    """
    将模块信息添加至app.module.ts

    :param project_path: 项目地址
    :param module_name: 模块名称(大驼峰)
    """
    app_module_code_path = project_path / 'src' / 'app.module.ts'
    app_module_code = FileUtil.read_file(app_module_code_path)
    # 提取每行信息
    lines = app_module_code.split("\n")

    # 找到导入部分并添加新的模块导入
    module_name_underline = NameRuleConverter.to_underline(module_name)
    import_line = f"import {{ {module_name}Module }} from './{module_name_underline}/{module_name_underline}.module';"
    for i, line in enumerate(lines):
        if line.strip() == "import { Module } from '@nestjs/common';":
            lines.insert(i, import_line)
            break

    # 找到导入数组并添加新模块
    for i, line in enumerate(lines):
        if "imports: [" in line:
            indent = line.split("imports: [")[0]
            lines.insert(i + 1, f"{indent}  {module_name}Module,")
            break

    # 用换行符做拼接
    updated_code = "\n".join(lines)
    FileUtil.write_file(app_module_code_path, updated_code)
    return updated_code
