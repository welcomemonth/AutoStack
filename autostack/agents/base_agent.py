#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/12/12 22:45
@Author: zhengyu
@File: base_agent
@Desc zhengyu 2024/12/12 22:45. + cause
"""

from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    BaseAgent
    """

    def __init__(self, tools, llm, verbose=False, max_iter=10):
        self.llm = llm
        self.tools = tools
        self.short_memory = []
        self.verbose = verbose
        self.max_iter = max_iter

        from .planner import Planner
        self.planner = Planner(self)  # Agent的计划能力，通过对记忆中的内容检索，给出下一步的具体任务

    @property
    def context(self):
        return "\n".join([f"{name}: {message}" for name, message in self.short_memory])

    def add_message(self, name, message):
        self.short_memory.append((name, message))

    def pretty_print(self, message_type, content):
        """
        Displays the given content with color-coded formatting based on the message type.

        Args:
            message_type (str): The type of message (e.g., "Decision", "Tool call", "Tool result", "Answer").
            content (str): The content to be displayed.
        """

        if not self.verbose:
            return

        color_codes = {
            "Decision": "\033[95m",  # Magenta
            "Reasoning": "\033[94m",  # Blue
            "Tool call": "\033[93m",  # Yellow
            "Tool args": "\033[93m",  # Yellow
            "Tool result": "\033[92m",  # Green
            "Not Completed": "\033[91m",  # Red
            "Answer": "\033[92m"  # Green
        }

        if message_type in color_codes:
            print(f"{message_type}:")
            print(f"{color_codes[message_type]}{content}\033[0m")
        else:
            print(f"{message_type}:")
            print(content)

    def run(self):
        """
        Abstract method to process a user's prompt and return a response.

        This method should be implemented by subclasses to define the specific
        behavior of how the agent processes and responds to user prompts.

        Returns:
            str: 任务执行结果

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses must implement the 'run' method.")
