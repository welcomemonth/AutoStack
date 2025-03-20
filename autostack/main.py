import json
from autostack.llm import LLM
from autostack.project import init_project, load_project
from autostack.common import logger
from autostack.utils import MarkdownUtil, PromptUtil
from autostack.container import DockerContainer

llm = LLM()


def run_command(container: DockerContainer, command: str) -> str:
    """运行命令"""
    res_log = container.execute_command(command)
    isSuccess_prompt = PromptUtil.prompt_handle("command_is_exec_success.prompt", {
        "command": command,
        "result": res_log
    })
    response = llm.completion(isSuccess_prompt)
    if json.loads(MarkdownUtil.parse_code_block(response, "json")[0])["result"] == "fail":
        logger.error(res_log)
        exit()


def initialize_project(project_name: str, project_desc: str):
    """初始化项目"""
    current_project = init_project(project_name, project_desc)
    current_project.save()
    container = DockerContainer(current_project.project_home)

    return current_project, container


def load_existing_project(project_name_by_snake: str):
    """加载已有项目"""
    current_project = load_project(project_name_by_snake)
    container = DockerContainer(current_project.project_home)
    return current_project, container


def main():
    while True:
        choice = input("需要新建项目还是从已有的项目中加载？\n1.新建\n2.加载\n请选择（1-2）：")
        if choice == "1":
            project_name = input("请输入项目名称（中文）：")
            project_desc = input("请输入对该项目的描述（越具体越好）：")
            current_project, container = initialize_project(project_name, project_desc)
            run_command(container, "npm install --force")
            run_command(container, "npx prisma format")
            run_command(container, "npx prisma migrate dev --name init")
            run_command(container, "npm run build")
            run_command(container, "npm run start")
            break
        elif choice == "2":
            project_name_by_snake = input("请输入已存在的项目目录名：")
            current_project, container = load_existing_project(project_name_by_snake)
            choice2 = input("是否需要重新安装依赖？\ny.yes\nn.no\n请选择（y or n）：")
            if choice2.lower()[0] == "y":
                run_command(container, "npm install --force")
            choice2 = input("是否需要重新迁移数据库？\ny.yes\nn.no\n请选择（y or n）：")
            if choice2.lower()[0] == "y":
                run_command(container, "npx prisma format")
                run_command(container, "npx prisma migrate dev --name init")
            run_command(container, "npm run build")
            run_command(container, "npm run start")
            break
        else:
            print("请选择（1-2）：")

    # project_name = input("请输入项目名称（中文）：")
    # project_name_by_snake = input("请输入项目名称（可选，英文，用下划线隔开）：")
    # container = None
    # if (DEFAULT_WORKSPACE_ROOT / project_name_by_snake).exists():
    #     choice = input("项目已存在！\n1.加载项目\n2.新建？\n请选择（1-2）：")
    #     while choice.lower() not in ["1", "2"]:
    #         choice = input("请选择（1-2）：")
    #     if choice == "1":
    #         current_project, container = load_existing_project(project_name)
    #     elif choice == "2":
    #         project_name += "_new"
    #         project_desc = input("请输入对该项目的描述（越具体越好）：")
    #         current_project, container = initialize_project(project_name, project_desc)
    # else:
    #     project_desc = input("请输入对该项目的描述（越具体越好）：")
    #     current_project, container = initialize_project(project_name, project_desc)


if __name__ == "__main__":
    main()
