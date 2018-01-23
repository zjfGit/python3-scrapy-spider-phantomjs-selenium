# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

from DgSpiderPhantomJS import urlSettings
from DgSpiderPhantomJS.items import DgspiderUrlItem


class UrlspiderYmyeSpider(scrapy.Spider):

    name = "UrlSpider_YMYE"

    # set your allowed domain
    allowed_domains = [urlSettings.DOMAIN]

    # set spider start url
    start_urls = [urlSettings.URL_START_YMYE]

    # scrapy crawl
    def parse(self, response):
        print("LOGS: Starting spider YMYE ...")

        # init the item
        item = DgspiderUrlItem()

        # get the page source
        sel = Selector(response)

        # page_source = self.page
        url_list = sel.xpath(urlSettings.POST_URL_PHANTOMJS_XPATH).extract()

        # if the url you got had some prefix, it will works, such as 'http://'
        url_item = []
        for url in url_list:
            url = url.replace(urlSettings.URL_PREFIX, '')
            url_item.append(urlSettings.URL_PREFIX + url)

        # use set to del repeated urls
        url_item = list(set(url_item))

        item['url'] = url_item

        # transer item to pipeline
        yield item

        # for i in range(5):
        #     yield Request(self.start_urls[0], callback=self.parse)