# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import json
import logging


class BatanPipeline(object):
    def _post(self, url, data):
        r = requests.post(
            url=url,
            # url='http://127.0.0.1:5000/v1/ShuiLiCompany.htm',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data)
        )
        if r.ok and r.status_code == 200:
            res = r.json()
            print(res)
            # 企业未备案的企业名， 存到集合title_name1
            # if res['msg'] == '未找到企业' and res['code'] == -102:
            #     self.red.sadd('title_name1', data['companyName'])
        else:
            logging.error('post数据失败！%s' % data)

    def process_item(self, item, spider):
        if spider.config['spider'].startswith('ZhongGuoShuiLiProjectSpider'):
            item['name'] = item['name'].strip()
            self._post(spider.crawler.settings['ADD_SHUILI_PROJECT'], dict(item))

        return item
