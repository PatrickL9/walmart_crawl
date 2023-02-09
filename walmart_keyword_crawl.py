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
import re
from html_file.html_file import html_text as h1
from html_file.html_file2 import html_text as h2
from html_file.product_detail import html_text as h3
from lxml import etree
from util import logging_util
from collections import defaultdict
import walmart_cookie_generate

# 代理API
proxy_url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=460e34f07cf041899a22e79353081288&orderno=YZ2021112078186AsWJy&returnType=1&count=1'
ipPool = []
# 主站点链接
main_url = 'https://www.walmart.com/ip/'
# 请求头
headers = {
    'authority': 'www.walmart.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    'cookie': 'ak_bmsc=13503B446C0F8C92A1F67BF7A9EB5555~000000000000000000000000000000~YAAQLJHIFx4KASeGAQAAn68TNBL7UTXXkEowg1pq7dpmeKSNkuRbZX6BTafYJYToVuCfDF36oqoob/pFr6/xuG7gpga3L9z9yLQRnaxVcyzPUiML6RLBwArx68lBWfI3TRGqQ/DryYKnINERD7Ehd7tIClgGn7WWmDi5+ZG2q1y9Zwa9zU+WkAXiWf0Q2TIKW2Zbm658h215uguQt7y/rtxmmGyJz7oIa8aoehYPURBfK3VHc4saiwyWLV2Lh6Gp2Uiiv832yY4k8WsQ6VjYTxoM2CXNKkhKZ8QUl/dFkK3bMInv3/+9I+CQhQJ3qb1hkz7b2hsjq3toS1lmDQ6W/v4/Cww7Jc4l3q6xRpNQqC+59w1EvooBqWpw/QNnUS35kC9Nd3Yl8De9AFRsOn+z03pXhBe425hCjvYZXuthM5nGL7zUGuSOwIsQyaFTBlfSq+qwTRgLLz/EXgUSvLfwdWDvzlNICT/tP/wVByM=; TBV=7; vtc=cSQCCWmh8yGNrOj0ZuyXVg; bstc=cSQCCWmh8yGNrOj0ZuyXVg; _astc=1259da77e80b2d1aa2717e115a650439; adblocked=false; dimensionData=969; pxcts=5515ebf3-a824-11ed-887b-41774f657977; _pxvid=55157565-a824-11ed-887b-41774f657977; _pxff_cfp=1; auth=MTAyOTYyMDE4PIaZyEqM3okL40sNMiONw/eqjYetZHTqplLMMuDutQEJ+P8p0SX+7GVzA8M6UWB9xsPGUHz/dF98VrB+XxgaNP0qywAypinfePoexxrMZ7WaQ0xn5kTinw94dCe9zGfy767wuZloTfhm7Wk2KcjygglTqinKgSpV0hco0QKmh1C5PK6p8/UCgyFvvpNWJcWO4PpR3Qm2b8m9Q8a4Q6eS+90AwvdYFPPCKe7mpM5sMYEUMk70P8glgOEpLOprhDfMDCcb9mgycy9jtT1uIyOBHcAURAMQoFikpd0s+XPz7vs+flIhhiKBBtqdIETugm6iYPjzFIGxQ4stDk4lMK0BhbHoo/LKCo+WRxr1/25iaZ5kAkh3UmFAdmVWhicD5EDFdH0w0Mo4dNWTubnVgvEBz5E5WBBdZBCyKnCQAR7o6eg=; ACID=75ed83f1-9b50-42f8-ba06-34d0ba03404c; hasACID=true; locDataV3=eyJpc0RlZmF1bHRlZCI6dHJ1ZSwiaW50ZW50IjoiU0hJUFBJTkciLCJwaWNrdXAiOlt7ImJ1SWQiOiIwIiwibm9kZUlkIjoiMzA4MSIsImRpc3BsYXlOYW1lIjoiU2FjcmFtZW50byBTdXBlcmNlbnRlciIsIm5vZGVUeXBlIjoiU1RPUkUiLCJhZGRyZXNzIjp7InBvc3RhbENvZGUiOiI5NTgyOSIsImFkZHJlc3NMaW5lMSI6Ijg5MTUgR2VyYmVyIFJvYWQiLCJjaXR5IjoiU2FjcmFtZW50byIsInN0YXRlIjoiQ0EiLCJjb3VudHJ5IjoiVVMiLCJwb3N0YWxDb2RlOSI6Ijk1ODI5LTAwMDAifSwiZ2VvUG9pbnQiOnsibGF0aXR1ZGUiOjM4LjQ4MjY3NywibG9uZ2l0dWRlIjotMTIxLjM2OTAyNn0sImlzR2xhc3NFbmFibGVkIjp0cnVlLCJzY2hlZHVsZWRFbmFibGVkIjp0cnVlLCJ1blNjaGVkdWxlZEVuYWJsZWQiOnRydWUsImh1Yk5vZGVJZCI6IjMwODEiLCJzdG9yZUhycyI6IjA2OjAwLTIzOjAwIiwic3VwcG9ydGVkQWNjZXNzVHlwZXMiOlsiUElDS1VQX0lOU1RPUkUiLCJQSUNLVVBfQ1VSQlNJREUiXX1dLCJzaGlwcGluZ0FkZHJlc3MiOnsibGF0aXR1ZGUiOjM4LjQ4MjY3NywibG9uZ2l0dWRlIjotMTIxLjM2OTAyNiwicG9zdGFsQ29kZSI6Ijk1ODI5IiwiY2l0eSI6IlNhY3JhbWVudG8iLCJzdGF0ZSI6IkNBIiwiY291bnRyeUNvZGUiOiJVUyIsImxvY2F0aW9uQWNjdXJhY3kiOiJsb3ciLCJnaWZ0QWRkcmVzcyI6ZmFsc2V9LCJhc3NvcnRtZW50Ijp7Im5vZGVJZCI6IjMwODEiLCJkaXNwbGF5TmFtZSI6IlNhY3JhbWVudG8gU3VwZXJjZW50ZXIiLCJhY2Nlc3NQb2ludHMiOm51bGwsInN1cHBvcnRlZEFjY2Vzc1R5cGVzIjpbXSwiaW50ZW50IjoiUElDS1VQIiwic2NoZWR1bGVFbmFibGVkIjpmYWxzZX0sImRlbGl2ZXJ5Ijp7ImJ1SWQiOiIwIiwibm9kZUlkIjoiMzA4MSIsImRpc3BsYXlOYW1lIjoiU2FjcmFtZW50byBTdXBlcmNlbnRlciIsIm5vZGVUeXBlIjoiU1RPUkUiLCJhZGRyZXNzIjp7InBvc3RhbENvZGUiOiI5NTgyOSIsImFkZHJlc3NMaW5lMSI6Ijg5MTUgR2VyYmVyIFJvYWQiLCJjaXR5IjoiU2FjcmFtZW50byIsInN0YXRlIjoiQ0EiLCJjb3VudHJ5IjoiVVMiLCJwb3N0YWxDb2RlOSI6Ijk1ODI5LTAwMDAifSwiZ2VvUG9pbnQiOnsibGF0aXR1ZGUiOjM4LjQ4MjY3NywibG9uZ2l0dWRlIjotMTIxLjM2OTAyNn0sImlzR2xhc3NFbmFibGVkIjp0cnVlLCJzY2hlZHVsZWRFbmFibGVkIjp0cnVlLCJ1blNjaGVkdWxlZEVuYWJsZWQiOnRydWUsImFjY2Vzc1BvaW50cyI6W3siYWNjZXNzVHlwZSI6IkRFTElWRVJZX0FERFJFU1MifV0sImh1Yk5vZGVJZCI6IjMwODEiLCJzdXBwb3J0ZWRBY2Nlc3NUeXBlcyI6WyJERUxJVkVSWV9BRERSRVNTIl19LCJpbnN0b3JlIjpmYWxzZSwicmVmcmVzaEF0IjoxNjc1OTMyNTUyNjEwLCJ2YWxpZGF0ZUtleSI6InByb2Q6djI6NzVlZDgzZjEtOWI1MC00MmY4LWJhMDYtMzRkMGJhMDM0MDRjIn0=; assortmentStoreId=3081; hasLocData=1; locGuestData=eyJpbnRlbnQiOiJTSElQUElORyIsInN0b3JlSW50ZW50IjoiUElDS1VQIiwibWVyZ2VGbGFnIjpmYWxzZSwiaXNEZWZhdWx0ZWQiOnRydWUsInN0b3JlU2VsZWN0aW9uVHlwZSI6IkRFRkFVTFRFRCIsInBpY2t1cCI6eyJub2RlSWQiOiIzMDgxIiwidGltZXN0YW1wIjoxNjc1OTEwOTUyNTk0fSwic2hpcHBpbmdBZGRyZXNzIjp7ImlkIjpudWxsLCJ0aW1lc3RhbXAiOjE2NzU5MTA5NTI1OTQsImNyZWF0ZVRpbWVzdGFtcCI6bnVsbCwidHlwZSI6InBhcnRpYWwtbG9jYXRpb24iLCJnaWZ0QWRkcmVzcyI6ZmFsc2UsInBvc3RhbENvZGUiOiI5NTgyOSIsImNpdHkiOiJTYWNyYW1lbnRvIiwic3RhdGUiOiJDQSIsImRlbGl2ZXJ5U3RvcmVMaXN0IjpbeyJub2RlSWQiOiIzMDgxIiwidHlwZSI6IkRFTElWRVJZIn1dfSwicG9zdGFsQ29kZSI6eyJ0aW1lc3RhbXAiOjE2NzU5MTA5NTI1OTQsImJhc2UiOiI5NTgyOSJ9LCJtcCI6W10sInZhbGlkYXRlS2V5IjoicHJvZDp2Mjo3NWVkODNmMS05YjUwLTQyZjgtYmEwNi0zNGQwYmEwMzQwNGMifQ==; TB_Latency_Tracker_100=1; TB_Navigation_Preload_01=1; TB_SFOU-100=; mobileweb=0; xpth=x-o-mart+B2C~x-o-mverified+false; xpa=-7Lfp|14us3|1m0dF|1nWDp|2xWuI|3AZCz|3IsSY|4WnNc|4sTVz|5a1kK|5naDk|83J85|8J6Zl|Amg8a|D8jju|DSZXu|Eq7vl|FPyei|FVa_h|GK20V|IM26Z|N0ZXc|SglEw|UUnt1|V9HWe|XUHzs|guSMV|hLkLm|huxun|j8K4O|mwK0m|nbZv8|o12zp|oZgq1|p5lYO|t77zC|uTxgM|vHnsu|vq9e-|w9B7l|xig4c; exp-ck=1m0dF11nWDp13IsSY14WnNc14sTVz1D8jju1DSZXu4Eq7vl1FPyei2IM26Z3N0ZXc2UUnt12V9HWe1j8K4O1mwK0m3nbZv81o12zp1oZgq11p5lYO1uTxgM1w9B7l2xig4c1; _pxhd=e29fc324dd9ce1966432eaaf7c7c9d388a929a397b2aa899913138108dacb0b1:55778cb9-a824-11ed-8c32-6f4b6a766b74; akavpau_p2=1675911553~id=3376534d74e94aa2e7f5db74c271645a; bm_mi=955D49830B1F35C0F9696AA1859CBB9E~YAAQLJHIFyQKASeGAQAA5bkTNBKlYf6NKXEhfibnVAoA/bcWljK59JTjfPP2qCNxO8Cp5+Kb8+H6iOoWC8FOgEcAoa/gw8BQAvb7dJ9alRMwwOObsfKXKGXYQQDqs10wok/xiI9tyFSW3MWLO9SDcU7yt8Uaccv7K1UATVzTsflLfp9gPUmjZNW2a148FGcYvetzRpQlClnx4VBT/2NdoBcBpZc/Z7EWZnXLAQauAFstciXLsgsBsBxbT/TZui4kwJxkaTCmkmLoDddpB+z4cEbzrWpHPOGCnGSWqurLIvtrJPK5rluqdTiaCfxN/Q==~1; xptc=assortmentStoreId+3081; xpm=1+1675910955+cSQCCWmh8yGNrOj0ZuyXVg~+0; TS012768cf=01eb65a76e9d31a3a6260263ddef25ed5b56efce4fc45fc100dd5006fcbe43206f2b692245bd08af77b6aa7cbdbf1affda7f804971; TS01a90220=01eb65a76e9d31a3a6260263ddef25ed5b56efce4fc45fc100dd5006fcbe43206f2b692245bd08af77b6aa7cbdbf1affda7f804971; _px3=db7a8ab7161bfed73289019de01b821c28b1a93806f324196c384ae380f1a51f:zW9u7PLqp9V42CNg5db/SIda4Lahymcefwh05me/U2e+eCxtLluCEniarrsG5Z6dluQoGusg8P6m2o9XKh839A==:1000:I2637kzTbOEw2hd2wPO8QNoSRVZcfvD5oeQZGfkJaFxjsdqgGRxUpH1SvPErT3eeYcHIj+lNCvyzC2r6gxn89Hyly+yYM6VePfszdoRjWvEUAphSKE0NGBXbQUeY33IHMvpzMZ6QcdnFUKKlWKPZtJesyszcu4Cc+Dcr+HGs2ueXNyrLRHn5iWXITV/ecjgJM52hJ7qpd+aSN9sTFph5XQ==; xptwg=2655821577:1FA453F25076610:51173E5:6DE59E89:1392C881:C0DB775F:; TS2a5e0c5c027=083cd933a5ab20002910f517e79f898cd1132de31b8513dc1fb7f791a84a8866aa1c256e1f8afb0308af2ca2ca1130005b55f2fd82abfbd5177a6d02dff4fc41eaf42678e7dab44c643f4155019667cd765672dc86e6ad43f2f18a7b2bb7f8ba; bm_sv=1E848668C6A8D8F16D5AB806E484BB35~YAAQLJHIFzIKASeGAQAA4skTNBLw7tH9IfaeFc3VuA+78UMBFPi1PsNSv2Rd6skFN2mALKsBvCWMIM7WKHIFrf3SsYLveXEDRbR8XIYE+yA6E18w3ufidFEXoMslRbsfzMj35uQBxVWOoX3egwUrervyXBbxJpra1lMPzFIZrtBUiyDDhlSoH2km1jMMlUwuam61jSYhZCB/V10JvaH4+l+TVw6w5DcTx30wPB3F5wxr/BCNWFoRLKJ3nyixpGLi4Q==~1',
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
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44',
}

