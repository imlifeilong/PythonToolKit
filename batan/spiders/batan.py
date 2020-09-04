from scrapy import signals
import scrapy
import re
from batan.libs import parse_config
from batan.libs import BatanItemLoader
from batan.request import ClickRequest, ChromeRequest
from batan.webdriver import WebDriver


class BaseSpider(scrapy.Spider):
    driver = None
    # chromedriver = None
    # pages = None
    name = None

    def __init__(self, name=None):
        super().__init__(name)
        self.config = parse_config(self.name)
        self.name = self.config['spider']
        print(self.config)
        if self.config['selenium']:
            self._request = ChromeRequest
        else:
            self._request = scrapy.Request

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
        # self.chromedriver = None

    def start_requests(self):
        self.start_urls = self.config['start_urls']
        if self.start_urls:
            yield self._request(url=self.start_urls, dont_filter=True)

    def parse(self, response):
        print('--------------->', response.text)

        yield from self.parse_list(response)
        yield from self.parse_next(response)

    def parse_list(self, response):

        for row in response.xpath(self.config['list']):
            loader = BatanItemLoader(selector=row, response=response)
            for key, value in self.config['item'].items():
                loader.add_xpath(key, value)
            item = loader.load_item()
            item['source'] = self.name
            item['area'] = self.config['area']
            print('----------------->', item)
            yield item

    def _total_pages(self, response):
        '''获取总页数'''
        tmp = None
        if not self.config['pages']: return 0
        if 'pages_type' in self.config and self.config['pages_type'].startswith('string'):
            tmp = response.xpath(self.config['pages']).extract_first()
        else:
            tmp = self.driver.find_element_by_xpath(self.config['pages']).text
        if tmp and isinstance(tmp, str):
            pages = re.findall('\d+', tmp)
            return int(pages[0]) if pages else 0
        else:
            return 0

    def _page(self, response):
        '''获取当前页'''
        page = 1
        if not self.config['page']: return 1
        if 'page_type' in self.config and self.config['page_type'].startswith('string'):
            page = response.xpath(self.config['page']).extract_first()
        else:
            element = self.driver.find_element_by_xpath(self.config['page'])
            if element.tag_name.startswith('input'):
                page = element.get_attribute('value')
            else:
                page = element.text
        return int(page.strip()) if page else 1

    def _is_more(self, page, pages):
        '''判断下一页'''
        return True if page < pages else False

    def parse_next(self, response):
        if 'next' in self.config:
            pages = self._total_pages(response)
            page = self._page(response)
            print(page, pages, self._is_more(page, pages))
            if self._is_more(page, pages):
                if self.config['next_button']:
                    yield from self.parse_next_click(response)
                elif not self.config['next_button']:
                    yield from self.parse_next_url(response)

    def parse_next_click(self, response):
        '''点击下一页'''

        yield ClickRequest(response.url, dont_filter=True)

    def parse_next_url(self, response):
        '''打开连接'''
        _next = response.xpath(self.config['next']).extract_first()
        if _next:
            url = self.config['website'] + _next
            print('next link', url)
            yield self._request(url=url, dont_filter=True)
