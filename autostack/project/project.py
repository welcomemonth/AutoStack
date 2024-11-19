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


# 实体属性类
class Attribute(BaseModel):
    """
    {
        "name": "id",
        "type": "String",
        "required": True,
        "comment": "用户ID"
    }
    """
    name: str
    type: str
    required: bool
    comment: str
    
    @property
    def serialize(self):
        return self.model_dump()


# 实体类
class Module(BaseModel):
    entity_name: str
    description: str
    attributes: List[Attribute] = None
    
    @property
    def serialize(self):
        # exclude={"entity_name"}采用这个可以去除一些属性
        return self.model_dump()

@singleton
class Project(BaseModel):
    project_name: str
    project_description: str
    author: Optional[str] = "autostack"
    requirement_path: Optional[str] = None
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
        return self.model_dump(exclude={"project_home", "resources", "docs", "requirement_path", })
    
    @property
    def file_tree(self, file_path: Union[str, Path] = None):
        """返回项目的文件树"""
        if file_path is None:
            file_path = self.project_home
        return tree(file_path)


def init_project(project_name: str, project_desc: str, requirement_path: str = None, modules: List[Module] = []):
    """
        项目初始化工作：
            1、在默认的工作目录下创建项目文件夹
            2、在项目文件夹下创建docs和resources文件夹
            3、存储用户交互得数据，并使用prompt生成需求文档并存储到resources文件夹下
            4、然后通过project反向序列化得json，传递给项目初始化函数，进行项目初始化
    """
    project = Project(project_name=project_name, project_description=project_desc, requirement_path=requirement_path, modules=modules)
    llm = LLM()
    ######################### 0、存储用户的输入数据  ############################
    user_data_floder = project.resources / "user_data"
    os.makedirs(user_data_floder, exist_ok=True)
    with open(user_data_floder / "user_data.json", "w", encoding='utf-8') as f:
        f.write(f'{{"project_name": "{project_name}", "project_desc": "{project_desc}"}}')
        
    ######################### 1、需求生成和存储 ##################################
    prd_folder = project.docs / 'prd'
    os.makedirs(prd_folder, exist_ok=True)
    
    genprd_prompt = prompt_handle("gen_prd.prompt", project_name + ':\n' + project_desc)
    res_prd = llm.completion(genprd_prompt)
    real_prd = parse_code_block(res_prd, "markdown")
    
    with open(prd_folder / "requirement.md", "w", encoding='utf-8') as f:
        f.write(real_prd)
    
    ######################### 2、数据库表生成 ##################################
    database_folder = project.docs / 'database_design'
    os.makedirs(database_folder, exist_ok=True)
    
    database_prompt = prompt_handle("database.prompt", real_prd)
    database_md = llm.completion(database_prompt)
    database = parse_code_block(database_md, "markdown")
    with open(database_folder / "database.md", "w", encoding='utf-8') as f:
        f.write(database)
    
    ######################### 3、项目初始化 ##################################
    NestProjectTemplateHandler(project.serialize, project.project_home / project.project_name).create_project()
    
    return project
