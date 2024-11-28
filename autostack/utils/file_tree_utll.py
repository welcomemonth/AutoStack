#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/11/27
@Author  : RexTechie
@File    : file_tree_utll.py
@Desc    : 输出文件树
"""

from pathlib import Path
from typing import Callable, Dict, List, Union
from gitignore_parser import parse_gitignore


class FileTreeUtil:

    @staticmethod
    def tree(root: Union[str, Path], gitignore: Union[str, Path] = None) -> str:
        """
        递归遍历目录结构并以树状格式输出。
        Example
            >>> FileTreeUtil.tree(".")
            utils
            +-- serialize.py
            +-- project_repo.py
            +-- tree.py
            +-- mmdc_playwright.py
            +-- __pycache__
            |   +-- __init__.cpython-39.pyc
            |   +-- redis.cpython-39.pyc
            |   +-- singleton.cpython-39.pyc
            +-- parse_docstring.py

            >>> FileTreeUtil.tree(".", gitignore="../../.gitignore")
            utils
            +-- serialize.py
            +-- project_repo.py
            +-- tree.py
            +-- mmdc_playwright.py
            +-- parse_docstring.py
        :param root: 起始遍历的根目录。
        :param gitignore: .gitignore 文件路径。
        :return: 目录树的字符串表示。
        """
        root = Path(root).resolve()

        git_ignore_rules = parse_gitignore(gitignore) if gitignore else None
        dir_ = {root.name: FileTreeUtil._list_children(root=root, git_ignore_rules=git_ignore_rules)}
        v = FileTreeUtil._print_tree(dir_)
        return "\n".join(v)

    @staticmethod
    def _list_children(root: Path, git_ignore_rules: Callable) -> Dict[str, Dict]:
        dir_ = {}
        for i in root.iterdir():
            if git_ignore_rules and git_ignore_rules(str(i)):
                continue
            try:
                if i.is_file():
                    dir_[i.name] = {}
                else:
                    dir_[i.name] = FileTreeUtil._list_children(root=i, git_ignore_rules=git_ignore_rules)
            except (FileNotFoundError, PermissionError, OSError):
                dir_[i.name] = {}
        return dir_

    @staticmethod
    def _print_tree(dir_: Dict[str, Dict]) -> List[str]:
        ret = []
        for name, children in dir_.items():
            ret.append(name)
            if not children:
                continue
            lines = FileTreeUtil._print_tree(children)
            for j, v in enumerate(lines):
                if v[0] not in ["+", " ", "|"]:
                    ret = FileTreeUtil._add_line(ret)
                    row = f"+-- {v}"
                else:
                    row = f"    {v}"
                ret.append(row)
        return ret

    @staticmethod
    def _add_line(rows: List[str]) -> List[str]:
        for i in range(len(rows) - 1, -1, -1):
            v = rows[i]
            if v[0] != " ":
                return rows
            rows[i] = "|" + v[1:]
        return rows
