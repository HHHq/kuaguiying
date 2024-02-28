import requests
import logging


def visit(method, url, params=None, data=None, json=None, **kwargs):
    res = requests.request(method, url, params=params, data=data, json=json, **kwargs)
    try:
        return res.json()
    except Exception as e:
        logging.error('返回数据不是json格式:{}'.format(e))
        return None


