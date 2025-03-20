import json
import uuid
from typing import List, Optional, Union, Any
from pathlib import Path
from pydantic import BaseModel
from autostack.utils import MarkdownUtil, FileTreeUtil, FileUtil, PromptUtil
from autostack.common.const import DEFAULT_WORKSPACE_ROOT
from autostack.llm import LLM
from autostack.common.logs import logger
from autostack.template_handler import NestTemplateHandler
from .module import Module, Entity


# @singleton
class Project(BaseModel):
    project_name: str
    project_description: str
    project_name_by_snake: str
    author: Optional[str] = "autostack"
    requirement_path: Optional[Path] = None
    database_design_path: Optional[Path] = None
    modules: Optional[List[Module]] = []  # 模块列表，默认为空
    root: Optional[Path] = None
    project_home: Optional[Path] = None
    resources: Optional[Path] = None
    docs: Optional[Path] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.root = DEFAULT_WORKSPACE_ROOT / self.project_name_by_snake
        self.project_home = self.root / self.project_name_by_snake
        self.resources = self.root / 'resources'  # 都是处理后的json格式
        self.docs = self.root / 'docs'  # 原生的markdown格式

        FileUtil.create_dir(self.root)
        FileUtil.create_dir(self.docs)
        FileUtil.create_dir(self.resources)

    @property
    def requirement_doc(self):
        # 读取需求文件
        return FileUtil.read_file(self.requirement_path)

    @property
    def database_design_doc(self):
        """读取数据库设计文档并返回内容"""
        return FileUtil.read_file(self.database_design_path)

    @property
    def entities(self):
        """返回数据库设计文档中的实体列表"""
        entity_str_list = FileUtil.read_file(self.resources / 'entity' / "entity_list.json")
        return json.loads(entity_str_list)

    @property
    def prisma_schema(self):
        return FileUtil.read_file(self.project_home / "prisma" / "schema.prisma")

    def add_module(self, module: Module):
        """添加模块到项目"""
        NestTemplateHandler.create_module(self.project_home, module.serialize)
        module.created = True
        self.modules.append(module)

    def update_module_status(self, module_name: str, status: str):
        """更新指定模块的状态"""
        for module in self.modules:
            if module.name == module_name:
                module.status = status
                logger.info(f"Module '{module_name}' status updated to '{status}'.")
                break
        else:
            logger.error(f"Module '{module_name}' not found in project.")

    @property
    def serialize(self):
        # exclude={"name"}采用这个可以去除一些属性
        return self.model_dump(exclude={"project_home", "resources", "docs", "requirement_path"})

    def save(self):
        # 将项目序列化的数据保存到文件，每次都覆盖原文件
        with open(self.root / "project.json", "w", encoding='utf-8') as f:
            f.write(self.model_dump_json())

    @staticmethod
    def load(project_path: Path):
        """从文件中加载项目信息"""
        with open(project_path, "r", encoding='utf-8') as f:
            project_data = f.read()
        return Project.model_validate_json(project_data)

    @property
    def file_tree(self, file_path: Union[str, Path] = None):
        """返回项目的文件树"""
        if file_path is None:
            file_path = self.root
        return FileTreeUtil.tree(file_path)

    def __del__(self):
        """对象销毁时自动保存"""
        logger.info("Saving project data before exiting...")
        self.save()


