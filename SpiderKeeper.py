# -*- coding: utf-8 -*-

import time
import threading
from scrapy import cmdline

# def ylbg():
#     print(">> thread.staring ylbg ...")
#     cmdline.execute("scrapy crawl UrlSpider_YLBG".split())
#     print(">> thread.ending ylbg ...")
#
# def sydw():
#     print(">> thread.starting sydw ...")
#     cmdline.execute("scrapy crawl UrlSpider_SYDW".split())
#     print(">> thread.ending sydw ...")
#
# threading._start_new_thread(ylbg())
# threading._start_new_thread(sydw())

# 配置 commands ,执行 scrapy list 下的所有spider
cmdline.execute("scrapy crawlall".split())