# 日志文件前缀
logging_path = os.getcwd() + '.log'
# 设置日志级别
logging = logging_util.LoggingUtil("INFO", logging_path).get_logging()


def get_ip_pool():
    """
    获取IP代理池
    :param
    :return:
    """
    logging.info('获取IP代理，搭建代理IP池')
    ips = requests.get(proxy_url)
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


def get_all_url(url_r):
    """
    爬取初始url页面中所有的产品url
    :param url_r: 初始url
    :return:product_list: 所有产品url
    """
    product_list = []
    product_list.append(['1103217313', ''])
    # *******************自动版*************************
    # proxies = {'http': get_random_ip()}
    # resp = requests.get(url_r, headers=headers, proxies=proxies, timeout=5)
    # text = resp.content.decode('utf-8')
    # *************************************************

    # *******************手动版*************************
    # h1和h2是手动下载的html页面
    # html = etree.HTML(h1)
    # item_ids = html.xpath('//*[@id="maincontent"]//div[@data-item-id]')
    # for ii in item_ids:
    #     link_ids = ii.xpath('./a/@link-identifier')
    #     ad_tags = ii.xpath(
    #         './div[@data-testid="list-view"]//div[@class="flex items-center lh-title h2-l normal"]/span/text()'
    #     )
    #     product_list.append([''.join(link_ids), ''.join(ad_tags)])
    # html = etree.HTML(h2)
    # item_ids = html.xpath('//*[@id="maincontent"]//div[@data-item-id]')
    # for ii in item_ids:
    #     link_ids = ii.xpath('./a/@link-identifier')
    #     ad_tags = ii.xpath(
    #         './div[@data-testid="list-view"]//div[@class="flex items-center lh-title h2-l normal"]/span/text()'
    #     )
    #     product_list.append([''.join(link_ids), ''.join(ad_tags)])
    logging.info('爬取首页成功，获取目标url共' + str(len(product_list)) + '个')
    return product_list


