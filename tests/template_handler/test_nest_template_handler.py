# test_nest_template_handler.py

import os
from pathlib import Path
from autostack.common.const import ROOT
from unittest.mock import patch, mock_open, MagicMock
from autostack.template_handler.nest_template_handler import (
    generate_nest_attributions,
    generate_file_by_template,
    create_module,
    create_project,
    add_module_to_app,
)

# Mock paths that will be used in the tests
TEST_TEMPLATE_PATH = ROOT / 'templates/backend/'
TEST_PROJECT_PATH = Path("path/to/project")


# Test cases for generate_nest_attributions function
def test_generate_nest_attributions():
    attributions = [
        {"name": "id", "type": "Int", "required": True, "comment": "The ID of the entity"},
        {"name": "name", "type": "String", "required": False, "comment": "The name of the entity"},
    ]
    expected_output = "\n    /**\n     * The ID of the entity\n     */\n    @ApiProperty()\n    @IsInt()\n    id: number;\n\n    /**\n     * The name of the entity\n     */\n    @ApiProperty()\n    @IsString()\n    name?: string;"
    assert generate_nest_attributions(attributions) == expected_output


# Test cases for generate_file_by_template function
@patch("builtins.open", new_callable=mock_open)
def test_generate_file_by_template(mock_file):
    target_path = TEST_PROJECT_PATH / "file.txt"
    template_path = TEST_TEMPLATE_PATH / "template.txt"
    info = {"key": "value"}

    # Mock the template content
    mock_template_content = "This is a template content with {key}."
    mock_file.return_value.read_data = mock_template_content

    # Expected file content after substitution
    expected_content = "This is a template content with value."

    generate_file_by_template(target_path, template_path, info)

    # Check if the file was written correctly
    mock_file.assert_called_once_with(str(target_path), 'w', encoding='utf-8')
    handle = mock_file()
    handle.write.assert_called_once_with(expected_content)


# Test cases for create_module function
@patch("autostack.template_handler.nest_template_handler.create_project", return_value=None)
@patch("builtins.open", new_callable=mock_open)
def test_create_module(mock_file, mock_create_project):
    module_info = {
        "name": "TestModule",
        "attributes": [{"name": "testAttr", "type": "String", "required": True, "comment": "Test attribute"}],
    }
    project_path = TEST_PROJECT_PATH

    create_module(project_path, module_info)

    # Check if the module_info is being passed correctly
    mock_create_project.assert_called_once_with(project_path, module_info)


# Test cases for create_project function
@patch("builtins.open", new_callable=mock_open)
def test_create_project(mock_file):
    project_path = TEST_PROJECT_PATH
    project_info = {
        "project_name": "TestProject",
        "project_description": "A test project",
    }

    # Mock the template content
    mock_template_content = "This is a template content."
    mock_file.return_value.read_data = mock_template_content

    # Expected file content after substitution
    expected_content = "This is a template content."

    create_project(project_path, project_info)

    # Check if the file was written correctly
    mock_file.assert_called_once_with(str(project_path / "package.json"), 'w', encoding='utf-8')
    handle = mock_file()
    handle.write.assert_called_once_with(expected_content)


# Test cases for add_module_to_app function
@patch("autostack.template_handler.nest_template_handler.generate_file_by_template", return_value=None)
def test_add_module_to_app(mock_generate_file):
    project_path = TEST_PROJECT_PATH
    module_name = "TestModule"

    add_module_to_app(project_path, module_name)

    # Check if the app.module.ts file was written correctly
    mock_generate_file.assert_called_once()


