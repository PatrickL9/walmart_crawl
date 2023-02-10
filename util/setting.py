import json
import random
import redis

# 代理API
PROXY_URL = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=460e34f07cf041899a22e79353081288&orderno=YZ2021112078186AsWJy&returnType=1&count=1'
ipPool = []

# 主站点链接
main_url = 'https://www.walmart.com/ip/'
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
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44',
}

success_id = ['948851967',
              '733392547',
              '1279130678',
              '796578533',
              '36491106',
              '555621168',
              '55047751',
              '869330315',
              '793582474',
              '1619305148',
              '972739335',
              '1399600991',
              '991543721',
              '34426669',
              '963539816',
              '291073014',
              '950579789',
              '818943344',
              '591001465',
              '841961195',
              '1511273728',
              '515120494',
              '1171898558',
              '21192349',
              '257644953',
              '36728078',
              '875465827',
              '5673409',
              '314651644',
              '818333505',
              '47507975',
              '127954425',
              '424481600',
              '896228937',
              '119711814',
              '245880436',
              '245889732',
              '43347768',
              '55583249',
              '838403477',
              '55583247',
              '184901237',
              '488367961',
              '335199428',
              '253957599',
              '522935881',
              '825979444',
              '164481787',
              '814985930',
              '515925965',
              '690527281',
              '800740822',
              '708601032',
              '402543556',
              '571221523',
              '50861978',
              '998281468',
              '356881870',
              '687749368',
              '280570803',
              '53733844',
              '44724103',
              '265007415',
              '346390193',
              '44012326',
              '202351979',
              '563747682',
              '1114304819',
              '611571401',
              '894736079',
              '1014397699',
              '828252535',
              '579610035',
              '43347804',
              '2602486506',
              '55047744',
              '314996259',
              '621061787',
              '876927002',
              '1216362458',
              '51576793',
              '480547248',
              '51576894',
              '729767959',
              '36728079'
              ]

REDIS_CLIENT = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
WALMART_COOKIE_KEY = "walmart_cookies"
# walmart_cate_start_key = 'wal_start_cate_url'

avail_cookie = REDIS_CLIENT.llen(WALMART_COOKIE_KEY)
# print('WALMART_COOKIE_KEY 一共有{}个'.format(avail_cookie))
# print('WALMART_COOKIE_KEY的内容如下：')
# print(REDIS_CLIENT.lrange(WALMART_COOKIE_KEY, 0, -1))

