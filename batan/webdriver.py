from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import platform
import os


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
