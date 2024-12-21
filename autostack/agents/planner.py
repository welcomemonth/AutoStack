#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/12/13 10:22
@Author: zhengyu
@File: planner
@Desc zhengyu 2024/12/13 10:22. + cause
"""

from __future__ import annotations

import json
import pickle
from autostack.common.logs import logger
from typing import List, Union, Optional
from .base_agent import BaseAgent
from autostack.llm import Message, Plan, Task
from autostack.project import Project
from autostack.utils import PromptUtil, MarkdownUtil


class Planner:

    def __init__(self, agent: BaseAgent):
        self.plan: Optional[Plan] = None
        self.agent = agent

    @property
    def current_task_id(self):
        return self.plan.current_task_id

    @property
    def current_task(self):
        return self.plan.current_task

    def set_goal(self, goal: str):
        """
        设置目标，一个计划只有一个目标
        为实现这个目标会设立多个任务。设立目标之后，立即分解计划
        :param goal: 计划的目标
        """
        self.plan = Plan(goal=goal)
        self._split_plan()

    def update_plan(self, max_tasks: int = 5, max_retries: int = 3):
        context = self.get_useful_memories()
        self._split_plan(context=context, max_tasks=max_tasks)

    def _split_plan(self, context: str = "", max_tasks: int = 7):
        # 任务规划
        unfinished_tasks = [task.get_task_desc() for task in self.plan.get_unfinished_tasks()]
        unfinished_tasks_str = json.dumps(unfinished_tasks, indent=4, ensure_ascii=False)

        context = context if context else "当前项目没有开始，请从零开始设计任务实现用户目标。"
        subdivide_plan_prompt = PromptUtil.prompt_handle("tasks_subdivision.prompt", {
            "goal": self.plan.goal,
            "context": context,
            "max_tasks": max_tasks,
            "existing_tasks": unfinished_tasks_str
        })

        tasks_str_json = self.agent.llm.completion(subdivide_plan_prompt)
        tasks_str = MarkdownUtil.parse_code_block(tasks_str_json, "json")
        tmp_tasks = json.loads(tasks_str[0])
        tasks = [Task(**task) for task in tmp_tasks]
        self.plan.add_tasks(tasks)

    def process_task_result(self, task_result):
        """
        处理review之后的结果, 如果确认就更新一下任务状态
        如果返回错误就去解决这错误，如果返回其他内容就是去更新剩余的任务
        :param task_result:
        :return:
        """
        confirmed = self.ask_review(task_result)
        if confirmed == "confirmed":
            self.confirm_task()
        elif confirmed == "error":
            # todo 怎么解决问题
            pass
        else:
            pass
            # self.update_plan_task()

    def ask_review(self, max_iter: int = 5):
        """
        通过AI来review
        :param max_iter:
        :return:
        """
        # FIXME 这个prompt还没有写，判断是否成功
        prompt = PromptUtil.prompt_handle("task_is_success.prompt", {
            "task_desc": self.current_task.task_desc,
            "task_result": self.current_task.result
        })

        res = self.agent.llm.completion(prompt)
        return res

    def confirm_task(self):
        """ 确认任务 """
        self.current_task.is_finished = True

        self.plan.finish_current_task()

    def get_useful_memories(self) -> str:
        """返回有用的记忆，目前即是返回任务的执行记录"""

        finished_tasks_dict = [task.to_dict() for task in self.plan.get_finished_tasks()]
        finished_tasks_memories = json.dumps(finished_tasks_dict, indent=4, ensure_ascii=False)

        return finished_tasks_memories

    def get_plan_status(self) -> str:
        """
        准备计划状态的组成部分
        :return:
        """
        finished_tasks = self.plan.get_finished_tasks()
        task_results = [task.result for task in finished_tasks]
        task_results = "\n\n".join(task_results)
        prompt = PLAN_STATUS.format(
            task_results=task_results,
            current_task=self.current_task.task_desc,
        )
        """
        ## Finished Tasks
        ### code
        ```python
        {code_written}
        ```

        ### execution result
        {task_results}

        ## Current Task
        {current_task}

        ## Task Guidance
        Write complete code for 'Current Task'. And avoid duplicating code from 'Finished Tasks', such as repeated import of packages, reading data, etc.
        Specifically, {guidance}
        """

        return prompt

    def save(self):
        with open(self.agent.project.resources / "plan.json", 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(project_resources_path):
        """从文件加载planner的内容"""
        filepath = project_resources_path / "plan.json"
        with open(filepath, 'rb') as f:
            return pickle.load(f)

