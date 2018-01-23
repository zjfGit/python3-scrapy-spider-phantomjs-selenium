import datetime
import sys, shelve, time, execjs
# import PyV8

# create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# print(create_time)


def initDriverPool():
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_array = time.strptime(create_time, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array))

    print(time_stamp)

def execjs():
    js_str = open('D:\Scrapy\DgSpiderPhantomJS\DgSpiderPhantomJS\params.js').read()
    a = execjs.compile(js_str).call('getParam')
    # a = execjs.eval(js_str3)
    print(a)

# def js(self):
#     ctxt = PyV8.JSContext()
#     ctxt.enter()
#     func = ctxt.eval('''(function(){return '###'})''')
#     print(func)

if __name__=='__main__':
    execjs()