def get_product_detail_by_script(product_list):
    """
    获取产品url，通过正则方式解析script，爬取产品url中的产品信息
    :param product_list: 所有产品url的列表
    :return:df_result 详情页信息明细
    """
    df_result = pd.DataFrame(columns=('item_id', 'product_url', 'title', 'catalog_full', 'brand', 'price',
                                      'seller_name', 'proseller_tag', 'variant', 'shipping_method', 'shortDescription',
                                      'longDescription', 'specification', 'warranty',
                                      'reviews', 'stars', 'one_star_reviews', 'two_star_reviews', 'three_star_reviews',
                                      'four_star_reviews', 'five_star_reviews', 'first_review_date')
                             )
    count = 0
    for pl in product_list:
        count += 1
        if count >= 5:
            return df_result
        product_url = 'https://www.walmart.com/ip/' + pl[0]
        logging.info('开始解析产品详情页，解析url ' + product_url)
        # 获取随机代理IP和随机cookie
        # proxies = {'http': get_random_ip()}
        # cookies = walmart_cookie_generate.get_random_cookie()
        # resp = requests.get(product_url, headers=headers, proxies=proxies, cookies=cookies, timeout=5)

        # if resp.status_code == 200:
        if 1 == 1:
            # text = resp.content.decode('utf-8')
            # if 'Robot or human' in text:
            #     logging.info('被反爬了，退出')
            #     continue
            # if 'Pro Seller' in text:
            #     is_proseller = '是'
            # else:
            #     is_proseller = '否'
            # html = etree.HTML(text)
            # json_data = html.xpath('//script[@type="application/json"]/text()')[0]
            # json_text = json.loads(json_data)

            with open('D:\pythonProject\walmart_crawl\html_file\product_detail.json', encoding='UTF-8') as f:
                json_text = json.load(f)


            product_detail = json_text['props']['pageProps']['initialData']['data']
            is_proseller = '否'
            # 品牌
            brand = product_detail['product']['brand']
            # 产品链接
            product_url = product_detail['product']['canonicalUrl']
            # 长描述
            longDescription = product_detail['idml']['longDescription']
            # 短描述
            shortDescription = product_detail['idml']['shortDescription']
            # 产品规范 specification
            specification = product_detail['idml']['specifications']
            specification_text = ''
            for sc in specification:
                for v in sc.values():
                    specification_text = specification_text + '\n' + v
            # 产品保修 Warranty
            warranty = product_detail['idml']['warranty']['information']
            # 标题
            title = product_detail['product']['name']
            # 产品价格
            price = product_detail['product']['priceInfo']['currentPrice']['priceString']
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

            temp_dict = {
                'item_id': item_id,
                'product_url': 'www.walmart.com' + product_url,
                # 'ad_tag': ad_tag,
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
                # 'first_review_date': first_review_date,
            }
            # 把爬取结果插入到dataframe最后一行
            df_result.loc[len(df_result)] = temp_dict
        return df_result


