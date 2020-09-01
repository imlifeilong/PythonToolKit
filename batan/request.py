import scrapy
import time
import random
import re


# 重写Request添加方式
class ClickRequest(scrapy.Request):
    def __init__(self, url, **kwargs):
        # 继承父类
        super(ClickRequest, self).__init__(url, **kwargs)


class ClickAccess(object):
    '''点击访问'''

    def __init__(self, request, config, webdriver, **kwargs):
        self.config = config
        self.webdriver = webdriver
        self.request = request
        self.spider = kwargs.get('spider')

    def __call__(self, *args, **kwargs):
        element = self.webdriver.find_element_by_xpath(self.config['next'])
        print(element, self.config['next'])
        element.click()
        # 延时
        time.sleep(random.random() * 0.9)

        return scrapy.http.HtmlResponse(
            url=self.webdriver.current_url,
            body=self.webdriver.page_source.encode('utf-8'),
            encoding='utf-8',
            request=self.request
        )
        #     self.spider.crawler.engine.close_spider(self.spider, '爬取完成：%s ' % self.config['name'])


# 重写Request添加方式
class ChromeRequest(scrapy.Request):
    def __init__(self, url, **kwargs):
        # 继承父类
        super(ChromeRequest, self).__init__(url, **kwargs)


class ChromeAccess(object):
    '''浏览器访问'''

    def __init__(self, request, webdriver):
        self.webdriver = webdriver
        self.request = request
        # self.url = url

    def __call__(self, *args, **kwargs):
        # url = self.url if self.url else self.request.url
        self.webdriver.get(self.request.url)
        # 延时
        time.sleep(random.random() * 0.9)
        return scrapy.http.HtmlResponse(
            url=self.request.url,
            body=self.webdriver.page_source.encode('utf-8'),
            encoding='utf-8',
            request=self.request
        )
