# -*- coding: utf-8 -*-

"""爬取域名"""
DOMAIN = 'toutiao.com'

"""圈子列表"""
# 减肥瘦身
GROUP_ID_JFSS = '33'
# 情感生活
GROUP_ID_QQSH = '30'
# 营养专家
GROUP_ID_YYZJ = '35'
# 孕妈育儿
GROUP_ID_YMYE = '4'
# 深夜豆文
GROUP_ID_SYDW = '37'
# 美食杂谈
GROUP_ID_MSZT = '24'
# 娱乐八卦
GROUP_ID_YLBG = '38'

"""爬虫列表"""
SPIDER_JFSS = 'UrlSpider_JFSS'
SPIDER_QQSH = 'UrlSpider_QQSH'
SPIDER_YYZJ = 'UrlSpider_YYZJ'
SPIDER_YMYE = 'UrlSpider_YMYE'
SPIDER_SYDW = 'UrlSpider_SYDW'
SPIDER_MSZT = 'UrlSpider_MSZT'
SPIDER_YLBG = 'UrlSpider_YLBG'

MODULE = '999'

# url 前缀
URL_PREFIX = 'http://www.toutiao.com'

# 爬取起始页
URL_START_JFSS = 'http://www.toutiao.com/ch/news_regimen/'
URL_START_YMYE = 'http://www.toutiao.com/ch/news_baby/'
URL_START_SYDW = 'http://www.toutiao.com/ch/news_essay/'
URL_START_MSZT = 'http://www.toutiao.com/ch/news_food/'
URL_START_YLBG = 'http://www.toutiao.com/ch/news_entertainment/'

"""静态页爬取规则"""
# # 文章列表页起始爬取URL
# START_LIST_URL = 'http://www.eastlady.cn/emotion/pxgx/1.html'
#
# # 文章列表循环规则
# LIST_URL_RULER_PREFIX = 'http://www.eastlady.cn/emotion/pxgx/'
# LIST_URL_RULER_SUFFIX = '.html'
# LIST_URL_RULER_LOOP = 30
#
# # 文章URL爬取规则XPATH
# POST_URL_XPATH = '//div[@class="article_list"]/ul/li/span[1]/a[last()]/@href'

"""今日头条-动态JS/Ajax爬取规则"""
POST_URL_PHANTOMJS_XPATH = '//div[@class="title-box"]/a/@href'


