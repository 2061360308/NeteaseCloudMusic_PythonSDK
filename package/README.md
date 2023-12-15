# NeteaseCloudMusic_PythonSDK
> 基于 [ NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi) 封装的 Python SDK。
> 网易云API Python版本。
> 现已同步原项目接口且测试通过的有200多个
> 已发布到PyPi，可直接使用pip安装
> 项目地址：[GitHub](https://github.com/2061360308/NeteaseCloudMusic_PythonSDK)

![](https://img.shields.io/badge/py_mini_racer-@0.6.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-yellow)

### 依赖于
- [ NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)
- [ NeteaseCloudMusicApi_V8 ](https://github.com/2061360308/NeteaseCloudMusicApi_V8)

### 原理
- 通过 `py_mini_racer` 调用 `NeteaseCloudMusicApi_V8` 的 `js` 方法。进一步进行了简单封装。

### 使用
- 安装 `pip install NeteaseCloudMusic`
- 导入API进行使用(具体查看`test.py`中的示例)
```python
from NeteaseCloudMusic import NeteaseCloudMusicApi, api_help, api_list
import os

netease_cloud_music_api = NeteaseCloudMusicApi()  # 初始化API
netease_cloud_music_api.cookie = os.getenv("COOKIE")  # 设置cookie
response = netease_cloud_music_api.request("song_url_v1", {"id": 33894312, "level": "exhigh"})  # 调用API

# 获取帮助
print(api_help())
print(api_help('song_url_v1'))
# 获取API列表
print(api_list())
```

> 注意： request(self, name, query=None) 的第一个参数为API名称，第二个参数为API参数，具体API名称和参数请参考 [NeteaseCloudMusicApi文档](https://docs.neteasecloudmusicapi.binaryify.com)，name支持`/song/url/v1`和`song_url_v1`两种写法。


### 开发
- 克隆项目 `git clone git@github.com:2061360308/NeteaseCloudMusic_PythonSDK.git`
- 安装依赖 `pip install -r requirements.txt`
- 目录/文件说明
├── package  项目包根目录
├── test_gender  生成测试代码的脚本
├── test.py  手动测试/ 使用示例


### 改进
> 下列API未支持
>
- apicache.js
- memory-cache.js
- request_reference.js
- avatar_upload.js
- cloud.js
- playlist_cover_update.js
- voice_upload.js
- register_anonimous.js
- verify_getQr.js

> 以下api未测试(这些接口测试起来比较繁琐)
> 
- /user/replacephone
- /audio/match
- /rebind
- /nickname/check
- /activate/init/profile
- /cellphone/existence/check
- /register/cellphone
- /captcha/verify
- /captcha/sent
- /login/refresh
- /logout
- /user/update
- /pl/count
- /playlist/update
- /playlist/desc/update
- /playlist/name/update
- /playlist/tags/update
- /event/forward
- /event/del
- /share/resource
- /send/text
- /send/playlist
- /playlist/create
- /playlist/tracks
- /daily_signin
- /fm_trash

### 欢迎提交PR
