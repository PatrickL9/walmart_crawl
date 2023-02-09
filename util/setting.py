import json
import random

import redis

# redis_client = redis.StrictRedis(decode_responses=True)
REDIS_CLIENT = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
WALMART_COOKIE_KEY = "walmart_cookies"
# walmart_cate_start_key = 'wal_start_cate_url'

# avail_cookie = REDIS_CLIENT.llen(WALMART_COOKIE_KEY)
# print('WALMART_COOKIE_KEY 一共有{}个'.format(avail_cookie))
# print('WALMART_COOKIE_KEY的内容如下：')
# print(REDIS_CLIENT.lrange(WALMART_COOKIE_KEY, 0, -1))

