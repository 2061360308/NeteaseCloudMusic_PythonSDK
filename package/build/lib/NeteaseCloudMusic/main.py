import json
import os.path
import socket
from pprint import pprint

import pkg_resources
import requests
from py_mini_racer import py_mini_racer
from .help import api_list


class NeteaseCloudMusicApi:
    __cookie = None
    __ip = None

    def __init__(self, debug=False):
        self.DEBUG = debug  # 是否开启调试模式

        self.special_api = {"/playlist/track/all": self.playlist_track_all,
                            "/inner/version": self.inner_version}

        # 载入js代码
        resource_path = pkg_resources.resource_filename(__name__, 'NeteaseCloudMusicApi.js')

        with open(resource_path, 'r', encoding='utf-8') as file:
            js_code = file.read()
        self.ctx = py_mini_racer.MiniRacer()
        self.ctx.eval(js_code)

    def request(self, name: str, query: dict = None) -> dict:
        """
        调用接口
        接口文档地址： https://docs.neteasecloudmusicapi.binaryify.com
        :param name: api名称 例如: song_url_v1, /song/url/v1
        :param query: 请求参数
        :return: 请求结果 示例：{"code": 200, "data": {}, "msg": "success"}
        """

        special = {
            'daily_signin': '/daily_signin',
            'fm_trash': '/fm_trash',
            'personal_fm': '/personal_fm',
        }

        yubei_special = {'/yunbei/tasks/receipt': '/yunbei/receipt',
                         '/yunbei/tasks/expense': '/yunbei/expense'}  # 这俩个接口准换的路由莫名奇妙

        # 测试name是否合法
        name.replace("\\", "/")
        if not name.startswith("/"):
            if name in special.keys():
                name = special[name]
            else:
                name = "/" + name
                name = name.replace("_", "/")

        # 处理俩个云贝接口名称转换问题
        if name in yubei_special.keys():
            name = yubei_special[name]
            print("转换了个麻烦的路由", name)

        if name not in api_list():
            if name not in yubei_special.values():
                raise Exception(f"apiName: {name} not found，please use ”api_list()“ to view the interface list")

        if query is None:
            query = {}
        if query.get("cookie") is None:
            query["cookie"] = self.cookie

        if query.get("realIP") is None:
            query["realIP"] = self.ip
        else:
            query["realIP"] = query.get("realIP")

        # 特殊api处理
        if name in self.special_api.keys():
            result = self.special_api[name](query)
        else:
            result = self.call_api(name, query)

        return result

    @staticmethod
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            print("get local ip error")
            IP = "116.25.146.177"
        finally:
            s.close()
        return IP

    @property
    def cookie(self):
        if self.__cookie is None:
            if os.path.isfile("cookie_storage"):
                with open("cookie_storage", "r", encoding='utf-8') as f:
                    self.__cookie = f.read()
            else:
                self.__cookie = ""  # 如果没有cookie文件，就设置为空

        return self.__cookie

    @cookie.setter
    def cookie(self, cookie):
        if cookie is None:
            cookie = ""
        self.__cookie = cookie
        with open("cookie_storage", "w+", encoding='utf-8') as f:
            f.write(cookie)

    @property
    def ip(self):
        if self.__ip is None:
            self.__ip = self.get_local_ip()
        return self.__ip

    def call_api(self, name, query):
        request_param = self.ctx.call('NeteaseCloudMusicApi.beforeRequest', name, query)  # 拿到请求头和请求参数

        param_data = {}
        if request_param["data"] != "":
            for item in request_param["data"].split("&"):
                param_data[item.split("=")[0]] = item.split("=")[1]

        # print("url", request_param["url"], "data", param_data, "headers\n", json.dumps(request_param["headers"], indent=2, ensure_ascii=False))

        if request_param.get("method") == "GET":
            response = requests.get(request_param["url"], params=param_data, headers=request_param["headers"])
        else:
            response = requests.post(request_param["url"], data=param_data, headers=request_param["headers"])
        # response = requests.post(request_param["url"], data=param_data, headers=request_param["headers"])

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            data = response.text

        response_result = {
            "headers": dict(response.headers),
            "data": data,
            "status": response.status_code,
        }

        result = self.ctx.call('NeteaseCloudMusicApi.afterRequest',
                               json.dumps(response_result),
                               request_param.get('crypto', None),
                               request_param['apiName'])  # 拿到请求结果

        return result

    def playlist_track_all(self, query):
        """
        获取歌单全部歌曲
        :param query:
        :return:
        """

        detail_query = {"id": query.get("id"), "cookie": query.get("cookie"), "realIP": query.get("realIP")}

        result = self.call_api("/playlist/detail", detail_query)

        track_all_query = {"detail_result": json.dumps(result), "cookie": query.get("cookie"),
                           "realIP": query.get("realIP")}
        if query.get("limit"):
            track_all_query["limit"] = query.get("limit")
        if query.get("offset"):
            track_all_query["offset"] = query.get("offset")

        result = self.call_api("/playlist/track/all", track_all_query)
        return result

    def inner_version(self, query):
        """
        获取所使用的 NeteaseCloudMusicApi 和 NeteaseCloudMusicApi_V8 版本号
        :param query:
        :return:
        """
        result = self.ctx.call('NeteaseCloudMusicApi.inner_version')
        return result


if __name__ == '__main__':
    import json
    import os
    from pprint import pprint
    import dotenv

    dotenv.load_dotenv("../../.env")  # 从.env文件中加载环境变量

    netease_cloud_music_api = NeteaseCloudMusicApi()  # 初始化API
    netease_cloud_music_api.cookie = os.getenv("COOKIE")  # 设置cookie
    netease_cloud_music_api.DEBUG = True  # 开启调试模式


    def songv1_test():
        # 获取歌曲详情
        response = netease_cloud_music_api.request("song_url_v1", {"id": 33894312, "level": "exhigh"})
        pprint(response)


    songv1_test()
