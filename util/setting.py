# -*- coding: UTF-8 -*-
#!/usr/bin/python3

"""
爬虫程序各项配置参数
@Author ：Patrick Lam
@Date ：2023-02-10
"""

import redis
from util import logging_util, proxy_pool


# 代理API
PROXY_URL = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=460e34f07cf041899a22e79353081288&orderno=YZ2021112078186AsWJy&returnType=1&count=3'
# ipPool = []
# 设置ip代理池
proxy_pool = proxy_pool.ProxyPool(PROXY_URL)

# 主站点链接
main_url = 'https://www.walmart.com'
# 请求头
headers = {
    'authority': 'www.walmart.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    'referer': 'https://www.walmart.com/',
    'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'service-worker-navigation-preload': 'true',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
}

# 目标详情列表
PRODUCT_LIST = []
# 已爬取过的item_id，用于做链接去重处理
SUCCESS_ID = []

# redis服务，用于保存cookie池
REDIS_CLIENT = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
WALMART_COOKIE_KEY = "walmart_cookies"
# walmart_cate_start_key = 'wal_start_cate_url'

avail_cookie = REDIS_CLIENT.llen(WALMART_COOKIE_KEY)
# print('WALMART_COOKIE_KEY 一共有{}个'.format(avail_cookie))
# print('WALMART_COOKIE_KEY的内容如下：')
# print(REDIS_CLIENT.lrange(WALMART_COOKIE_KEY, 0, -1))

