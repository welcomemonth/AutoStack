#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/12/1 20:34
@Author: zhengyu
@File: docker_operate.py
@Desc zhengyu 2024/12/1 20:34. + cause
"""
from pathlib import Path
from typing import Union
from autostack.common import logger
import docker
import random
import time

# 创建 Docker 客户端
client = docker.from_env()


def start_container(project_path: Union[Path, str], image_name: str = 'nestjs:latest'):
    """
    根据镜像名称启动容器，挂载本地项目并映射端口
    @:param project_path: 本机项目路径
    @:param image_name: 镜像名称，默认nestjs/cli
    """
    try:
        print(f"正在启动容器: {image_name}")
        port = random.randint(20000, 50000)
        # 启动容器，映射容器的 3000 端口到宿主机的随机端口
        container = client.containers.run(
            image_name,
            command="tail -f /dev/null",  # 启动容器后保持容器运行，不执行其他命令
            volumes={project_path: {'bind': '/app', 'mode': 'rw'}},  # 将本地项目目录挂载到容器内
            working_dir='/app',  # 容器内的工作目录
            ports={'3000/tcp': port},  # None 表示随机端口
            detach=True,  # 后台运行容器
            restart_policy={"Name": "always"}  # 确保容器重启策略为“总是重启”
        )

        time.sleep(5)  # 这里等待5秒，可以根据实际情况调整时间
        return container
    except Exception as e:
        print(f"容器启动失败: {e}")
        return None


def execute_command_in_container(container, command):
    """
    在容器中执行命令并返回执行日志

    """
    try:
        # 在容器中执行命令
        exec_log = container.exec_run(command, tty=True, stream=True)

        # 读取并打印命令输出
        print(f"执行命令: {command}")
        logs = ""
        for log in exec_log[1]:
            logger.info(log.decode("utf-8").strip())
            logs += log.decode("utf-8")

        return logs
    except Exception as e:
        print(f"执行命令失败: {e}")
        return None


# 主函数示例
# def main():
#     # 设置 NestJS 项目路径和镜像名称
#     project_path = r'E:\projectfactory\AutoStack\workspace\app'  # NestJS 项目的路径
#     image_name = 'node:16'  # 使用的基础镜像
#
#     # 启动容器并返回容器对象
#     container = start_container(image_name, project_path)
#
#     if container:
#         # 在容器中执行命令：安装依赖、构建并启动 NestJS 项目
#         execute_command_in_container(container, "npm install")
#         execute_command_in_container(container, "npm run build")
#         execute_command_in_container(container, "npm run start:prod")
#
#         # 容器将在后台继续运行，执行其他操作可根据需求添加
#         print("容器将在后台继续运行...")


# if __name__ == "__main__":
#     main()
