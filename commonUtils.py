import random
import time
import datetime
from hashlib import md5


# 获取随机发帖ID
def get_random_user(user_str):
    user_list = []
    for user_id in str(user_str).split(','):
        user_list.append(user_id)
    userid_idx = random.randint(1, len(user_list))
    user_chooesd = user_list[userid_idx-1]
    return user_chooesd


# 获取MD5加密URL
def get_linkmd5id(url):
    # url进行md5处理，为避免重复采集设计
    md5_url = md5(url.encode("utf8")).hexdigest()
    return md5_url


# get unix time stamp
def get_time_stamp():
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_array = time.strptime(create_time, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array))
    return time_stamp

