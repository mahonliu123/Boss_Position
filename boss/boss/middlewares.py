# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import requests
from scrapy import signals
import random
import time
from selenium import webdriver
import pyautogui as pg
from .settings import USER_AGENT_LIST, PROXY_LIST

# 若要爬取大量数据，需要使用代理IP，否则会被封IP24小时
class RandomProxies(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXY_LIST)
        request.meta['proxy'] = proxy
        return None

# 设置User-Agent
class RandomUserAgent(object):
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = ua
        return None

class BossDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.


    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # 设置headers，cookies
        cookie_url = 'https://www.zhipin.com/?ka=header-home'
        headers = {
            'referer': 'https://www.zhipin.com/c100010000-p100901/?ka=sel-city-100010000',
        }
        r = requests.get(url=cookie_url, headers=headers)
        cookie = dict(r.cookies)
        request.headers['referer'] = 'https://www.zhipin.com/c100010000-p100901/?ka=sel-city-100010000'
        request.headers['cookies'] = cookie
        # 爬一定数量后会重定向至滑块验证页面
        # 判断是否重定向，若重定向则使用selenium
        # 通过测试发现使用selenium锁定元素会触发反爬机制
        # 所以使用开发者模式并且计算出滑块的位置
        # 使用pyautogui这个库来控制鼠标拖动滑块
        if 'verify' in request.url:
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches',
                                            ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
            options.add_argument('--log-level=3')
            browser = webdriver.Chrome(options=options)
            browser.get('https://www.zhipin.com/')
            time.sleep(2)
            pg.moveTo(100, 410)
            pg.click()
            time.sleep(2)
            pg.moveTo(200, 580)
            pg.dragTo(440, 580, duration=2)
            time.sleep(2)
            browser.close()
        return None

    def process_response(self, request, response, spider):

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
