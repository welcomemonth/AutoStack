#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/11/14 17:58
@Author  : Rex
@File    : file_util.py.py
"""
import os
import shutil
from string import Template
from autostack.common.logs import logger


class FileUtil:

    @staticmethod
    def create_dir(dir_path):
        """
        如果路径不存在，则创建
        :param dir_path: 路径地址
        """
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    @staticmethod
    def write_file(file_path, content):
        """
        写入文件
        :param file_path: 文件路径
        :param content: 文件内容
        :return:
        """
        # 获取文件路径中的目录部分
        directory = os.path.dirname(file_path)
        # 如果目录不存在，则创建它
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    @staticmethod
    def append_file(file_path, content):
        """
        追加内容到文件,如果文件不存在则创建文件
        :param file_path: 文件路径
        :param content: 文件内容
        :return:
        """
        # 获取文件路径中的目录部分
        directory = os.path.dirname(file_path)
        # 如果目录不存在，则创建它
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(file_path, 'a+', encoding='utf-8') as file:
            file.write(content)

    @staticmethod
    def remove_dir(dir_path):
        """
        删除目录
        :param dir_path: 目录路径
        """
        shutil.rmtree(dir_path)

    @staticmethod
    def remove_file(file_path):
        """
        删除文件
        :param file_path: 文件路径
        :return:
        """
        os.remove(file_path)

    @staticmethod
    def read_file(file_path):
        """
        读取文件内容
        :param file_path: 文件路径
        :return: 文件内容
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"文件未找到: {file_path}")
            return None
        except IOError as e:
            logger.error(f"读取文件时发生错误: {e}")
            return None

    @staticmethod
    def get_template(template_file_path):
        """
        获取模板文件
        :param template_file_path: 模板文件地址
        :return: 模板文件文本
        """
        template_str = None
        with open(template_file_path, 'r', encoding='utf-8') as template_file:
            template_str = template_file.read()

        return Template(template_str)

    @staticmethod
    def copy_all_files(src_dir, dest_dir):
        """
        将 src_dir 下的所有文件复制到 dest_dir。

        :param src_dir: 源目录
        :param dest_dir: 目标目录
        """
        try:
            # 确保源目录存在
            if not os.path.exists(src_dir):
                raise FileNotFoundError(f"源目录 '{src_dir}' 不存在。")

            # 如果目标目录不存在，创建目标目录
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            # 遍历源目录中的所有文件
            for item in os.listdir(src_dir):
                src_path = os.path.join(src_dir, item)
                dest_path = os.path.join(dest_dir, item)

                # 如果是文件，则复制
                if os.path.isfile(src_path):
                    shutil.copy2(src_path, dest_path)  # 使用 copy2 保留元数据
                elif os.path.isdir(src_path):
                    # 如果是目录，递归复制目录内容
                    shutil.copytree(src_path, dest_path, dirs_exist_ok=True)

            print(f"所有文件已成功复制到 '{dest_dir}'。")
        except Exception as e:
            print(f"复制文件时出错: {e}")

    @staticmethod
    def generate_env(env_dict: dict, file_path):
        """
        用于生成环境变量xxx.env
        :param env_dict: 环境变量字典
        :param file_path: 文件路径
        :return:
        """
        env_str = ""
        for key, value in env_dict.items():
            env_str += f"{key}={value}\n"
        FileUtil.write_file(file_path, env_str)
