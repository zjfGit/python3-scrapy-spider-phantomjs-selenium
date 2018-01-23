# douguo object pool
# for the page which loaded by js/ajax
# ang changes should be recored here:
#
# @author zhangjianfei
# @date 2017/05/08

from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import random
import os
import DgSpiderPhantomJS.settings as settings
import pickle


def save_driver():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (random.choice(settings.USER_AGENTS))
    dcap["phantomjs.page.settings.loadImages"] = False
    driver = webdriver.PhantomJS(executable_path=r"D:\phantomjs-2.1.1\bin\phantomjs.exe", desired_capabilities=dcap)
    fn = open('D:\driver.pkl', 'w')

    # with open(fn, 'w') as f:
    pickle.dump(driver, fn, 0)
    fn.close()


def get_driver():
    fn = 'D:\driver.pkl'
    with open(fn, 'r') as f:
        driver = pickle.load(f)
    return driver


if __name__ == '__main__':
    save_driver()
