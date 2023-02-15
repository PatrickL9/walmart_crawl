# -*- coding: UTF-8 -*-
#!/usr/bin/python3

"""
walamrt平台根据关键词搜索，查询前3页查询结果的详情页信息
@Author ：Patrick Lam
@Date ：2023-02-03
"""
import json
import os
import random
import time
import requests
import pandas as pd
from lxml import etree
from util.setting import logging, PROXY_URL, ipPool, main_url, headers, SUCCESS_ID, PRODUCT_LIST
import walmart_cookie_generate


def get_ip_pool():
    """
    获取IP代理池
    :param
    :return:
    """
    logging.info('获取IP代理，搭建代理IP池')
    ips = requests.get(PROXY_URL)
    for ip in ips.text.split('\r\n'):
        if len(ip) > 8:
            ipPool.append('http://' + ip)


def get_random_ip():
    """
    获取随机代理IP
    :param
    :return:随机代理IP
    """
    ip = random.choice(ipPool)
    logging.info('获取随机代理IP: ' + ip)
    return ip


def get_all_url(url_r, crawl_page):
    """
    爬取初始url及其翻页中所有的产品url
    :param url_r: 初始url
    :param crawl_page: 指定爬取页数（可选）
    :return:PRODUCT_LIST: 所有产品的item_id、url和sponsored
    """
    for i in range(1, crawl_page):
        # 如果是第1页，取原url，如果是翻页，拼接翻页url
        if i == 1:
            crawl_url = url_r
        else:
            crawl_url = url_r + '?page={}&affinityOverride=default'.format(str(i))
        i += 1
        retry_cnt = 0
        # 防反爬，重试三次
        while retry_cnt <= 3:
            retry_cnt += 1
            logging.info('解析产品列表页，url链接： ' + crawl_url)
            proxies = {'http': get_random_ip()}
            cookies = walmart_cookie_generate.get_random_cookie()
            resp = requests.get(crawl_url, headers=headers, proxies=proxies, cookies=cookies, timeout=5)
            text = resp.content.decode('utf-8')
            if 'Robot or human' in text:
                logging.info('被反爬了，重试第{}次'.format(str(retry_cnt)))
            else:
                # 解析页面text
                get_item_list(text)
                break
            # 放反爬，每次解析暂停5秒
            time.sleep(5)
    logging.info('解析产品列表结束，一共需爬取{}个产品链接'.format(len(PRODUCT_LIST)))
    return PRODUCT_LIST


def get_item_list(h_text):
    """
    根据request返回的txt，解析json，获取所有产品url的列表
    :param h_text: request返回的txt文本
    :return:
    """
    html = etree.HTML(h_text)
    json_data = html.xpath('//script[@type="application/json"]/text()')[0]
    json_text = json.loads(json_data)
    # with open('D:\pythonProject\walmart_crawl\html_file\product_list.json', encoding='UTF-8') as f:
    #     json_text = json.load(f)
    item_list = json_text['props']['pageProps']['initialData']['searchResult']['itemStacks'][0]['items']
    for il in item_list:
        try:
            item_id = il['usItemId']
            item_url = il['canonicalUrl']
            sponsored = il['isSponsoredFlag']
            # 获取的itemid,url和sponsored传进全局变量PRODUCT_LIST
            PRODUCT_LIST.append([item_id, main_url + item_url, sponsored])
            # print(item_id, main_url + item_url, sponsored)
        except:
            continue