def init_project(project_name: str, project_desc: str, requirement_path: Path = None, modules: List[Module] = None):
    """
        项目初始化工作：
            1、在默认的工作目录下创建项目文件夹
            2、在项目文件夹下创建docs和resources文件夹
            3、存储用户交互得数据，并使用prompt生成需求文档并存储到resources文件夹下
            4、然后通过project反向序列化得json，传递给项目初始化函数，进行项目初始化
    """
    llm = LLM()
    logger.info(f"项目信息：\n项目名称：{project_name}\n项目描述：{project_desc}")
    # 生成项目名称(用蛇形命名法命名)
    gen_project_name_by_snake = PromptUtil.prompt_handle("gen_project_name_by_snake.prompt", {
        "project_name": project_name
    })
    project_name_by_snake = llm.completion(gen_project_name_by_snake)

    # 0. 初始化项目
    logger.info(f" ==================== 开始准备项目:{project_name_by_snake} ====================")
    project = Project(project_name=project_name,
                      project_name_by_snake=project_name_by_snake,
                      project_description=project_desc,
                      requirement_path=requirement_path,
                      modules=modules)

    project.modules = modules if modules else []

    # 存储用户的输入数据
    user_data_content = f'{{"project_name": "{project_name}", "project_desc": "{project_desc}"}}'
    FileUtil.write_file(project.resources / "user_data" / "user_data.json", user_data_content)

    logger.info("==================== 项目准备完成！====================")

    # 1、需求生成和存储

    logger.info("==================== 开始生成需求文档 ====================")

    gen_prd_prompt = PromptUtil.prompt_handle("gen_prd.prompt", {
        "project_name": project_name,
        "project_desc": project_desc
    })
    res_prd = llm.completion(gen_prd_prompt)
    real_prd = MarkdownUtil.parse_code_block(res_prd, "markdown")

    project.requirement_path = project.docs / "prd" / "requirement.md"
    FileUtil.write_file(project.requirement_path, real_prd[0])

    logger.info("==================== 需求文档生成完成！====================")

    # 2、数据库设计文档生成

    logger.info("==================== 开始生成数据库设计文档 ====================")
    database_design_prompt = PromptUtil.prompt_handle("gen_dbdd.prompt", {
        "prd_content": real_prd[0]
    })
    # 修改为根据用户描述生成数据库设计文档
    # database_design_prompt = PromptUtil.prompt_handle("gen_dbdd_without_prd.prompt", {
    #     "project_desc": project_desc
    # })
    database_design_doc = llm.completion(database_design_prompt)
    database_design = MarkdownUtil.parse_code_block(database_design_doc, "markdown")
    project.database_design_path = project.docs / "database_design" / "database_design.md"
    FileUtil.write_file(project.database_design_path, database_design[0])

    logger.info("==================== 数据库设计文档生成完成！====================")
    # 3、项目初始化

    logger.info("==================== 开始初始化项目 ====================")

    NestTemplateHandler.create_project(project.project_home, project.serialize)

    logger.info("==================== 项目初始化完成！====================")

    # 4、数据库信息生成，prisma schema生成

    logger.info("==================== 开始生成prisma schema ====================")

    database_prompt = PromptUtil.prompt_handle("gen_prisma_schema.prompt", {
        "database_design_doc": project.database_design_doc,
        "prisma_schema": project.prisma_schema
    })
    database_res = llm.completion(database_prompt)
    prisma_database = MarkdownUtil.parse_code_block(database_res, "prisma")
    FileUtil.write_file(project.project_home / "prisma" / "schema.prisma", prisma_database[0])

    logger.info("==================== prisma schema生成完成！====================")

    # 5、依据prisma实体生成entity的json格式

    logger.info("==================== 开始生成entity的json格式 ====================")

    gen_entity_prompt = PromptUtil.prompt_handle("gen_entity_list.prompt", {
        "schema_prisma": prisma_database[0],
        "schema_json": Entity.get_schema(),
    })
    entity_res = llm.completion(gen_entity_prompt)
    logger.info("entity_res: \n" + entity_res)
    entity_str_list = MarkdownUtil.parse_code_block(entity_res, "json")
    entity_list = [json.loads(entity) for entity in entity_str_list]
    FileUtil.append_file(
        project.resources / 'entity' / "entity_list.json",
        json.dumps(entity_list, ensure_ascii=False, indent=4))

    logger.info("==================== entity的json格式生成完成！====================")

    # 6、将模块添加到项目

    logger.info("==================== 开始添加模块到项目 ====================")
    for entity in entity_list:
        # json 格式化
        module = Module(name=entity["name"],
                        entity=Entity(name=entity["name"],
                                      attributes=entity["attributes"],
                                      description=entity["description"],
                                      ))
        project.add_module(module)

    logger.info("==================== 模块添加完成！====================")

    return project


def load_project(project_name_by_snake: str) -> Project:
    """ 从json文件中加载已有的项目 """
    project_path = DEFAULT_WORKSPACE_ROOT / project_name_by_snake / "project.json"
    return Project.load(project_path)

