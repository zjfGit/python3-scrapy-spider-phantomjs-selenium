import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


def upload_post(json_data):
    # 上传帖子 ，参考：http://192.168.2.25:3000/api/interface/2016
    # create_post_url = "http://api.qa.douguo.net/robot/uploadimagespost"
    create_post_url = "http://api.douguo.net/robot/uploadimagespost"

    # 传帖子
    # dataJson = json.dumps({"user_id":"19013245","gid":30,"t":"2017-03-23","cs":[{"c":"啦啦啦","i":"","w":0,"h":0},
    #                       {"c":"啦啦啦2222","i":"http://wwww.douguo.com/abc.jpg","w":0,"h":0}],"time":1235235234})
    # jsonData = {"user_id":"19013245","gid":5,"t":"TEST","cs":'[{"c":"啊啊啊","i":"qqq","w":12,"h":10},
    #               {"c":"这个内容真不错","i":"http://wwww.baidu.com","w":10,"h":10}]',"time":61411313}

    # print(jsonData)
    req_post = requests.post(create_post_url, data=json_data)
    print(req_post.json())
    # print(reqPost.text)


def uploadImage(img_path, content_type, user_id):
    # 上传单个图片 ， 参考：http://192.168.2.25:3000/api/interface/2015
    # UPLOAD_IMG_URL = "http://api.qa.douguo.net/robot/uploadpostimage"
    UPLOAD_IMG_URL = "http://api.douguo.net/robot/uploadpostimage"
    # 传图片

    m = MultipartEncoder(
        # fields={'user_id': '192323',
        #         'images': ('filename', open(imgPath, 'rb'), 'image/JPEG')}
        fields={'user_id': user_id,
                'apisign': '99ea3eda4b45549162c4a741d58baa60',
                'image': ('filename', open(img_path, 'rb'), 'image/jpeg')}
    )

    r = requests.post(UPLOAD_IMG_URL, data=m, headers={'Content-Type': m.content_type})
    print(r.json())
    # print(r.text)
    return r.json()
    # return r.text