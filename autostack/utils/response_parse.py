#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/12/21 22:35
@Author: zhengyu
@File: response_parse
@Desc zhengyu 2024/12/21 22:35. + cause
"""
import re
import json


# 创建一个对AI内容进行解析，并操作的类
class ResponseHandler:
    def __init__(self, content):
        self.content = content
        self.task_list = parse_bolt_artifacts(content)


def parse_bolt_artifacts(content):
    # 使用正则表达式提取所有的 <boltArtifact> 和 <boltAction> 标签
    bolt_artifacts = []

    # 正则表达式提取 boltArtifact 和 boltAction 标签的内容
    artifact_pattern = re.compile(r'<boltArtifact.*?id="(.*?)".*?title="(.*?)">(.*?)</boltArtifact>', re.DOTALL)
    action_pattern = re.compile(r'(?i)<boltAction\s+type="(.*?)".*?(filePath|shellPath)="(.*?)"\s*>(.*?)</boltAction>', re.DOTALL)

    # 查找所有符合 <boltArtifact> 的块
    artifacts = artifact_pattern.findall(content)

    for artifact in artifacts:
        artifact_id, artifact_title, actions_content = artifact
        artifact_data = {
            "id": artifact_id,
            "title": artifact_title,
            "boltActions": []
        }

        # 查找该 <boltArtifact> 内部的所有 <boltAction>
        actions = action_pattern.findall(actions_content)
        for action in actions:
            action_type, path_type, path_value, action_content = action
            action_data = {
                "type": action_type,
                f"{path_type.lower()}": path_value,
                "content": action_content.strip()
            }
            artifact_data["boltActions"].append(action_data)

        bolt_artifacts.append(artifact_data)

    # 返回 JSON 格式
    return bolt_artifacts


if __name__ == '__main__':
    res = """
    基于上述高校学生管理系统的需求文档，我建议将这个项目命名为“EduManage”。
为了开始这个项目，请遵循以下步骤创建项目：
<boltArtifact id="setup-edumanage-project" title="Setup EduManage Project">
  <boltAction type="shell" shellpath="/app">
  nest new edu-manage --package-manager npm
  </boltAction>
</boltArtifact>
    """
    bolt_artifacts = parse_bolt_artifacts(res)
    for bolt_artifact in bolt_artifacts:
        bolt_actions = bolt_artifact.get("boltActions")
        for bolt_action in bolt_actions:
            if bolt_action.get("type") == "file":
                print(bolt_action.get("filepath"))
            elif bolt_action.get("type") == "shell":
                print(bolt_action.get("shellpath"))

