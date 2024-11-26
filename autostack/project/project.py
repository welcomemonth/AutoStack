import os
from typing import List, Optional, Union
from pathlib import Path
from pydantic import BaseModel
from autostack.prompt import prompt_handle
from autostack.utils import singleton, parse_code_block, tree
from autostack.const import DEFAULT_WORKSPACE_ROOT
from autostack.llm import LLM
from autostack.logs import logger
from autostack.template_handler import NestModuleTemplateHandler, NestProjectTemplateHandler
from .module import Module


# @singleton
class Project(BaseModel):
    project_name: str
    project_description: str
    author: Optional[str] = "autostack"
    requirement_path: Optional[Path] = None
    database_design: Optional[Path] = None
    modules: Optional[List[Module]] = []  # 模块列表，默认为空
    project_home: Optional[Path] = None
    resources: Optional[Path] = None
    docs: Optional[Path] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.project_home = DEFAULT_WORKSPACE_ROOT / self.project_name
        self.resources = self.project_home / 'resources'  # 都是处理后的json格式
        self.docs = self.project_home / 'docs'  # 原生的markdown格式

        os.makedirs(self.project_home, exist_ok=True)
        os.makedirs(self.docs, exist_ok=True)
        os.makedirs(self.resources, exist_ok=True)

    @property
    def requirement(self):
        # 读取需求文件
        try:
            with open(self.requirement_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"文件未找到: {self.requirement_path}")
            return ""
        except IOError as e:
            logger.error(f"读取文件时发生错误: {e}")
            return ""

    @property
    def database_design_content(self):
        """读取数据库设计文档并返回内容"""
        if self.database_design.exists():
            try:
                with open(self.database_design, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                logger.error(f"读取数据库设计文档时出错: {e}")
                return ""
        else:
            logger.error(f"数据库设计文档不存在: {self.database_design}")
            return ""


    def add_module(self, module_name: str, module_description: str, status: str = 'Not Started'):
        """添加模块到项目"""
        module = Module(module_name=module_name, module_description=module_description, status=status)
        self.modules.append(module)
        print(f"Module '{module_name}' added to project.")

    def update_module_status(self, module_name: str, status: str):
        """更新指定模块的状态"""
        for module in self.modules:
            if module.module_name == module_name:
                module.status = status
                print(f"Module '{module_name}' status updated to '{status}'.")
                break
        else:
            print(f"Module '{module_name}' not found in project.")

    @property
    def serialize(self):
        # exclude={"name"}采用这个可以去除一些属性
        return self.model_dump(exclude={"project_home", "resources", "docs", "requirement_path"})

    def save(self):
        # 将项目序列化得数据保存到文件，每次都覆盖原文件
        with open(self.project_home / "project.json", "w", encoding='utf-8') as f:
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
            file_path = self.project_home
        return tree(file_path)


def init_project(project_name: str, project_desc: str, requirement_path: Path = None, modules: List[Module] = []):
    """
        项目初始化工作：
            1、在默认的工作目录下创建项目文件夹
            2、在项目文件夹下创建docs和resources文件夹
            3、存储用户交互得数据，并使用prompt生成需求文档并存储到resources文件夹下
            4、然后通过project反向序列化得json，传递给项目初始化函数，进行项目初始化
    """
    project = Project(project_name=project_name, project_description=project_desc, requirement_path=requirement_path,
                      modules=modules)
    llm = LLM()
    project.modules = []
    ######################### 0、存储用户的输入数据  ############################
    user_data_floder = project.resources / "user_data"
    os.makedirs(user_data_floder, exist_ok=True)
    with open(user_data_floder / "user_data.json", "w", encoding='utf-8') as f:
        f.write(f'{{"project_name": "{project_name}", "project_desc": "{project_desc}"}}')

    ######################### 1、需求生成和存储 ##################################
    prd_folder = project.docs / 'prd'
    os.makedirs(prd_folder, exist_ok=True)

    genprd_prompt = prompt_handle("gen_prd.prompt", "项目名称：" + project_name + '\n' + "项目描述：" + project_desc)
    res_prd = llm.completion(genprd_prompt)
    real_prd = parse_code_block(res_prd, "markdown")

    with open(prd_folder / "requirement.md", "w", encoding='utf-8') as f:
        f.write(real_prd)
    project.requirement_path = prd_folder / "requirement.md"

    ######################### 2、数据库设计文档生成 ##################################
    database_folder = project.docs / 'database_design'
    os.makedirs(database_folder, exist_ok=True)

    database_prompt = prompt_handle("database_design.prompt", real_prd)
    database_md = llm.completion(database_prompt)
    database = parse_code_block(database_md, "markdown")
    with open(database_folder / "database.md", "w", encoding='utf-8') as f:
        f.write(database)

    project.database_design = database_folder / "database.md"
    ######################### 3、项目初始化 ##################################
    NestProjectTemplateHandler(project.serialize, project.project_home / project.project_name).create_project()

    return project


def load_project(project_name: str) -> Project:
    """ 从json文件中加载已有的项目 """
    project_path = DEFAULT_WORKSPACE_ROOT / project_name / "project.json"
    return Project.load(project_path)
