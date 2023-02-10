# -*- coding: UTF-8 -*-

"""
@Author ：Patrick Lam
@Date ：2023-01-31
"""

import logging
import colorlog

logging_level = {"INFO": logging.INFO,
                 "ERROR": logging.ERROR,
                 "DEBUG": logging.DEBUG,
                 "WARN": logging.WARN,
                 "CRITICAL": logging.CRITICAL
                 }

log_colors_config = {
    'DEBUG': 'white',  # cyan white
    'INFO': 'green',
    'WARN': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

class LoggingUtil:

    def __init__(self, level, logging_file):
        """
        :param level: 日志级别
        :param logging_file: 日志文件路径
        """
        self.level = level
        self.logging_file = logging_file

    def get_logging(self):

        # 日志配置
        logging.basicConfig(level=logging_level[self.level],
                            filename=self.logging_file,
                            filemode='a',
                            format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        console = logging.StreamHandler()
        console.setLevel(logging_level[self.level])
        # 设置日志打印格式
        console.setFormatter(
            logging.Formatter(
            '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
            )
        )
        # 设置日志打印颜色
        console.setFormatter(
            colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
            # datefmt='%Y-%m-%d  %H:%M:%S',
            log_colors=log_colors_config
            )
        )

        # 将定义好的console日志handler添加到root logger
        logging.getLogger('').addHandler(console)
        return logging