def get_product_detail(product_list):
    """
    获取产品url，爬取产品url中的产品信息
    :param product_list: 所有产品url的列表
    :return:df_result 详情页信息明细
    """

    # 构造一个datafrome用于存储结果数据
    df_result = pd.DataFrame(columns=('link_id', 'product_url', 'ad_tag', 'title', 'catalog_full', 'brand', 'price',
                                      'proseller_tag', 'variant', 'variant', 'fullfill_type', 'description', 'reviews',
                                      'stars', 'one_star_reviews', 'two_star_reviews', 'three_star_reviews',
                                      'four_star_reviews', 'five_star_reviews', 'first_review_date')
                             )
    count = 0
    for pl in product_list:
        count += 1
        if count >= 5:
            return df_result
        product_url = 'https://www.walmart.com/ip/' + pl[0]
        logging.info('开始解析产品详情页，解析url ' + product_url)
        proxies = {'http': get_random_ip()}
        cookies = walmart_cookie_generate.get_random_cookie()
        resp = requests.get(product_url, headers=headers, proxies=proxies, cookies=cookies, timeout=5)
        if resp.status_code == 200:
            text = resp.content.decode('utf-8')
            if 'Robot or human' in text:
                logging.info('被反爬了，退出')
                continue
            html = etree.HTML(text)
            print(text)
            # 广告标记
            ad_tag = 'none' if len(pl[1]) == 0 else pl[1]
            print('广告标记: ' + ad_tag)
            # 标题
            title = html.xpath('//h1[@itemprop="name"]/text()')
            print('标题: ' + ''.join(title))
            # 品类路径
            cats = html.xpath('//a[@itemprop="item"]/span//text()')
            cat_full = ''
            for cat in cats:
                cat_full = cat_full + cat
            print('类目路径： ' + cat_full)
            # 品牌
            brand = html.xpath('//a[contains(@href,"/c/brand/")]/text()')
            print('品牌： ' + ''.join(brand))
            # 价格
            prices = html.xpath('//span[@data-testid="price-wrap"]//span/text()')
            price = ''
            for p in prices:
                price = price + ' ' + p
            print('价格： ' + price.strip())
            # 是否pro seller
            proseller_tag = '否'
            if 'Pro Seller' in h3:
                proseller_tag = '是'
            print('是否pro seller: ' + proseller_tag)
            # 变体
            variant = html.xpath('//div[@role="list"]/div[@role="listitem"]//span[@class="w_iUH7"]/text()')
            print(variant)
            # 发货方式
            seller_types = html.xpath('//span[@class="lh-title"]/div//text()')
            seller_type = 'Sold by Seller'
            fullfill_type = 'FBM'
            for st in seller_types:
                if 'Walmart.com' in st:
                    seller_type = 'Sold by Walmart'
                    fullfill_type = 'WFS'
                if 'Fulfilled by' in st:
                    fullfill_type = 'WFS'
            print('卖家方式： ' + seller_type)
            print('发货方式： ' +fullfill_type)
            # 产品描述
            descriptions = html.xpath('//*[@data-testid="product-description"]//text()')
            description = ''
            for de in descriptions:
                if len(de) > 0:
                    description = description + '\n' + de
            print('产品描述： ' + description.strip())
            # 评论数
            reviews = html.xpath('//a[@link-identifier="reviewsLink"]/text()')
            # 星级
            stars = html.xpath('//div[@data-testid="reviews-and-ratings"]//span[contains(@class,"rating-number")]/text()')
            print('评论数： ' + ''.join(reviews).split(' ')[0])
            print('星级： ' + ''.join(stars).replace('(', '').replace(')', ''))
            # 5星评论数
            five_star_reviews = html.xpath('//div[@id="item-review-section"]/div/div/ol/li[1]//span[@class="w3 tc"]/text()')
            four_star_reviews = html.xpath('//div[@id="item-review-section"]/div/div/ol/li[2]//span[@class="w3 tc"]/text()')
            three_star_reviews = html.xpath('//div[@id="item-review-section"]/div/div/ol/li[3]//span[@class="w3 tc"]/text()')
            two_star_reviews = html.xpath('//div[@id="item-review-section"]/div/div/ol/li[4]//span[@class="w3 tc"]/text()')
            one_star_reviews = html.xpath('//div[@id="item-review-section"]/div/div/ol/li[5]//span[@class="w3 tc"]/text()')
            print('五星： ' + ''.join(five_star_reviews))
            print('四星： ' + ''.join(four_star_reviews))
            print('三星： ' + ''.join(three_star_reviews))
            print('二星： ' + ''.join(two_star_reviews))
            print('一星： ' + ''.join(one_star_reviews))
            # 上架时间（最早评论时间）
            first_review_date = ''
            review_url = 'https://www.walmart.com/reviews/product/{}?sort=submission-asc'.format(pl[0])
            proxies = {'http': get_random_ip()}
            logging.info('开始解析产品评论页，解析url ' + review_url)
            # 暂停2秒，访问评论页
            time.sleep(2)
            resp = requests.get(review_url, headers=headers, proxies=proxies, timeout=5)
            if resp.status_code == 200:
                try:
                    text = resp.content.decode('utf-8')
                    # print(text)
                    html = etree.HTML(text)
                    first_review_date = html.xpath('//main[@role="main"]//li[contains(@style,"translate3d")][1]//div[@class="f7 gray"]/text()')
                except:
                    first_review_date = 'none'
            print(first_review_date)

            temp_dict = {
                'link_id': pl[0],
                'product_url': product_url,
                'ad_tag': ad_tag,
                'title': ''.join(title).strip(),
                'catalog_full': cat_full,
                'brand': ''.join(brand),
                'price': price.strip(),
                'proseller_tag': proseller_tag,
                'variant': variant,
                'seller_type': seller_type,
                'fullfill_type': fullfill_type,
                'description': description.strip(),
                'reviews': ''.join(reviews).split(' ')[0],
                'stars': ''.join(stars).replace('(', '').replace(')', ''),
                'one_star_reviews': ''.join(one_star_reviews),
                'two_star_reviews': ''.join(two_star_reviews),
                'three_star_reviews': ''.join(three_star_reviews),
                'four_star_reviews': ''.join(four_star_reviews),
                'five_star_reviews': ''.join(five_star_reviews),
                'first_review_date': first_review_date,
            }
            # 把爬取结果插入到dataframe最后一行
            df_result.loc[len(df_result)] = temp_dict
        # 涉及解析页面延迟3秒
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


def run(url_f, key_word):
    """
    程序运行本体
    :param url_f: 网址前缀
    :param key_word: 查询的关键词
    :return:
    """
    get_ip_pool()
    logging.info('开始otto爬取。初始url: ' + url_f + ' 关键词： ' + key_word)
    df = get_product_detail_by_script(get_all_url(url_f))
    print(df)
    save_to_csv(df, key_word)


if __name__ == '__main__':
    # 初始网页前缀
    url_front = 'https://www.walmart.com/browse/baby/double-strollers/5427_118134_1101428'
    # 搜索关键词
    ky = 'Double Strollers'
    # 传入网址和关键词，开始爬取
    run(url_front, ky)
