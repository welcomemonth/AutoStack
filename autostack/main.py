from autostack.llm import LLM
from autostack.project import init_project, load_project
from autostack.common.const import DEFAULT_WORKSPACE_ROOT
from autostack.utils import MarkdownUtil, FileUtil, PromptUtil


def main():
    llm = LLM()
    current_project = None
    project_name = input("your project name：")
    project_desc = input("your project description：")
    # 判断路径是否存在
    if (DEFAULT_WORKSPACE_ROOT / project_name).exists():
        choice = input("项目已存在，加载项目 or 新建？load / new: ")
        # 忽略大小写
        if choice.lower() == "load":
            current_project = load_project(project_name)
        elif choice.lower() == "new":
            # 直接将已有目录修改名称
            pass
        else:
            # 退出
            exit()

    # 如果current_project不为空，则直接使用，否则初始化一个新项目
    current_project = current_project if current_project else init_project(project_name, project_desc)
    # project信息存储,方便下次读取
    current_project.save()

    # 1、根据项目需求文档和数据库设计文档来生成 创建模块所需要的内容：
    database_prompt = PromptUtil.prompt_handle("database.prompt",
                                               current_project.requirement_doc,
                                               current_project.database_design_doc,
                                               current_project.prisma_schema)
    database_res = llm.completion(database_prompt)
    database = MarkdownUtil.parse_code_block(database_res, "prisma")
    FileUtil.append_file(current_project.project_home / "prisma" / "schema.prisma", database)
    # 2、分析需求文档，生成接口描述，项目中的模块文件描述。

    # 3、对于某个复杂业务接口，让AI根据项目中已有的模块中的服务文件来选择该业务需要哪些服务，携带者已有的服务文件，生成该业务接口的代码

    # 4、对于业务接口代码进行测试，解决该接口的运行成功出现的bug

    # 5、循环遍历所有业务，生成所有业务接口代码


if __name__ == "__main__":
    main()
