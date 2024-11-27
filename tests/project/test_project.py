import pytest
from autostack.project import Project, Module  # 导入你的类


@pytest.fixture
def project():
    """创建一个测试用的 Project 实例"""
    return Project(project_name="AI Project", requirement_path="path/to/requirement_doc")


def test_create_project(project):
    """测试创建项目"""
    assert project.project_name == "AI Project"
    assert project.requirement_path == "path/to/requirement_doc"
    assert project.modules == []  # 初始时模块列表为空


def test_add_module(project):
    """测试添加模块"""
    project.add_module(module_name="Module 1", module_description="First module")
    assert len(project.modules) == 1
    assert project.modules[0].module_name == "Module 1"
    assert project.modules[0].status == "Not Started"
    assert project.modules[0].module_description == "First module"


def test_update_module_status(project):
    """测试更新模块状态"""
    project.add_module(module_name="Module 1", module_description="First module")
    project.update_module_status(module_name="Module 1", status="In Progress")
    assert project.modules[0].status == "In Progress"


def test_singleton(project):
    """测试单例模式，确保每次实例化的对象都是同一个"""
    project2 = Project(project_name="New Project", requirement_path="path/to/another/requirement_doc")
    assert project is project2  # 由于使用了singleton，project 和 project2 应该是同一个实例


def test_project_summary(project, capsys):
    """测试项目概览，确保打印模块信息"""
    project.add_module(module_name="Module 1", module_description="First module")
    project.add_module(module_name="Module 2", module_description="Second module", status="In Progress")

    # 捕获标准输出
    project.project_summary()
    captured = capsys.readouterr()

    # 检查打印的内容
    assert "Project: AI Project" in captured.out
    assert "Modules:" in captured.out
    assert "Module 1 - Not Started" in captured.out
    assert "Module 2 - In Progress" in captured.out
