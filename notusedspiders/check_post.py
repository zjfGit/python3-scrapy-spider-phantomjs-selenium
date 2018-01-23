import requests, re
import http
import urllib

# 圈圈：孕妈育儿 4
# 圈圈：减肥瘦身 33
# 圈圈：情感生活 30


def checkPost():
    # CREATE_POST_URL = "http://api.qa.douguo.net/robot/handlePost"
    CREATE_POST_URL = "http://api.douguo.net/robot/handlePost"

    fields={'group_id': '35',
            'type': 1,
            'apisign':'99ea3eda4b45549162c4a741d58baa60'}

    r = requests.post(CREATE_POST_URL, data=fields)

    print(r.json())


if __name__ == '__main__':
    #for i in range(1,50):
    #checkPost()
    checkPost()
    #    print(i),
    #print(testText('aaaa\001'))