from datetime import time
import requests
from requests import ConnectionError
from .proxypool import get_proxy

class Status:
    NEW = 0
    COMPLETE = 100
    PAUSE = 101
    STOP = 102
    FAILED = 999


class Spider:
    def __init__(self, start_url, name=None, start_time=None, end_time=None, use_proxy=False):
        self.name = name or __class__.__name__
        self.proxy = get_proxy() if use_proxy else None
        self.start_url = start_url
        self.current_url = start_url
        self.his_url = []
        self.start_time = start_time or time(hour=9)
        self.end_time = end_time or time(hour=18)
        self.status = Status.NEW
        self.max_retry = 5

        # record the error
        self.error = None

    def __repr__(self):
        return '<Spider object at {}>'.format(hex(id(self)))

    def _get_page(self, url, retry=0):
        if retry >= self.max_retry:
            return
        headers = {}
        try:
            if self.proxy:
                proxies = {'http': 'http://' + self.proxy}
                res = requests.get(url, headers=headers, proxies=proxies)
            else:
                res = requests.get(url, headers=headers)
            if res.status_code == 200:
                return res
        except ConnectionError as e:
            self.error = e
        # increase retry count
        retry += 1
        self._get_page(url, retry)

    def start(self):
        self.on_start()

    def on_start(self):
        self.crawl(self.start_url, callback=self.index_page)

    def on_result(self, result):
        raise NotImplementedError

    def crawl(self, url, callback):
        print('{} {}'.format(callback.__name__, url))
        self.current_url = url
        self.his_url.append(url)
        res = self._get_page(url)
        if res:
            result = callback(res)
            if result:
                self.on_result(result)

    def index_page(self, response):
        raise NotImplementedError

    def detail_page(self, response):
        raise NotImplementedError
