import unittest
from autostack.project import Project, init_project, load_project


def get_project():
    """
    创建一个测试用的 Project 实例
    :return: Project实例
    """
    return Project(
        project_name="AI Project",
        requirement_path="path/to/requirement_doc"
    )


class TestProject(unittest.TestCase):

    def test_create_project(self):
        """
        测试创建项目
        """
        project = get_project()
        assert project.project_name == "AI Project"
        assert project.requirement_path == "path/to/requirement_doc"
        assert project.modules == []  # 初始时模块列表为空

    def test_add_module(self):
        """
        测试添加模块
        """
        project = get_project()
        project.add_module(module_name="Module 1", module_description="First module")
        assert len(project.modules) == 1
        assert project.modules[0].module_name == "Module 1"
        assert project.modules[0].status == "Not Started"
        assert project.modules[0].module_description == "First module"

    def test_update_module_status(self):
        """
        测试更新模块状态
        """
        project = get_project()
        project.add_module(module_name="Module 1", module_description="First module")
        project.update_module_status(module_name="Module 1", status="In Progress")
        assert project.modules[0].status == "In Progress"

    def test_singleton(self):
        """
        测试单例模式，确保每次实例化的对象都是同一个
        """
        project = get_project()
        project2 = Project(project_name="New Project", requirement_path="path/to/another/requirement_doc")
        assert project is project2  # 由于使用了singleton，project 和 project2 应该是同一个实例
