from autostack.logs import logger
from autostack.project import init_project


def main():
    project_name = input("your project name：")
    project_desc = input("your project descprition：")

    PROJECT = init_project(project_name, project_desc)
    logger.info(f"项目初始化完成：{PROJECT.file_tree}")


if __name__ == "__main__":
    main()






