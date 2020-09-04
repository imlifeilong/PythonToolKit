import requests
import json


class FastRequest(object):
    def __init__(self):
        self.session = requests.Session()
        self.pages = None
        self.name = self.__class__.__name__

    def post_data(self, url, data):
        data['source'] = self.name
        r = requests.post(url=url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
        if r.ok and r.status_code == 200:
            res = r.json()
            print(res)

    def parse_pages(self, totals, offset):
        pages = totals // offset
        if totals % offset != 0:
            pages += 1
        self.pages = pages
