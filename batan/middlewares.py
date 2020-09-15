# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import scrapy
from scrapy import signals
from scrapy.utils.project import get_project_settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities

import platform
import os
import time
from scrapy.http import Request
from batan.request import ClickAccess, ClickRequest, ChromeAccess, ChromeRequest

settings = get_project_settings().copy()


class BatanSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BatanDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        print('----------------->', type(request))
        # 点击访问
        if isinstance(request, ClickRequest):
            return ClickAccess(request=request, config=spider.config, webdriver=spider.driver,
                               spider=spider, access_xpath=request.access_xpath)()
        # 浏览器访问
        if isinstance(request, ChromeRequest):
            return ChromeAccess(request=request, webdriver=spider.driver)()
        # 默认访问
        if isinstance(request, Request):
            pass
        return None

    def process_response(self, request, response, spider):
        # print('next----------------------->')
        # if spider.config['next']:
        #     element = spider.driver.find_element_by_xpath(spider.config['next'])
        #     element.click()
        #     html = spider.driver.page_source
        #
        #     return scrapy.http.HtmlResponse(
        #         url=request.url,
        #         body=html.encode('utf-8'),
        #         encoding='utf-8',
        #         request=request
        #     )
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# class BatanDownloaderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the downloader middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_request(self, request, spider):
#         if spider.config['selenium']:
#             spider.driver.get(request.url)
#             html = spider.driver.page_source
#
#             return scrapy.http.HtmlResponse(
#                 url=request.url,
#                 body=html.encode('utf-8'),
#                 encoding='utf-8',
#                 request=request
#             )
#         return None
#
#     def process_response(self, request, response, spider):
#         # print('next----------------------->')
#         # if spider.config['next']:
#         #     element = spider.driver.find_element_by_xpath(spider.config['next'])
#         #     element.click()
#         #     html = spider.driver.page_source
#         #
#         #     return scrapy.http.HtmlResponse(
#         #         url=request.url,
#         #         body=html.encode('utf-8'),
#         #         encoding='utf-8',
#         #         request=request
#         #     )
#         return response
#
#     def process_exception(self, request, exception, spider):
#         pass
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)
