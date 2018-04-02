#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/2 0002 下午 8:26
 @Author  : jyq
 @Software: PyCharm
 @Description:
"""

import requests

from lib.utils.logger_utils import logger
from task import celery
from task.fetch_review import fetch_review
from task.fetch_pro import fetch_pro
from task.func import get_joom_token
import ujson as json


@celery.task(ignore_result=True)
def fetch_cate_pro(token, cate_id, off=0):
    url = 'https://api.joom.com/1.1/search/products?language=en-US&currency=USD'
    params = {
        'count': 50,
        'pageToken': 'off:%s' % off,
        'filters': [{
            'id': 'categoryId',
            'value': {
                'type': 'categories',
                'items': [{
                    'id': cate_id
                }]
            }
        }]
    }
    logger.info(u"正在抓取分类%s下第%s-%s个产品" % (cate_id, off, off + 50))
    res = requests.post(url, data=json.dumps(params), headers={
        "authorization": token,
        "content-type": 'application/json'
    })
    if "unauthorized" in res.content:
        token = get_joom_token()
        fetch_cate_pro.delay(token, cate_id, off)
        return

    content = json.loads(res.content)
    items = content["payload"]["items"]
    if len(items) == 0:
        logger.info(u"分类%s抓取完成" % cate_id)
    else:
        for item in items:
            logger.info(u'产品id为%s' % item["id"])
            fetch_pro.delay(item["id"], token)
            fetch_review.delay(item["id"], token)
        fetch_cate_pro.delay(token, cate_id, off+50)

