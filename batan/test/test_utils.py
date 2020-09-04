# class CLanguage:
#     # 定义__call__方法
#     def __call__(self,name,add):
#         print("调用__call__()方法",name,add)
# clangs = CLanguage()
# clangs("C语言中文网","http://c.biancheng.net")
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import platform
import os
from scrapy.utils.project import get_project_settings
from batan.request import ClickAccess
from batan.chrome_proxy_extension import proxy_auth_plugin_path

settings = get_project_settings().copy()


class WebDriver(object):
    chromedriver = None

    def __init__(self, settings):
        self.settings = settings

    def __call__(self, *args, **kwargs):
        chrome_options = Options()
        # chrome_options = ChromeOptions()
        # 添加认证代理
        chrome_options.add_extension(proxy_auth_plugin_path)
        # 无头模式
        # chrome_options.add_argument('--headless')
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
        # 代理
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


# # !/usr/bin/env python
# # encoding: utf-8
#
# from selenium import webdriver
# import time
#
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=http://t19840672147027:0skfkkzt@tps121.kdlapi.com:15818')  # 隧道域名:端口号
# # ${chromedriver_path}: chromedriver驱动存放路径
# driver = webdriver.Chrome(executable_path=os.path.join(settings['BASE_DIR'], 'tools\windows\chromedriver.exe'),
#                           chrome_options=chrome_options)
# driver.get("https://dev.kdlapi.com/testproxy")
#
# # 获取页面内容
# print(driver.page_source)
#
# # 延迟3秒后关闭当前窗口，如果是最后一个窗口则退出
# time.sleep(3)
# driver.close()

url = 'https://dev.kdlapi.com/testproxy'
wd = WebDriver(settings)()
wd.get(url)
html = wd.page_source
print(html)
wd.close()
# fa = ClickAccess(request=None, xpath='//button[@id="ext-gen36"]', webdriver=wd)()


# r = requests.post(
#     url='http://etl.maotouin.com/v1/ShuiLiCompany.htm',
#     # url='http://127.0.0.1:5000/v1/ShuiLiCompany.htm',
#     headers={'Content-Type': 'application/json'},
#     data=json.dumps({"area": "辽宁省", "name": "朝阳莱恩水务工程建设有限公司", "source": "LiaoNingShuiLiSpider"})
# )
# print(r.json())
