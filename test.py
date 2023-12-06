import json
import os
from pprint import pprint
import dotenv

from main import NeteaseCloudMusicApi

dotenv.load_dotenv()

netease_cloud_music_api = NeteaseCloudMusicApi()
netease_cloud_music_api.cookie = os.getenv("COOKIE")
netease_cloud_music_api.DEBUG = True


def songv1_test():
    # 获取歌曲详情
    response = netease_cloud_music_api.api("song_url_v1", {"id": 33894312, "level": "exhigh"})
    pprint(json.loads(response.text))


def search_test():
    # 搜索
    response = netease_cloud_music_api.api("search", {"keywords": "海阔天空"})
    print("|", response.text, "|")
    # pprint(json.loads(response.text))


def search_default_test():
    # 搜索
    response = netease_cloud_music_api.api("search_default")
    pprint(json.loads(response.text))


def user_account_test():
    # 获取用户账号信息
    response = netease_cloud_music_api.api("user_account")
    pprint(response.text)


if __name__ == '__main__':
    # songv1_test()
    # search_test()
    # search_default_test()
    user_account_test()
