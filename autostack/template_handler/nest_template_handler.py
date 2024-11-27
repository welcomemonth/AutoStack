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
    'entity': 'model' + os.sep + '${entity_lower_underline}.entity.ts.templ'
}
# 定义 Prisma 类型到 TypeScript 类型的映射关系
PRISMA_TO_TS = {
    "String": "string",  # 字符串类型
    "Int": "number",  # 整数类型
    "Float": "number",  # 浮点数类型
    "BigInt": "bigint",  # 大整数类型
    "Boolean": "boolean",  # 布尔类型
    "DateTime": "Date",  # 日期类型
    "Json": "any",  # JSON 类型映射为任意类型
    "Null": "null",  # 空值类型
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


class NestModuleTemplateHandler:
    """
    Nest模块模板处理器
    """

    def __init__(self, entity_info, project_dir):
        """
        初始化项目模块处理器
        :param entity_info: 模块实体信息
        :param project_dir: 项目路径
        """
        self.entity_info = entity_info
        self.project_dir = project_dir
        # 初始化模块目录
        module_name = NameRuleConverter.to_underline(self.entity_info['entity_name'])
        module_dir = self.project_dir / "src" / module_name
        self.module_dir = module_dir
        logger.info("module_dir", str(module_dir))
        # 检查文件夹是否存在，不存在则创建
        if not os.path.exists(self.module_dir):
            os.makedirs(self.module_dir)
            logger.info(f'项目模块创建完成，模块路径: {self.module_dir}')

    def create_module(self):
        """
        创建模块
        """
        # 将实体信息导入prisma
        self.generate_prisma_model(self.entity_info)
        entity_name = self.entity_info.get("entity_name")
        attributions = self.entity_info.get("attributes", [])
        info = {
            "entity_lower_camel": NameRuleConverter.to_lower_camel_case(entity_name),
            "entity_upper_camel": NameRuleConverter.to_upper_camel_case(entity_name),
            "entity_lower_underline": NameRuleConverter.to_underline(entity_name),
            "entity_attribute": generate_nest_attributions(attributions, validate=False),
            "create_entity_dto_attribute": generate_nest_attributions(attributions),
            "update_entity_dto_attribute": generate_nest_attributions(attributions)
        }
        # 创建文件
        simple_file_list = ['controller', 'controller_spec', 'service', 'service_spec', 'module']
        for file_type in MODULE_TEMPLATE_PATHS.keys():
            self.generate_file(file_type, info)

    def generate_file(self, file_type, info):
        """
        根据模板文件、实体信息生成文件
        :param file_type: 文件类型：controller、service、entity等
        :param info: 实体信息
        :return: 无返回值
        """
        # 获取模板文件相对路径
        template_path = MODULE_TEMPLATE_PATHS[file_type]
        # 更改模板文件名
        new_file_path_template = Template(template_path[:-6])
        new_file_path = new_file_path_template.substitute(info)
        # 更改模板文件内容
        template_absolute_path = BACKEND_TEMPLATE_DIR_PATH / "src" / "demo" / template_path
        try:
            template = FileUtil.get_template(template_absolute_path)
            content = template.substitute(info)
            new_file_absolute_path = self.module_dir / new_file_path
            FileUtil.write_file(new_file_absolute_path, content)
            logger.info(f"文件 {file_type} 生成完成")
        except FileNotFoundError as e:
            logger.error(f"模板文件未找到: {template_absolute_path}")
        except KeyError as e:
            logger.error(f"模板变量缺失: {e}")
        except Exception as e:
            logger.error(f"文件 {file_type} 生成失败: {e}")

    def generate_prisma_model(self, entity_info):
        """
        创建sql
        :param entity_info: 实体信息
        """
        entity_name = entity_info.get("entity_name")
        description = entity_info.get("description")
        prisma_model_text = f"\n// {description}\n"
        prisma_model_text += f"model {entity_name} {{\n"
        attributes = entity_info.get("attributes", [])
        if attributes is not None:
            for attribute in attributes:
                attribute_name = attribute.get("name")
                attribute_type = attribute.get("type")
                attribute_required = attribute.get("required")
                attribute_comment = attribute.get("comment")
                attribute_text = f"    {attribute_name} {attribute_type}"
                # 若属性非必填，则添加问号
                if not attribute_required:
                    attribute_text += "?"
                # 若属性为id，则添加默认值
                if attribute_name == "id":
                    attribute_text += " @id @default(cuid())"
                # 添加注释
                attribute_text += f" //{attribute_comment}\n"
                prisma_model_text += attribute_text
        prisma_model_text += "}"
        # 将以上内容
        prisma_file_path = self.project_dir / PRISMA_FILE_TEMPLATE
        FileUtil.append_file(prisma_file_path, prisma_model_text)


class NestProjectTemplateHandler:
    def __init__(self, project_info, project_dir=None):
        self.project_info = project_info
        self.project_dir = project_dir if project_dir else WORKSPACE_ROOT_PATH / project_info.get("project_name")
        # 若项目已存在则在文件后加"_copy"
        while os.path.exists(self.project_dir):
            project_file_name = self.project_dir.name + '_copy'
            print(project_file_name)
            self.project_dir = self.project_dir.parent / project_file_name

    def create_project(self):
        project_name = self.project_info["project_name"]
        """
        创建项目
        """
        # 若文件目录不存在，则创建目录
        if not os.path.exists(self.project_dir):
            os.makedirs(self.project_dir)
            logger.info(f"项目目录创建完成，项目目录：{self.project_dir} ")

        # 文件复制
        FileUtil.copy_all_files(BACKEND_TEMPLATE_DIR_PATH, self.project_dir)

        # 获取项目模块
        module_list = self.project_info.get("modules")

        # 逐一创建项目模块
        for module in module_list:
            module_handler = NestModuleTemplateHandler(module, self.project_dir)
            module_handler.create_module()

        self.generate_package_file()
        self.add_modules_config_to_project(module_list)

        # 文件删除，删除模板文件
        FileUtil.remove_file(self.project_dir / ".env")
        FileUtil.remove_dir(self.project_dir / "src/demo")
        FileUtil.remove_file(self.project_dir / "package.json.templ")
        FileUtil.remove_file(self.project_dir / "src/app.module.ts.templ")

        # 生成.env文件
        default_env = {
            "POSTGRES_USER": "postgres",
            "POSTGRES_PASSWORD": "postgres",
            "POSTGRES_DB": project_name,
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
            "DB_SCHEMA": project_name,
            "DATABASE_URL": "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DB_HOST}:${DB_PORT}/${POSTGRES_DB}?schema=${DB_SCHEMA}&sslmode=prefer"
        }
        FileUtil.generate_env(default_env, self.project_dir / ".env")

    def generate_package_file(self):
        """
        生成package.json文件
        """
        package_info = {
            "project_name": self.project_info.get("project_name"),
            "project_description": self.project_info.get('project_description')
        }
        package_json_template_path = BACKEND_TEMPLATE_DIR_PATH / PROJECT_TEMPLATE_PATHS['package']
        package_path = PROJECT_TEMPLATE_PATHS['package'][:-6]
        # 更改模板文件内容
        try:
            template = FileUtil.get_template(package_json_template_path)
            content = template.substitute(package_info)
            absolute_package_path = self.project_dir / package_path
            FileUtil.write_file(absolute_package_path, content)
            logger.info(f"文件 package.json 生成完成")
        except FileNotFoundError as e:
            logger.error(f"模板文件未找到: {package_json_template_path}")
        except KeyError as e:
            logger.error(f"模板变量缺失: {e}")
        except Exception as e:
            logger.error(f"文件 package.json 生成失败: {e}")

    def add_modules_config_to_project(self, module_list):
        """
        在项目中添加模块信息
        :param module_list: 模块列表
        """
        # 构造modules_info
        import_module_list = []
        module_name_list = []
        for module in module_list:
            module_name = module.get("entity_name")
            module_name_underline = NameRuleConverter.to_underline(module_name)
            module_name_upper = NameRuleConverter.to_upper_camel_case(module_name)
            import_module_content = f"import {{ {module_name_upper}Module }} from './{module_name_underline}/{module_name_underline}.module';"
            import_module_list.append(import_module_content)
            module_name_list.append(f"{module_name}Module")
        modules_info = {
            "import_module_list": "\n".join(import_module_list),
            "module_list": ",\n    ".join(module_name_list)
        }
        module_template_path = BACKEND_TEMPLATE_DIR_PATH / PROJECT_TEMPLATE_PATHS["app.module"]
        # 更改模板文件内容
        try:
            template = FileUtil.get_template(module_template_path)
            content = template.substitute(modules_info)
            new_file_absolute_path = self.project_dir / PROJECT_TEMPLATE_PATHS["app.module"][:-6]
            FileUtil.write_file(new_file_absolute_path, content)
            logger.info(f"文件 app.module.ts 生成完成")
        except FileNotFoundError as e:
            logger.error(f"模板文件未找到: {module_template_path}")
        except KeyError as e:
            logger.error(f"模板变量缺失: {e}")
        except Exception as e:
            logger.error(f"文件 app.module.ts 生成失败: {e}")