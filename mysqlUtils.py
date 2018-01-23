import pymysql
import pymysql.cursors
import os


def dbhandle_online():
    host = '192.168.1.235'
    user = 'root'
    passwd = 'douguo2015'
    charset = 'utf8'
    conn = pymysql.connect(
        host=host,
        user=user,
        passwd=passwd,
        charset=charset,
        use_unicode=False
    )
    return conn


def dbhandle_local():
    host = '192.168.1.235'
    user = 'root'
    passwd = 'douguo2015'
    charset = 'utf8'
    conn = pymysql.connect(
        host=host,
        user=user,
        passwd=passwd,
        charset=charset,
        use_unicode=True
        # use_unicode=False
    )
    return conn


def dbhandle_geturl(gid):
    host = '192.168.1.235'
    user = 'root'
    passwd = 'douguo2015'
    charset = 'utf8'
    conn = pymysql.connect(
        host=host,
        user=user,
        passwd=passwd,
        charset=charset,
        use_unicode=False
    )
    cursor = conn.cursor()
    sql = 'select url,spider_name,site,gid,module from dg_spider.dg_spider_post where status=0 and gid=%s limit 1' % gid
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
    except Exception as e:
        print("***** exception")
        print(e)
        conn.rollback()

    if result is None:
        os._exit(0)
    else:
        url = result[0]
        spider_name = result[1]
        site = result[2]
        gid = result[3]
        module = result[4]
        return url.decode(), spider_name.decode(), site.decode(), gid.decode(), module.decode()


def dbhandle_insert_content(url, title, content, user_id, has_img):
    host = '192.168.1.235'
    user = 'root'
    passwd = 'douguo2015'
    charset = 'utf8'
    conn = pymysql.connect(
        host=host,
        user=user,
        passwd=passwd,
        charset=charset,
        use_unicode=False
    )
    cur = conn.cursor()

    # 如果标题或者内容为空，那么程序将退出，篇文章将会作废并将status设置为1，爬虫继续向下运行获得新的URl
    if content.strip() == '' or title.strip() == '':
        sql_fail = 'update dg_spider.dg_spider_post set status="%s" where url="%s" ' % ('1', url)
        try:
            cur.execute(sql_fail)
            result = cur.fetchone()
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        os._exit(0)

    sql = 'update dg_spider.dg_spider_post set title="%s",content="%s",user_id="%s",has_img="%s" where url="%s" ' \
          % (title, content, user_id, has_img, url)

    try:
        cur.execute(sql)
        result = cur.fetchone()
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    return result


def dbhandle_update_status(url, status):
    host = '192.168.1.235'
    user = 'root'
    passwd = 'douguo2015'
    charset = 'utf8'
    conn = pymysql.connect(
        host=host,
        user=user,
        passwd=passwd,
        charset=charset,
        use_unicode=False
    )
    cur = conn.cursor()
    sql = 'update dg_spider.dg_spider_post set status="%s" where url="%s" ' \
          % (status, url)
    try:
        cur.execute(sql)
        result = cur.fetchone()
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    return result


def dbhandle_get_content(url):
    host = '192.168.1.235'
    user = 'root'
    passwd = 'douguo2015'
    charset = 'utf8'
    conn = pymysql.connect(
        host=host,
        user=user,
        passwd=passwd,
        charset=charset,
        use_unicode=False
    )
    cursor = conn.cursor()
    sql = 'select title,content,user_id,gid from dg_spider.dg_spider_post where status=1 and url="%s" limit 1' % url
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
    except Exception as e:
        print("***** exception")
        print(e)
        conn.rollback()

    if result is None:
        os._exit(1)

    title = result[0]
    content = result[1]
    user_id = result[2]
    gid = result[3]
    return title.decode(), content.decode(), user_id.decode(), gid.decode()


# 获取爬虫初始化参数
def dbhandle_get_spider_param(url):
    host = '192.168.1.235'
    user = 'root'
    passwd = 'douguo2015'
    charset = 'utf8'
    conn = pymysql.connect(
        host=host,
        user=user,
        passwd=passwd,
        charset=charset,
        use_unicode=False
    )
    cursor = conn.cursor()
    sql = 'select title,content,user_id,gid from dg_spider.dg_spider_post where status=0 and url="%s" limit 1' % url
    result = ''
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
    except Exception as e:
        print("***** exception")
        print(e)
        conn.rollback()
    title = result[0]
    content = result[1]
    user_id = result[2]
    gid = result[3]
    return title.decode(), content.decode(), user_id.decode(), gid.decode()