def get_product_detail(product_list):
    """
    获取产品url，通过解析script的application/json，获取详情页信息
    :param product_list: 所有产品url的列表
    :return:df_result 详情页信息明细
    """
    # 定义一个dataframe，用于保存爬取结果
    df_result = pd.DataFrame(columns=('item_id', 'product_url', 'ad_tag', 'title', 'catalog_full', 'brand', 'price',
                                      'seller_name', 'proseller_tag', 'variant', 'shipping_method', 'shortDescription',
                                      'longDescription', 'specification', 'warranty',
                                      'reviews', 'stars', 'one_star_reviews', 'two_star_reviews', 'three_star_reviews',
                                      'four_star_reviews', 'five_star_reviews', 'first_review_date')
                             )
    # count = 0
    for pl in product_list:
        # 检查是否重复产品链接
        crawl_tag = 0
        for ii in SUCCESS_ID:
            if pl[0] == ii:
                logging.info('itemid {} 已被抓取过，跳过'.format(pl[0]))
                crawl_tag = 1
                break
        if crawl_tag == 1:
            continue
        # 产品详情页url
        product_url = pl[1]
        # 是否sponsored
        ad_tag = pl[2]
        logging.info('开始解析产品详情页，解析url ' + product_url)
        # 获取随机代理IP和随机cookie
        proxies = {'http': get_random_ip()}
        cookies = walmart_cookie_generate.get_random_cookie()
        resp = requests.get(product_url, headers=headers, proxies=proxies, cookies=cookies, timeout=100)

        if resp.status_code == 200:
        # if 1 == 1:
            text = resp.content.decode('utf-8')
            if 'Robot or human' in text:
                logging.warning('被反爬了，退出。被反爬的item_id是： ' + pl[0])
                continue
            if 'Pro Seller' in text:
                is_proseller = '是'
            else:
                is_proseller = '否'
            # xpath解析，由于walmart网站所有的信息都放在script的application/json下面，直接解析json比较方便
            html = etree.HTML(text)
            json_data = html.xpath('//script[@type="application/json"]/text()')[0]
            json_text = json.loads(json_data)

            # with open('D:\pythonProject\walmart_crawl\html_file\product_detail.json', encoding='UTF-8') as f:
            #     json_text = json.load(f)

            product_detail = json_text['props']['pageProps']['initialData']['data']
            # is_proseller = '否'
            # 品牌
            brand = product_detail['product']['brand']
            # 产品链接
            product_url = product_detail['product']['canonicalUrl']
            # 长描述
            try:
                longDescription = product_detail['idml']['longDescription']
            except:
                longDescription = ''
            # 短描述
            try:
                shortDescription = product_detail['idml']['shortDescription']
            except:
                shortDescription = ''
            # 产品规范 specification
            specification_text = ''
            try:
                specification = product_detail['idml']['specifications']
            except:
                specification = ''
            for sc in specification:
                for v in sc.values():
                    specification_text = specification_text + '\n' + v
            # 产品保修 Warranty
            try:
                warranty = product_detail['idml']['warranty']['information']
            except:
                warranty = ''
            # 标题
            title = product_detail['product']['name']
            # 产品价格
            try:
                price = product_detail['product']['priceInfo']['currentPrice']['priceString']
            except:
                price = ''
            # 产品ID
            item_id = product_detail['product']['usItemId']
            # 卖家
            seller_name = product_detail['product']['sellerDisplayName']
            # 评论数
            stars = product_detail['reviews']['averageOverallRating']
            # 总评论数
            reviews = product_detail['reviews']['totalReviewCount']
            # 1至5星评论数
            one_star_reviews = product_detail['reviews']['ratingValueOneCount']
            two_star_reviews = product_detail['reviews']['ratingValueTwoCount']
            three_star_reviews = product_detail['reviews']['ratingValueThreeCount']
            four_star_reviews = product_detail['reviews']['ratingValueFourCount']
            five_star_reviews = product_detail['reviews']['ratingValueFiveCount']
            # 类目路径
            catalog_full = product_detail['contentLayout']['modules'][0]['configs']['ad']['pageContext']['itemContext']['categoryPathName']
            # 邮寄方式。'FC'即为沃尔玛，'MARKETPLACE'为三方卖家
            shipping_method = product_detail['product']['fulfillmentType']
            shipping_method = '沃尔玛提供' if shipping_method == 'FC' else '第三方卖家提供'
            # 是否pro seller
            # 变体
            varirant_list = product_detail['product']['variantCriteria']
            varirant_dict = {}
            for vl in varirant_list:
                for n in vl['variantList']:
                    varirant_dict.setdefault(vl['name'], []).append(n['name'])

            # 上架时间（最早评论时间），需要访问reviews页面
            first_review_date = ''
            review_url = 'https://www.walmart.com/reviews/product/{}?sort=submission-asc'.format(pl[0])
            logging.info('开始解析产品评论页，解析url ' + review_url)
            proxies = {'http': get_random_ip()}
            cookies = walmart_cookie_generate.get_random_cookie()

            rv_count = 0
            while rv_count <= 3:
                # 暂停2秒，访问评论页
                rv_count += 1
                time.sleep(2)
                resp = requests.get(review_url, headers=headers, proxies=proxies, cookies=cookies, timeout=100)
                if resp.status_code == 200:
                    try:
                        text = resp.content.decode('utf-8')
                        # print(text)
                        html = etree.HTML(text)
                        first_review_date = html.xpath('//main[@role="main"]//li[contains(@style,"translate3d")][1]//div[@class="f7 gray"]/text()')
                        break
                    except Exception as e:
                        print(e)
                        logging.debug('评论页面解析失败，重试第{}次。 '.format(rv_count) + review_url)
            # print(first_review_date)

            temp_dict = {
                'item_id': item_id,
                'product_url': 'www.walmart.com' + product_url,
                'ad_tag': ad_tag,
                'title': title,
                'catalog_full': catalog_full,
                'brand': brand,
                'price': price,
                'seller_name': seller_name,
                'proseller_tag': is_proseller,
                'variant': varirant_dict,
                'shipping_method': shipping_method,
                'shortDescription': shortDescription,
                'longDescription': longDescription,
                'specification': specification_text.strip(),
                'warranty': warranty,
                'reviews': reviews,
                'stars': stars,
                'one_star_reviews': one_star_reviews,
                'two_star_reviews': two_star_reviews,
                'three_star_reviews': three_star_reviews,
                'four_star_reviews': four_star_reviews,
                'five_star_reviews': five_star_reviews,
                'first_review_date': ''.join(first_review_date),
            }
            # 把爬取结果插入到dataframe最后一行
            df_result.loc[len(df_result)] = temp_dict
            logging.info('本页爬取结束，itemid {} 加入已爬取队列'.format(pl[0]))
            SUCCESS_ID.append(pl[0])
        logging.info('本页爬取结束，暂停5秒')
        time.sleep(5)
    return df_result


def save_to_csv(df, key_word):
    """
    结果保存到csv
    :param df: 结果明细
    :param key_word: 查询的关键词
    :return:
    """
    file_name = 'walamrt平台' + key_word + '爬取结果.csv'
    file_path = os.path.join(os.getcwd(), file_name)
    df.to_csv(file_path, index=False, sep=',')
    logging.info('保存结果到CSV文件，保存路径： ' + file_path)


def run(url_f, key_word, crawl_page):
    """
    程序运行本体
    :param url_f: 网址前缀
    :param key_word: 查询的关键词
    :param crawl_page: 指定爬取页数（可选）
    :return:
    """
    get_ip_pool()
    logging.info('开始walmart关键词爬取。初始url: ' + url_f + ' 关键词： ' + key_word)
    df = get_product_detail(get_all_url(url_f, crawl_page))
    # print(df)
    save_to_csv(df, key_word)


if __name__ == '__main__':
    # 初始网页前缀
    url_front = 'https://www.walmart.com/browse/baby/double-strollers/5427_118134_1101428'
    # 搜索关键词
    ky = 'Double Strollers'
    # 指定爬取页数
    cp = 3
    # 传入网址和关键词，开始爬取
    run(url_front, ky, cp)
