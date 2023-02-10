import random
import os
# import ja3
# import proxy
from selenium import webdriver
import time
import json
from util import logging_util
from util.setting import REDIS_CLIENT, WALMART_COOKIE_KEY

# 日志文件前缀
logging_path = os.getcwd() + '.log'
# 设置日志级别
logging = logging_util.LoggingUtil("INFO", logging_path).get_logging()

headers = {
    'authority': 'www.walmart.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'service-worker-navigation-preload': 'true',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.walmart.com',
}


# 获取配置
# redis_client = walmart_spider_conf.redis_client
# walmart_cookies_key = walmart_spider_conf.walmart_cookies_key


def get_random_cookie():
    # 随机提起cookie
    avail_cookie = REDIS_CLIENT.llen(WALMART_COOKIE_KEY)
    if avail_cookie == 0:
        logging.error("已经没有可用cookie")
        exit()
        logging.info('获取一个随机cookie')
    num = random.choice(list(range(avail_cookie)))
    cookies = json.loads(REDIS_CLIENT.lrange(WALMART_COOKIE_KEY, num, num)[0])
    return cookies


# def spider(url, proxy_ip):
#     """
#     沃尔玛通用请求发起模块
#     :param url: 请求地址
#     :param proxy_ip: 代理ip
#     :return: response
#     """
#     logging.info("开始准备请求")
#     cookies = get_random_cookie()
#     s = requests.session()
#     s.keep_alive = False
#     s.mount(url, ja3.DESAdapter())
#     try:
#         response = s.get(url, headers=headers, cookies=cookies, proxies=proxy_ip, timeout=10)
#         logging.info("数据返回成功")
#     except Exception as e:
#         logging.error("请求出现异常,准备重试")
#         time.sleep(1)
#         proxy_ip = proxy.get_proxies()
#         response = spider(url, proxy_ip)
#     if "Activate and hold the button to confirm that you’re human" in response.text:
#         logging.error("出现验证码,移除当前所使用的cookie并开始重试")
#         redis_client.lrem(walmart_cookies_key, 0, json.dumps(cookies))
#         time.sleep(1)
#         proxy_ip = proxy.get_proxies()
#         response = spider(url, proxy_ip)
#     return response
#
#
# def url_handler(url):
#     """
#     处理部分截取的链接不含域名部分的数据
#     :param url: url地址
#     :return: 完整沃尔玛url
#     """
#     url = str(url)
#     if not url.startswith("https") and url != 'nan' and url.strip() != "":
#         url = "https://www.walmart.com" + url
#     return url


def chrome_conifg():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1280x1024')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    return chrome_options


def clean_cookie():
    """
    清理掉redis当中原有的cookie
    :return:
    """
    logging.info("清空redis中所有cookie")
    # 清除表中历史cookie
    REDIS_CLIENT.delete(WALMART_COOKIE_KEY)


def cookie_produce():
    """
    使用seleliumn生成一个可用的walmart cookie
    存放至redis
    :return:
    """
    chrome_options = chrome_conifg()
    driver = webdriver.Chrome(options=chrome_options)
    # 防止被监测,覆盖浏览器指纹
    with open('util/stealth.min.js') as f:
        js = f.read()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    url = 'https://www.walmart.com'
    driver.get(url)
    cookie = driver.get_cookies()
    cookies = {}
    for i in cookie:
        cookies[i["name"]] = i["value"]
    time.sleep(10)
    logging.info(cookies)
    if "Activate and hold the button to confirm that you’re human" in driver.page_source:
        print("验证码")
        time.sleep(100000)
    else:
        REDIS_CLIENT.lpush(WALMART_COOKIE_KEY, json.dumps(cookies))
    # with open('creat_cookie', 'w+', encoding='utf-8') as f:
    #     f.write(driver.page_source)
    driver.quit()


if __name__ == '__main__':
    clean_cookie()
    cookie_num = REDIS_CLIENT.llen(WALMART_COOKIE_KEY)
    cookie_need = 3
    logging.info('当前cookie池一共有{}个cookie'.format(cookie_num))
    logging.info('仍需要生成{}个cookie'.format(cookie_need - cookie_num))
    for i in range(cookie_need - cookie_num):
        logging.info('正在生成第{}个cookie'.format(i+1))
        cookie_produce()
