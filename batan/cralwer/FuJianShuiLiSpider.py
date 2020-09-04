import requests

try:
    from .request import FastRequest
except:
    from batan.cralwer.request import FastRequest


class FuJianShuiLiSpider(FastRequest):
    '''福建水利'''
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "61.154.12.112:9001",
        "Referer": "http://61.154.12.112:9001/CreditFB_web/xxpt.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    def crawl(self):
        r = self.session.get(
            url='http://61.154.12.112:9001/Handler/PublicHandler.ashx',
            params={
                "flag": "GetCompanyInfoList",
                "PageIndex": "1",
                "PageSize": "11",
                "CompanyName": "",
                "Legal": "",
                "PROVINCE": "",
                "CITY": "",
                "COUNTRY": "",
                "orderbyCode": "",
                "orderbyN": "",
                "math": "0.7053609341337956",
            },
            headers=self.headers
        )
        if r.status_code == 200 and r.ok:
            data = r.json()
            self.parse_pages(data['Count'], 11)
            self.crawl_next()

    def parse(self, data):
        for row in data['List']:
            item = {}
            item['name'] = row['C_NAME']
            item['area'] = '福建省'
            self.post_data('http://etl.maotouin.com/v1/ShuiLiCompany.htm', data=item)

    def crawl_next(self):
        for page in range(221, self.pages + 1):
            print('-------------->', page, self.pages)
            r = self.session.get(
                url='http://61.154.12.112:9001/Handler/PublicHandler.ashx',
                params={
                    "flag": "GetCompanyInfoList",
                    "PageIndex": str(page),
                    "PageSize": "11",
                    "CompanyName": "",
                    "Legal": "",
                    "PROVINCE": "",
                    "CITY": "",
                    "COUNTRY": "",
                    "orderbyCode": "",
                    "orderbyN": "",
                    "math": "0.7053609341337956",
                },
                headers=self.headers
            )
            if r.ok and r.status_code == 200:
                data = r.json()
                self.parse(data)


if __name__ == '__main__':
    fj = FuJianShuiLiSpider()
    fj.crawl()
