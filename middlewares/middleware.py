# douguo request middleware
# for the page which loaded by js/ajax
# ang changes should be recored here:
#
# @author zhangjianfei
# @date 2017/05/04

from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from DgSpiderPhantomJS import urlSettings
import time
import datetime
import random
import os
import execjs
import DgSpiderPhantomJS.settings as settings


class JavaScriptMiddleware(object):

    def process_request(self, request, spider):

        print("LOGS: Spider name in middleware - " + spider.name)

        # 开启虚拟浏览器参数
        dcap = dict(DesiredCapabilities.PHANTOMJS)

        # 设置agents
        dcap["phantomjs.page.settings.userAgent"] = (random.choice(settings.USER_AGENTS))

        # 禁止加载图片
        dcap["phantomjs.page.settings.loadImages"] = False

        driver = webdriver.PhantomJS(executable_path=r"D:\phantomjs-2.1.1\bin\phantomjs.exe", desired_capabilities=dcap)

        # 由于phantomjs路径已经增添在path中，path可以不写
        # driver = webdriver.PhantomJS()

        # 利用firfox
        # driver = webdriver.Firefox(executable_path=r"D:\FireFoxBrowser\firefox.exe")

        # 利用chrome
        # chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        # os.environ["webdriver.chrome.driver"] = chromedriver
        # driver = webdriver.Chrome(chromedriver)

        # 模拟登陆
        # driver.find_element_by_class_name("input_id").send_keys("34563453")
        # driver.find_element_by_class_name("input_pwd").send_keys("zjf%#￥&")
        # driver.find_element_by_class_name("btn btn_lightgreen btn_login").click()
        # driver.implicitly_wait(15)
        # time.sleep(10)

        # 模拟用户下拉
        # js1 = 'return document.body.scrollHeight'
        # js2 = 'window.scrollTo(0, document.body.scrollHeight)'
        # js3 = "document.body.scrollTop=1000"
        # old_scroll_height = 0
        # while driver.execute_script(js1) > old_scroll_height:
        #     old_scroll_height = driver.execute_script(js1)
        #     driver.execute_script(js2)
        #     time.sleep(3)

        # 设置20秒页面超时返回
        driver.set_page_load_timeout(180)
        # 设置20秒脚本超时时间
        driver.set_script_timeout(180)

        # get time stamp

        # get page screenshot
        # driver.save_screenshot("D:\p.jpg")

        # 模拟用户在同一个浏览器对象下刷新页面
        # the whole page source
        body = ''
        for i in range(50):
            print("SPider name: " + spider.name)
            # sleep in a random time for the ajax asynchronous request
            # time.sleep(random.randint(5, 6))
            time.sleep(random.randint(300, 600))

            print("LOGS: freshing page " + str(i) + "...")

            # get page request
            driver.get(request.url)

            # waiting for response
            driver.implicitly_wait(30)

            # get page resource
            body = body + driver.page_source

        return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)


