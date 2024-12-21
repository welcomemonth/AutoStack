from pathlib import Path
from typing import Union
from autostack.common import logger, CONTAINER_WORKDIR
import docker
import random
import time
import threading

# 创建 Docker 客户端
client = docker.from_env()


# 全局唯一的Docker_Util
class DockerUtil:
    """
    在docker容器中执行的shell 工具类
    """
    _instance = None
    _container = None

    def __new__(cls, project_path: Union[Path, str]):
        if cls._instance is None:
            cls._instance = super(DockerUtil, cls).__new__(cls)
            cls._instance.project_path = project_path
            cls._container = cls._start_container(project_path)
            if cls._container:
                cls._instance.execute_command(command="service postgresql restart")
                # 设置容器时间
                cls._instance.execute_command(command="ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime")
        return cls._instance

    @classmethod
    def _start_container(cls, project_path: Union[Path, str], image_name: str = 'zhengyuzhang/nestjs:latest'):
        """
        根据镜像名称启动容器，挂载本地项目并映射端口
        @:param project_path: 本机项目路径
        @:param image_name: 镜像名称，默认nestjs/cli
        """
        try:
            logger.info(f"正在启动容器: {image_name}")
            port = random.randint(30000, 50000)
            # 启动容器，映射容器的 3000 端口到宿主机的随机端口
            container = client.containers.run(
                image_name,
                command="tail -f /dev/null",  # 启动容器后保持容器运行，不执行其他命令
                volumes={project_path: {'bind': CONTAINER_WORKDIR, 'mode': 'rw'}},  # 将本地项目目录挂载到容器内
                working_dir=CONTAINER_WORKDIR,  # 容器内的工作目录
                ports={'3000/tcp': port},  # None 表示随机端口
                detach=True,  # 后台运行容器
                restart_policy={"Name": "always"}  # 确保容器重启策略为“总是重启”
            )
            time.sleep(3)  # 这里等待5秒，可以根据实际情况调整时间
            return container
        except Exception as e:
            logger.error(f"容器启动失败: {e}")
            return None

    def execute_command(self, command, workdir: Union[str, Path] = CONTAINER_WORKDIR, detach=False, stream=True):
        """
        :param command:   执行的命令
        :param workdir:   命令执行目录
        :param detach:
        :param stream:
        :return:
        """
        logger.info(f"执行命令: {command}")
        try:
            # 在容器中执行命令
            exec_log = self._container.exec_run(command, tty=True, stream=stream, detach=detach, workdir=workdir)
            logs = ""
            last_log_summary = None  # 用于存储上一条日志的摘要

            for log in exec_log[1]:
                log_text = log.decode("utf-8").strip()

                # 提取日志关键部分，例如去掉特殊符号、提取文本核心内容
                log_summary = ''.join(filter(str.isalpha, log_text))  # 只保留字母作为摘要

                # 判断是否与上一条摘要相同，或者是全新的日志
                if log_summary != last_log_summary:
                    logger.info(log_text)  # 仅记录摘要变化的日志
                    last_log_summary = log_summary  # 更新上一条摘要
                    logs += log_text + "\n"  # 保存日志
                else:
                    # 可以选择不保存重复动态日志，或者记录简略信息
                    pass
            return logs
        except Exception as e:
            logger.info(f"执行命令失败: {e}")
            return None

    def execute_command_thread(self, command: str, workdir: Union[str, Path] = CONTAINER_WORKDIR, detach=False, stream=True):
        """
        多线程执行
        :param stream:
        :param detach:
        :param workdir:
        :param command:
        :return:
        """
        thread = threading.Thread(target=self.execute_command, args=(command, workdir, detach, stream))
        thread.start()
        return thread