# -*- coding: UTF-8 -*-
#!/usr/bin/python3

"""
设置日志级别和log保存路径
@Author ：Patrick Lam
@Date ：2023-02-28
"""

import os
import datetime
from util import logging_util

# 日志级别
LOGGING_LEVEL = 'INFO'

# 日志文件保存路径
logging_dir = os.getcwd() + r'\log'
if not os.path.isdir(logging_dir):
    os.makedirs(logging_dir)
# 日志文件前缀处理
to_day = datetime.datetime.now()
LOGGING_PATH = logging_dir + r'\cd_crawl_{}{:02}{:02}.log'.format(to_day.year, to_day.month, to_day.day)
# 设置日志级别
logging = logging_util.LoggingUtil(LOGGING_LEVEL, LOGGING_PATH).get_logging()
