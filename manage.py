# coding:utf-8

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from batan.spiders.batan import BaseSpider

spider_list = [
    # 'BeiJingShuiLiSpider', # 北京水利
    # 'HeBeiShuiLiSpider',  # 河北水利
    # 'NeiMengGuShuiLiSpider', # 内蒙古水利
    # 'LiaoNingShuiLiSpider',  # 辽宁水利
    # 'HeiLongJiangShuiLiSpider', # 黑龙江水利
    'ShangHaiShuiLiSpider',  # 上海水利
]

settings = get_project_settings().copy()


def crawl(spider_names):
    process = CrawlerProcess(settings)
    for spider in spider_names:
        process.crawl(spider)
    process.start()


def cus_crawl(spiders):
    process = CrawlerProcess(settings)
    for spider in spiders:
        SpidersCus = type(spider, (BaseSpider,), {'name': spider})
        process.crawl(SpidersCus)
    process.start()


if __name__ == '__main__':
    # crawl(spider_list)

    cus_crawl(spider_list)
