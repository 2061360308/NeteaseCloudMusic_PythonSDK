import json
import os.path
import socket
from pprint import pprint
import requests
from py_mini_racer import py_mini_racer


class NeteaseCloudMusicApi:
    def __init__(self):
        with open('NeteaseCloudMusicApi.js', 'r', encoding='utf-8') as file:
            js_code = file.read()
        self.ctx = py_mini_racer.MiniRacer()
        self.ctx.eval(js_code)

        self.DEBUG = False

        self.__cookie = None
        self.__ip = None

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
                raise Exception("cookie not found")
        else:
            return self.__cookie

    @cookie.setter
    def cookie(self, cookie):
        self.__cookie = cookie
        with open("cookie_storage", "w+", encoding='utf-8') as f:
            f.write(cookie)

    @property
    def ip(self):
        if self.__ip is None:
            self.__ip = self.get_local_ip()
        return self.__ip

    def getRequestParam(self, name, query):
        result = self.ctx.call('NeteaseCloudMusicApi', name, query)  # 拿到请求头和请求参数

        if result.get("error"):
            raise Exception(result.get("error"))

        if self.DEBUG:
            print("RequestParam:")
            for item in result.keys():
                print(f"    - {item}:{result[item]}")
            # pprint(json.dumps(result))
            with open('result.json', 'w', encoding='utf-8') as file:
                file.write(json.dumps(result))

        return result

    def api(self, name, query=None):
        if query is None:
            query = {}
        if query.get("cookie") is None:
            query["cookie"] = self.cookie

        if query.get("realIP") is None:
            query["realIP"] = self.ip
        else:
            query["realIP"] = query.get("realIP")

        result = self.getRequestParam(name, query)

        param_data = {}
        for item in result["data"].split("&"):
            param_data[item.split("=")[0]] = item.split("=")[1]

        if self.DEBUG:
            print(f"    - param_data:{param_data}")

        response = requests.post(result["url"], data=param_data, headers=result["headers"])
        return response
