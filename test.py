import json
import os
from pprint import pprint
import dotenv

from main import NeteaseCloudMusicApi

dotenv.load_dotenv()  # 从.env文件中加载环境变量

netease_cloud_music_api = NeteaseCloudMusicApi()  # 初始化API
netease_cloud_music_api.cookie = os.getenv("COOKIE")  # 设置cookie
netease_cloud_music_api.DEBUG = True  # 开启调试模式


def songv1_test():
    # 获取歌曲详情
    response = netease_cloud_music_api.api("song_url_v1", {"id": 33894312, "level": "exhigh"})
    pprint(json.loads(response.text))


def search_test():
    # 搜索
    response = netease_cloud_music_api.api("search", {"keywords": "海阔天空"})
    # print("|", response.text, "|")
    pprint(json.loads(response.text))


def search_default_test():
    # 搜索
    response = netease_cloud_music_api.api("search_default")
    pprint(json.loads(response.text))


def user_account_test():
    # 获取用户账号信息
    response = netease_cloud_music_api.api("user_account")
    pprint(json.loads(response.text))


def comment_new_test():
    # 获取用户账号信息
    response = netease_cloud_music_api.api("comment_new", {
        "type": "0",
        "id": "1407551413",
        "sortType": 3,
        "cursor": 1602072870260,
        "pageSize": 20,
        "pageNo": 2,
        "realIP": "116.25.146.177",
    })
    pprint(json.loads(response.text))


if __name__ == '__main__':
    pass
    # songv1_test()
    # search_test()
    # search_default_test()
    # user_account_test()
    # comment_new_test()
