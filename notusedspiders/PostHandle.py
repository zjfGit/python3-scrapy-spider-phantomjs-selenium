# -*- coding: utf-8 -*-

import json

from DgSpiderPhantomJS.mysqlUtils import dbhandle_get_content
from DgSpiderPhantomJS.mysqlUtils import dbhandle_update_status
from DgSpiderPhantomJS.notusedspiders.uploadUtils import upload_post


def post_handel(url):
    result = dbhandle_get_content(url)

    title = result[0]
    content = result[1]
    user_id = result[2]
    gid = result[3]
    cs = []

    text_list = content.split('[dgimg]')
    for text_single in text_list:
        text_single_c = text_single.split('[/dgimg]')
        if len(text_single_c) == 1:
            cs_json = {"c": text_single_c[0], "i": '', "w": '', "h": ''}
            cs.append(cs_json)
        else:
            # tmp_img_upload_json = upload_img_result.pop()
            pic_flag = text_single_c[1]
            img_params = text_single_c[0].split(';')
            i = img_params[0]
            w = img_params[1]
            h = img_params[2]
            cs_json = {"c": pic_flag, "i": i, "w": w, "h": h}
            cs.append(cs_json)

    strcs = json.dumps(cs)
    json_data = {"apisign": "99ea3eda4b45549162c4a741d58baa60",
                 "user_id": user_id,
                 "gid": gid,
                 "t": title,
                 "cs": strcs}
    # 上传帖子
    result_uploadpost = upload_post(json_data)

    # 更新状态2，成功上传帖子
    result_updateresult = dbhandle_update_status(url, 2)
#
# if __name__ == '__main__':
#     post_handel('http://www.mama.cn/baby/art/20140523/773474.html')
