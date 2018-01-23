# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector

from DgSpiderPhantomJS import urlSettings
from DgSpiderPhantomJS.items import DgspiderPostItem
from DgSpiderPhantomJS.mysqlUtils import dbhandle_geturl
from DgSpiderPhantomJS.mysqlUtils import dbhandle_update_status
from DgSpiderPhantomJS.notusedspiders import contentSettings


class DgcontentspiderPhantomjsSpider(scrapy.Spider):
    print('>>> Spider DgContentPhantomJSSpider Staring  ...')

    # get url from db
    result = dbhandle_geturl(urlSettings.GROUP_ID)
    url = result[0]
    spider_name = result[1]
    site = result[2]
    gid = result[3]
    module = result[4]

    # set spider name
    name = contentSettings.SPIDER_NAME
    # name = 'DgUrlSpiderPhantomJS'

    # set domains
    allowed_domains = [contentSettings.DOMAIN]

    # set scrapy url
    start_urls = [url]

    # change status
    """对于爬去网页，无论是否爬取成功都将设置status为1，避免死循环"""
    dbhandle_update_status(url, 1)

    # scrapy crawl
    def parse(self, response):

        # init the item
        item = DgspiderPostItem()

        # get the page source
        sel = Selector(response)

        print(sel)

        # get post title
        title_date = sel.xpath(contentSettings.POST_TITLE_XPATH)
        item['title'] = title_date.xpath('string(.)').extract()

        # get post page source
        item['text'] = sel.xpath(contentSettings.POST_CONTENT_XPATH).extract()

        # get url
        item['url'] = self.url

        yield item

