import json

from autostack.llm import LLM
from autostack.project import init_project, load_project, Module
from autostack.template_handler import NestProjectTemplateHandler, NestModuleTemplateHandler
from autostack.utils import MarkdownUtil, FileUtil, PromptUtil
from autostack.project import init_project, load_project
from autostack.common.const import DEFAULT_WORKSPACE_ROOT
from autostack.utils import MarkdownUtil, FileUtil, PromptUtil


def main():
    llm = LLM()
    current_project = None
    project_name = input("your project name：")
    project_desc = input("your project description：")
    # 判断路径是否存在
    choice = "new"
    if (DEFAULT_WORKSPACE_ROOT / project_name).exists():
        choice = input("项目已存在，加载项目 or 新建？load / new: ")
        # 忽略大小写
        if choice.lower() == "load":
            current_project = load_project(project_name)
        elif choice.lower() == "new":
            # 修改目录名称
            pass
        else:
            # 退出
            exit()

    # 如果current_project不为空，则直接使用，否则初始化一个新项目
    current_project = current_project if current_project else init_project(project_name, project_desc)

    nest_project_template_handler = NestProjectTemplateHandler(current_project.serialize, current_project.project_home)
    nest_project_template_handler.create_project()

    # 1、根据项目需求文档和数据库设计文档来生成 创建模块所需要的内容：
    database_info = {
        "requirement_doc": current_project.requirement_doc,
        "database_design_doc": current_project.database_design_doc,
        "prisma_schema": current_project.prisma_schema
    }
    database_prompt = PromptUtil.prompt_handle("database.prompt", database_info)
    database_res = llm.completion(database_prompt)
    prisma_database = MarkdownUtil.parse_code_block(database_res, "prisma")
    FileUtil.append_file(current_project.project_home / "prisma" / "schema.prisma", prisma_database[0])
    # # 2、分析需求文档，生成接口描述，项目中的模块文件描述。
    gen_entity_info = {
        "schema_prisma": prisma_database[0],
        "schema_json": Module.get_schema(),
    }
    gen_entity_prompt = PromptUtil.prompt_handle("gen_entity.prompt", gen_entity_info)
    entity_res = llm.completion(gen_entity_prompt)
    entity_str_list = MarkdownUtil.parse_code_block(entity_res, "json")
    # 存储entity_list
    FileUtil.append_file(current_project.resources / 'entity' / "entity_list.json", json.dumps(entity_str_list))

    # entity_str_list = json.loads(FileUtil.read_file(current_project.resources / 'entity' / "entity_list.json"))
    current_project.save()
    entity_list = []
    for entity in entity_str_list:
        # json 格式化
        entity = json.loads(entity)
        module = Module(name=entity["name"],
                        description=entity["description"],
                        attributes=entity["attributes"])
        current_project.add_module(module)
        module_handler = NestModuleTemplateHandler(entity, current_project.project_home)
        module_handler.create_module()
        entity_list.append(entity)

    nest_project_template_handler.add_modules_config_to_project(entity_list)
    # print(entity_list)
    # project信息存储, 方便下次读取
    current_project.save()
    # print(current_project.modules)
    # 3、对于某个复杂业务接口，让AI根据项目中已有的模块中的服务文件来选择该业务需要哪些服务，携带者已有的服务文件，生成该业务接口的代码

    # 4、对于业务接口代码进行测试，解决该接口的运行成功出现的bug

    # 5、循环遍历所有业务，生成所有业务接口代码


if __name__ == "__main__":
    main()
