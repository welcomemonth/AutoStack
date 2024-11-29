from typing import List, Optional, Union, Any
from pathlib import Path
from pydantic import BaseModel
from autostack.utils import MarkdownUtil, FileTreeUtil, FileUtil, PromptUtil
from autostack.common.const import DEFAULT_WORKSPACE_ROOT
from autostack.llm import LLM
from autostack.common.logs import logger
from autostack.template_handler import create_project, create_module
from .module import Module


# @singleton
class Project(BaseModel):
    project_name: str
    project_description: str
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
        self.root = DEFAULT_WORKSPACE_ROOT / self.project_name
        self.project_home = self.root / self.project_name
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
    def prisma_schema(self):
        return FileUtil.read_file(self.project_home / "prisma" / "schema.prisma")

    def add_module(self, module: Module):
        """添加模块到项目"""
        create_module(self.project_home, module.serialize)
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
        # 将项目序列化得数据保存到文件，每次都覆盖原文件
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


def init_project(project_name: str, project_desc: str, requirement_path: Path = None, modules: List[Module] = []):
    """
        项目初始化工作：
            1、在默认的工作目录下创建项目文件夹
            2、在项目文件夹下创建docs和resources文件夹
            3、存储用户交互得数据，并使用prompt生成需求文档并存储到resources文件夹下
            4、然后通过project反向序列化得json，传递给项目初始化函数，进行项目初始化
    """
    project = Project(project_name=project_name,
                      project_description=project_desc,
                      requirement_path=requirement_path,
                      modules=modules)
    llm = LLM()
    project.modules = []

    # 0、存储用户的输入数据
    user_data_content = f'{{"project_name": "{project_name}", "project_desc": "{project_desc}"}}'
    FileUtil.write_file(project.resources / "user_data" / "user_data.json", user_data_content)

    # 1、需求生成和存储
    gen_prd_info = {
        "project_name": project_name,
        "project_desc": project_desc
    }
    gen_prd_prompt = PromptUtil.prompt_handle("gen_prd.prompt", gen_prd_info)
    res_prd = llm.completion(gen_prd_prompt)
    real_prd = MarkdownUtil.parse_code_block(res_prd, "markdown")

    project.requirement_path = project.docs / "prd" / "requirement.md"
    FileUtil.write_file(project.requirement_path, real_prd[0])

    # 2、数据库设计文档生成
    database_design_info = {
        "prd_content": real_prd[0]
    }
    database_prompt = PromptUtil.prompt_handle("database_design.prompt", database_design_info)
    database_design_doc = llm.completion(database_prompt)
    database_design = MarkdownUtil.parse_code_block(database_design_doc, "markdown")
    project.database_design_path = project.docs / "database_design" / "database_design.md"
    FileUtil.write_file(project.database_design_path, database_design[0])

    # 3、项目初始化
    create_project(project.project_home, project.serialize)
    return project


def load_project(project_name: str) -> Project:
    """ 从json文件中加载已有的项目 """
    project_path = DEFAULT_WORKSPACE_ROOT / project_name / "project.json"
    return Project.load(project_path)
