import json
from autostack.docker_env import execute_command_in_container, start_container
from autostack.llm import LLM
from autostack.project import init_project, load_project
from autostack.common import DEFAULT_WORKSPACE_ROOT, logger
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
            # 修改目录名称
            pass
        else:
            # 退出
            exit()

    # 如果current_project不为空，则直接使用，否则初始化一个新项目
    current_project = current_project if current_project else init_project(project_name, project_desc)
    current_project.save()
    # 项目已经创建完成，在容器中运行这个项目
    container = start_container(current_project.project_home)
    # container = start_container(r"E:\projectfactory\AutoStack\workspace\app")
    # 1、npm install
    execute_command_in_container(container, "service postgresql restart")
    res_log = execute_command_in_container(container, "npm install")
    isSuccess_prompt = PromptUtil.prompt_handle("command_is_exec_success.prompt", {
        "command": "npm install",
        "result": res_log
    })
    response = llm.completion(isSuccess_prompt)
    if json.loads(MarkdownUtil.parse_code_block(response, "json")[0])["result"] == "fail":
        logger.error(res_log)
        return
    # 2、prisma format，格式化 Prisma schema 文件（schema.prisma）的内容，使其符合标准的代码风格和格式规范
    res_log = execute_command_in_container(container, "npx prisma format")
    isSuccess_prompt = PromptUtil.prompt_handle("command_is_exec_success.prompt", {
        "command": "npx prisma format",
        "result": res_log
    })
    response = llm.completion(isSuccess_prompt)
    if json.loads(MarkdownUtil.parse_code_block(response, "json")[0])["result"] == "fail":
        logger.error(res_log)
        return
    # 2、根据 prisma schema 生成 prisma client
    res_log = execute_command_in_container(container, "npx prisma migrate dev --name init")
    isSuccess_prompt = PromptUtil.prompt_handle("command_is_exec_success.prompt", {
        "command": "npx prisma migrate dev --name init",
        "result": res_log
    })
    response = llm.completion(isSuccess_prompt)
    if json.loads(MarkdownUtil.parse_code_block(response, "json")[0])["result"] == "fail":
        logger.error(res_log)
        return

    # 3、项目编译
    res_log = execute_command_in_container(container, "npm run build")
    isSuccess_prompt = PromptUtil.prompt_handle("command_is_exec_success.prompt", {
        "command": "npm run build",
        "result": res_log
    })
    response = llm.completion(isSuccess_prompt)
    if json.loads(MarkdownUtil.parse_code_block(response, "json")[0])["result"] == "fail":
        logger.error(res_log)
        return
    execute_command_in_container(container, "npm run start:dev")
    # logger.info(reslog)
    # 3、对于某个复杂业务接口，让AI根据项目中已有的模块中的服务文件来选择该业务需要哪些服务，携带者已有的服务文件，生成该业务接口的代码

    # 4、对于业务接口代码进行测试，解决该接口的运行成功出现的bug

    # 5、循环遍历所有业务，生成所有业务接口代码


if __name__ == "__main__":
    main()
