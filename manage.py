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
    # 'ShangHaiShuiLiSpider',  # 上海水利
    # 'ZheJiangShuiLiSpider',  # 浙江水利
    # 'AnHuiShuiLiSpider',  # 安徽水利
    # 'ShanDongShuiLiSpider',  # 山东水利
    # 'HuBeiShuiLiSpider',  # 湖北水利
    # 'HuNanShuiLiSpider', # 湖南水利
    # 'GuangDongShuiLiSpider',  # 广东水利
    # 'GuangXiShiGongShuiLiSpider',  # 广西水利施工
    # 'GuangXiJianLiShuiLiSpider',  # 广西水利监理
    # 'GuangXiKanChaShuiLiSpider',  # 广西水利勘察设计
    # 'GuangXiZhaoBiaoShuiLiSpider',  # 广西水利招标代理
    # 'GuangXiJianCeShuiLiSpider',  # 广西水利检测
    # 'HaiNanShuiLiSpider',  # 海南水利
    # 'ChongQingShuiLiSpider',  # 重庆水利
    # 'GuiZhouShuiLiSpider',  # 贵州水利
    'XiZangShiGongShuiLiSpider',  # 西藏水利施工
    # 'XiZangGongHuoShuiLiSpider',  # 西藏水利供货
    # 'XiZangJianLiShuiLiSpider',  # 西藏水利监理
    # 'XiZangJianSheShuiLiSpider',  # 西藏水利建设
    # 'XiZangJiXieShuiLiSpider',  # 西藏水利机械
    # 'XiZangKanChaShuiLiSpider',  # 西藏水利勘察
    # 'XiZangSheJiShuiLiSpider',  # 西藏水利设计
    # 'XiZangZhaoBiaoShuiLiSpider',  # 西藏水利招标
    # 'XiZangZhiLiangShuiLiSpider',  # 西藏水利质量
    # 'XiZangZiXunShuiLiSpider',  # 西藏水利咨询
    # 'ShaanXiShuiLiSpider',  # 陕西水利
    # 'GanSuShuiLiSpider',  # 甘肃水利
    # 'QingHaiShuiLiSpider',  # 青海水利
    # 'ZhongGuoShuiLiSpider',  # 国家水利
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
