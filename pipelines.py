# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
from DgSpiderPhantomJS import urlSettings
from DgSpiderPhantomJS.mysqlUtils import dbhandle_online
from DgSpiderPhantomJS.commonUtils import get_linkmd5id


class DgspiderphantomjsPipeline(object):

    def __init__(self):
        pass

    # process the data
    def process_item(self, item, spider):

        # get mysql connettion
        db_object = dbhandle_online()
        cursor = db_object.cursor()

        print(">>>>> Spider name :")
        print(spider.name)

        for url in item['url']:
            linkmd5id = get_linkmd5id(url)

            if spider.name == urlSettings.SPIDER_JFSS:
                spider_name = urlSettings.SPIDER_JFSS
                gid = urlSettings.GROUP_ID_JFSS
            elif spider.name == urlSettings.SPIDER_MSZT:
                spider_name = urlSettings.SPIDER_MSZT
                gid = urlSettings.GROUP_ID_MSZT
            elif spider.name == urlSettings.SPIDER_SYDW:
                spider_name = urlSettings.SPIDER_SYDW
                gid = urlSettings.GROUP_ID_SYDW
            elif spider.name == urlSettings.SPIDER_YLBG:
                spider_name = urlSettings.SPIDER_YLBG
                gid = urlSettings.GROUP_ID_YLBG
            elif spider.name == urlSettings.SPIDER_YMYE:
                spider_name = urlSettings.SPIDER_YMYE
                gid = urlSettings.GROUP_ID_YMYE

            module = urlSettings.MODULE
            site = urlSettings.DOMAIN
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            status = '0'
            sql_search = 'select md5_url from dg_spider.dg_spider_post where md5_url="%s"' % linkmd5id
            sql = 'insert into dg_spider.dg_spider_post(md5_url, url, spider_name, site, gid, module, status, ' \
                  'create_time) ' \
                  'values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' \
                  % (linkmd5id, url, spider_name, site, gid, module, status, create_time)
            try:
                # if url is not existed, then insert
                cursor.execute(sql_search)
                result_search = cursor.fetchone()
                if result_search is None or result_search[0].strip() == '':
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    db_object.commit()
            except Exception as e:
                print("Waring!: catch exception !")
                print(e)
                db_object.rollback()

        return item

    # spider开启时被调用
    def open_spider(self, spider):
        pass

    # sipder 关闭时被调用
    def close_spider(self, spider):
        pass
