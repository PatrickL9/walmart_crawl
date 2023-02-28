# -*- coding: UTF-8 -*-
#!/usr/bin/python3

"""
构建ip代理池
@Author ：Patrick Lam
@Date ：2023-03-01
"""
from util.logging_conf import logging
import requests
import random


class ProxyPool:
    def __init__(self, proxy_url):
        """
        :param proxy_url: ip代理的api地址
        """
        self.proxy_url = proxy_url
        self.ipPool = []

    def get_ip_pool(self):
        """
        获取IP代理池
        :param
        :return:
        """
        logging.info('获取IP代理，搭建代理IP池')
        ips = requests.get(self.proxy_url)
        for ip in ips.text.split('\r\n'):
            if len(ip) > 8:
                self.ipPool.append('http://' + ip)
        logging.info('本次一共获取IP代理{}个'.format(str(len(self.ipPool))))
        # return self.ipPool

    def get_random_ip(self):
        """
        获取随机代理IP
        :param
        :return:随机代理IP
        """
        ip = random.choice(self.ipPool)
        logging.info('获取随机代理IP: ' + ip)
        return ip
