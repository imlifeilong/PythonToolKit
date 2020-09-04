from scrapy import signals
import scrapy
import re
from batan.libs import parse_config
from batan.libs import BatanItemLoader
from batan.request import ClickRequest, ChromeRequest
from batan.webdriver import WebDriver


class YunNanShuiLiSpider(scrapy.Spider):
    name = 'YunNanShuiLiSpider'
    config = {}

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        crawler.signals.connect(spider.open_spider, signals.spider_opened)
        crawler.signals.connect(spider.close_spider, signals.spider_closed)
        return spider

    def open_spider(self):
        self.driver = WebDriver(self.crawler.settings)()

    def close_spider(self):
        self.driver.close()
        self.driver.quit()
        self.driver = None

    def start_requests(self):
        urls = [
            'http://ynxy.cwun.org/UnitInfoMore.aspx?type=1',
            'http://ynxy.cwun.org/UnitInfoMore.aspx?type=2',
            'http://ynxy.cwun.org/UnitInfoMore.aspx?type=3',
            'http://ynxy.cwun.org/UnitInfoMore.aspx?type=4',
            'http://ynxy.cwun.org/UnitInfoMore.aspx?type=5',
            'http://ynxy.cwun.org/UnitInfoMore.aspx?type=6',
            'http://ynxy.cwun.org/UnitInfoMore.aspx?type=7',
            'http://ynxy.cwun.org/UnitInfoMore.aspx?type=8',
            'http://ynxy.cwun.org/UnitInfoMore.aspx?type=9',
            'http://ynxy.cwun.org/UnitInfoMore.aspx?type=10',
        ]
        for u in urls:
            yield ChromeRequest(url=u, dont_filter=True)

    def parse(self, response):
        print('===========================>', response)
        yield from self.parse_list(response)
        yield from self.parse_next(response)

    def parse_list(self, response):
        for row in response.xpath('//table[@id="ContentPlaceHolder1_GridViewUnitInfo"]//tbody//tr[position()>1]'):
            loader = BatanItemLoader(selector=row, response=response)
            loader.add_xpath('name', './/td[2]//div//a/text()')
            item = loader.load_item()
            item['source'] = self.name
            item['area'] = '云南省'
            print('----------------->', item)
            yield item

    def parse_next(self, response):
        _next = response.xpath('//a[contains(text(), "下一页")]')
        if _next:
            self.config['next'] = '//a[contains(text(), "下一页")]'
            yield from self.parse_next_click(response)

    def parse_next_click(self, response):
        '''点击下一页'''

        yield ClickRequest(response.url, dont_filter=True)
