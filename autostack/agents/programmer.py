#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/12/13 13:54
@Author: zhengyu
@File: programmer
@Desc zhengyu 2024/12/13 13:54. + cause
"""

from .base_agent import BaseAgent
from autostack.common.const import CONTAINER_WORKDIR
from autostack.llm import Task, LLM, Action, ActionType
from autostack.project import Project
from autostack.utils import PromptUtil, parse_bolt_artifacts, FileUtil, PathUtil, DockerUtil

COMPOSE_GOAL = """
根据需求文档和设计好的数据库设计文档，使用nestjs和prisma，postgresql为我实现这个项目。
需求文档如下：
```
{requirement_doc}
```
数据库设计文档如下：
```
{database_design_doc}
```
"""


class Programmer(BaseAgent):
    def __init__(self, tools, project: Project, verbose=False, max_iter=10):
        # 调用父类的构造方法
        llm = LLM(system_prompt=PromptUtil.prompt_handle("programmer_system_prompt.prompt"))
        super().__init__(tools, llm, verbose, max_iter)

        self.project = project
        self.container = DockerUtil(self.project.root)

    def run(self):
        """
        根据已有项目信息进行任务的开发
        """
        # 首先根据这个任务进行任务分析，细化一个可执行的任务列表
        goal = COMPOSE_GOAL.format(
            requirement_doc=self.project.requirement_doc,
            database_design_doc=self.project.database_design_doc
        )
        self.planner.set_goal(goal=goal)
        # 开始执行任务列表的任务
        while self.planner.current_task:
            # 执行计划器的当前任务
            self.perform_task()
            # 确认任务是否完成
            self.planner.confirm_task()
            # 根据任务执行结果更新后续计划
            self.planner.update_plan()

    def perform_task(self):
        """
        根据任务生成代码或执行命令
        """
        # 根据任务以及任务依赖执行任务
        code_generate_prompt = PromptUtil.prompt_handle("perform_task.prompt", {
            "task_desc": self.planner.current_task.task_desc,
            "cwd": CONTAINER_WORKDIR,
            "context": self.planner.plan.goal + '\n\n' + self.planner.get_useful_memories(),
        })
        res = self.llm.completion(code_generate_prompt)
        bolt_artifacts = parse_bolt_artifacts(res)
        task_actions: list[Action] = []
        for bolt_artifact in bolt_artifacts:
            bolt_actions = bolt_artifact.get("boltActions")
            for bolt_action in bolt_actions:
                if bolt_action.get("type") == "file":
                    filepath = bolt_action.get("filepath")

                    # 虚拟机路径与宿主机路径转换 将/app 转换为project_path
                    win_filepath = PathUtil.switch_linux_to_windows(self.project.root, filepath, CONTAINER_WORKDIR)
                    content = bolt_action.get("content")
                    result = FileUtil.write_file(win_filepath, content)

                    action: Action = Action(
                        type=ActionType.FILE,
                        content=content,
                        result="write success" if result else "write failed",
                    )
                    task_actions.append(action)

                elif bolt_action.get("type") == "shell":
                    shellpath = bolt_action.get("shellpath")
                    command = bolt_action.get("content")
                    task_result = self.container.execute_command(command, shellpath)

                    action: Action = Action(
                        type=ActionType.COMMAND,
                        content=command,
                        result=task_result
                    )
                    task_actions.append(action)
        self.planner.current_task.result = task_actions

