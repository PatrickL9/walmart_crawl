# -*- coding: UTF-8 -*-
#!/usr/bin/python3

"""
walamrt平台根据关键词搜索，查询前1页查询结果的星级、评论数和价格
@Author ：Patrick Lam
@Date ：2023-02-28
"""
# import json
# import os
# import random
import time
# import requests
# import pandas as pd
# from lxml import etree
from util.setting import proxy_pool
from util.logging_conf import logging
# import walmart_cookie_generate

logging.info("hello world")
proxy_pool.get_ip_pool()
for i in range(5):
    ip = proxy_pool.get_random_ip()
    print(ip)
    time.sleep(1)
