# class CLanguage:
#     # 定义__call__方法
#     def __call__(self,name,add):
#         print("调用__call__()方法",name,add)
# clangs = CLanguage()
# clangs("C语言中文网","http://c.biancheng.net")
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import platform
import os
from scrapy.utils.project import get_project_settings
from batan.request import ClickAccess

settings = get_project_settings().copy()


class WebDriver(object):
    chromedriver = None

    def __init__(self, settings):
        self.settings = settings

    def __call__(self, *args, **kwargs):
        chrome_options = Options()
        # 无头模式
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # 不调用Java
        chrome_options.add_argument('–disable-java')
        # 拦截弹出
        chrome_options.add_argument('–disable-popup-blocking')
        # 不打开应用页
        chrome_options.add_argument('--no-sandbox')
        # 单进程
        chrome_options.add_argument('–single-process')
        # 无痕模式
        chrome_options.add_argument('–incognito')

        # 禁止图片和css加载
        chrome_options.add_experimental_option("prefs", {
            'profile.managed_default_content_settings.images': 2,
            # 'profile.managed_default_content_settings.javascript': 2,
            'permissions.default.stylesheet': 2
        })

        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["pageLoadStrategy"] = "none"

        if platform.system() == 'Linux':
            self.chromedriver = os.path.join(self.settings['BASE_DIR'], 'tools/linux/chromedriver')
        elif platform.system() == 'Windows':
            self.chromedriver = os.path.join(self.settings['BASE_DIR'], 'tools\windows\chromedriver.exe')

        return webdriver.Chrome(
            executable_path=self.chromedriver,
            options=chrome_options,
            # service_args=service_args
        )


url = 'http://www.bwea.org.cn/bwea_credit/credit/jsp_credit_cydw.jsp'
wd = WebDriver()()
wd.get(url)
html = wd.page_source
print(html)
fa = ClickAccess(request=None, xpath='//button[@id="ext-gen36"]', webdriver=wd)()


# r = requests.post(
#     url='http://etl.maotouin.com/v1/ShuiLiCompany.htm',
#     # url='http://127.0.0.1:5000/v1/ShuiLiCompany.htm',
#     headers={'Content-Type': 'application/json'},
#     data=json.dumps({"area": "辽宁省", "name": "朝阳莱恩水务工程建设有限公司", "source": "LiaoNingShuiLiSpider"})
# )
# print(r.json())