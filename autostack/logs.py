#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/6/1 12:41
@Author  : alexanderwu
@File    : logs.py
"""

import sys
from datetime import datetime
from functools import partial

from loguru import logger as _logger

from segmapy.const import ROOT

'''
print_level：控制台输出的日志级别，默认为 INFO。
logfile_level：日志文件输出的日志级别，默认为 DEBUG。

'''
def define_log_level(print_level="INFO", logfile_level="DEBUG", name: str = None):
    """Adjust the log level to above level"""
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y%m%d")
    log_name = f"{name}_{formatted_date}" if name else formatted_date  # name a log with prefix name

    _logger.remove() # 清除已有的 logger 设置
    # 使用 _logger.add() 添加两个日志输出目标：
    _logger.add(sys.stderr, level=print_level) #
    _logger.add(ROOT / f"logs/{log_name}.txt", level=logfile_level)
    return _logger


logger = define_log_level()


def log_llm_stream(msg):
    _llm_stream_log(msg)


def set_llm_stream_logfunc(func):
    global _llm_stream_log
    _llm_stream_log = func


_llm_stream_log = partial(print, end="")
