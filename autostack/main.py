import json
from autostack.llm import LLM
from autostack.project import init_project, load_project
from autostack.common import DEFAULT_WORKSPACE_ROOT, logger
from autostack.utils import MarkdownUtil, FileUtil, PromptUtil
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


def main():
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

    container = DockerContainer(current_project.project_home)
    # container = start_container(r"E:\projectfactory\AutoStack\workspace\app")
    # 1、npm install
    run_command(container, "npm install")
    # 2、prisma format，格式化 Prisma schema 文件（schema.prisma）的内容，使其符合标准的代码风格和格式规范
    run_command(container, "npx prisma format")
    # 3、根据 prisma schema 生成 prisma client
    run_command(container, "npx prisma migrate dev --name init")
    # 4、项目编译
    run_command(container, "npm run build")
    # 5、项目启动
    run_command(container, "npm run start")
    # 3、对于某个复杂业务接口，让AI根据项目中已有的模块中的服务文件来选择该业务需要哪些服务，携带者已有的服务文件，生成该业务接口的代码

    # 4、对于业务接口代码进行测试，解决该接口的运行成功出现的bug

    # 5、循环遍历所有业务，生成所有业务接口代码


if __name__ == "__main__":
    main()
