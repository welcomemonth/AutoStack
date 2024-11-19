from autostack.logs import logger
from autostack.project import init_project


def main():
    project_name = input("请输入您的需求（项目名称）：")
    project_desc = input("请输入您的需求（项目描述）：")

    PROJECT = init_project(project_name, project_desc)
    logger.info(f"项目初始化完成：{PROJECT.file_tree}")


if __name__ == "__main__":
    main()






