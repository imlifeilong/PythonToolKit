import requests
import json

try:
    from .request import FastRequest
except:
    from batan.cralwer.request import FastRequest


class JiangXiShuiLiSpider(FastRequest):
    '''江西水利'''
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Length": "80",
        "Content-Type": "application/json",
        "Host": "jsscjgpt.jxwrd.gov.cn",
        "Origin": "http://jsscjgpt.jxwrd.gov.cn",
        "Proxy-Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    def crawl(self):
        r = self.session.post(
            url='http://jsscjgpt.jxwrd.gov.cn/api/employer/findAll',
            data=json.dumps({
                "pageNum": 1,
                "pageSize": 10,
                "query": "",
                "unitName": "",
                "unitCode": "",
                "userName": ""
            }),
            headers=self.headers
        )
        if r.status_code == 200 and r.ok:
            data = r.json()
            self.pages = data['data']['pages']
            self.crawl_next()

    def parse(self, data):
        for row in data['data']['list']:
            item = {}
            item['name'] = row['name']
            # item['source'] = 'FuJianShuiLiSpider'
            item['area'] = '江西省'
            print(item)
            self.post_data('http://etl.maotouin.com/v1/ShuiLiCompany.htm', data=item)

    def crawl_next(self):
        for page in range(1, self.pages + 1):
            print('-------------->', page, self.pages)
            r = self.session.post(
                url='http://jsscjgpt.jxwrd.gov.cn/api/employer/findAll',
                data=json.dumps({
                    "pageNum": page,
                    "pageSize": 10,
                    "query": "",
                    "unitName": "",
                    "unitCode": "",
                    "userName": ""
                }),
                headers=self.headers
            )
            if r.ok and r.status_code == 200:
                data = r.json()
                self.parse(data)


if __name__ == '__main__':
    fj = JiangXiShuiLiSpider()
    fj.crawl()
