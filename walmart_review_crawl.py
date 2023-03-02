# -*- coding: UTF-8 -*-
# !/usr/bin/python3

"""
walamrt平台根据关键词搜索，查询前1页查询结果的星级、评论数和价格
@Author ：Patrick Lam
@Date ：2023-02-28
"""
import json
import os
import time
import datetime
import requests
import pandas as pd
from lxml import etree
from util.setting import proxy_pool, main_url, headers
from util.logging_conf import logging
import walmart_cookie_generate


# pd.set_option('display.width', None)
# pd.set_option('display.max_rows', None)


def parse_all_url(url_list):
    """
    解析script的application/json，本页信息
    :param url_list: 本次爬取的所有url链接列表
    """
    for ul in url_list:
        # print(ul)
        retry_cnt = 0
        while retry_cnt <= 3:
            retry_cnt += 1
            logging.info('解析搜索页面，url链接： ' + ul)
            proxies = {'http': proxy_pool.get_random_ip()}
            cookies = walmart_cookie_generate.get_random_cookie()
            resp = requests.get(ul, headers=headers, proxies=proxies, cookies=cookies, timeout=5)
            text = resp.content.decode('utf-8')
            if 'Robot or human' in text:
                logging.info('遇到验证码，重试第{}次'.format(str(retry_cnt)))
            else:
                # 解析页面text
                df_result = get_item_detail(ul, text)
                logging.info('解析完成，保存结果到CSV')
                save_to_csv(df_result)
                break
            # 防反爬，每次解析暂停5秒
            time.sleep(5)


def get_item_detail(url, h_text):
    # def get_item_detail():
    """
    解析script的application/json，获取本页信息
    :param url: 本次解析的url链接
    :param h_text: 网页解析文本
    :return df_result: 爬取结果明细
    """
    # 定义一个dataframe，用于保存爬取结果
    df_result = pd.DataFrame(columns=('search_url', 'result_total', 'product_url', 'title',
                                      'stars', 'reviews', 'price')
                             )
    html = etree.HTML(h_text)
    json_data = html.xpath('//script[@type="application/json"]/text()')[0]
    json_text = json.loads(json_data)
    # with open('html_file/search_list.json', encoding='UTF-8') as f:
    #     json_text = json.load(f)
    # print(json_text)
    # noinspection PyBroadException
    try:
        result_total = json_text['props']['pageProps']['initialData']['searchResult']['itemStacks'][0]['count']
    except Exception as e:
        logging.warn('提取不到department结果数量，url链接： ' + url)
        # department_dict = {}
        result_total = 0
    # print(department_dict)
    # print(result_total)
    # noinspection PyBroadException
    try:
        product_list = json_text['props']['pageProps']['initialData']['searchResult']['itemStacks'][0]['items']
    except Exception as e:
        logging.warn('提取不到产品列表，url链接： ' + url)
        product_list = []
    # print(product_list)
    for pl in product_list:
        # 产品链接
        try:
            product_url = main_url + pl['canonicalUrl']
        except Exception as e:
            product_url = ''
        # 产品标题
        try:
            title = pl['name']
        except:
            title = ''
        # 产品售价
        try:
            price = pl['price']
        except:
            price = ''
        # 评论数
        try:
            reviews = pl['numberOfReviews']
        except:
            reviews = ''
        # 星级评分
        try:
            stars = pl['averageRating']
        except:
            stars = ''

        temp_dict = {
            'search_url': url,
            'result_total': result_total,
            # 'department_dict': department_dict,
            'product_url': product_url,
            'title': title,
            'stars': stars,
            'reviews': reviews,
            'price': price
        }
        # 把爬取结果插入到dataframe最后一行
        df_result.loc[len(df_result)] = temp_dict
    # 防反爬，暂停5秒
    logging.debug('防反爬，暂停5秒')
    time.sleep(5)
    return df_result
    # print(df_result)


def save_to_csv(df):
    """
    结果保存到csv
    :param df: 结果明细
    :return:
    """
    to_day = datetime.datetime.now()
    file_name = 'walamrt平台类目评论爬取结果_{}{:02}{:02}.csv'.format(to_day.year, to_day.month, to_day.day)
    file_path = os.path.join(os.getcwd(), file_name)
    df.to_csv(file_path, mode='a', index=False, sep=',')
    logging.info('保存结果到CSV文件，保存路径： ' + file_path)


def run(url_list):
    """
    程序运行本体
    :param url_list: 需爬取的目标链接
    :return:
    """
    # 构建代理池
    proxy_pool.get_ip_pool()
    # 开始爬取
    parse_all_url(url_list)
    logging.info('运行成功，退出程序')


if __name__ == '__main__':
    target_url = []
    # 从txt中读取目标asin
    with open('review_target.txt', 'r') as f:
        arr = f.readlines()
        for tg in arr:
            a = tg.strip()
            target_url.append(a)
    logging.info('读取目标txt完毕，一共有{}个链接需要爬取'.format(len(target_url)))
    run(target_url)
