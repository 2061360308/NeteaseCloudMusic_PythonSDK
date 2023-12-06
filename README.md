# NeteaseCloudMusic_PythonSDK
> 基于 [ NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi) 封装的 Python SDK

![](https://img.shields.io/badge/py_mini_racer-@0.6.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-yellow)

### 依赖于
- [ NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)
- [ NeteaseCloudMusicApi_V8 ](https://github.com/2061360308/NeteaseCloudMusicApi_V8)

### 原理
- 通过 `py_mini_racer` 调用 `NeteaseCloudMusicApi_V8` 的 `js` 方法。进一步进行了简单封装。

### 使用
- 克隆项目 `git clone git@github.com:2061360308/NeteaseCloudMusic_PythonSDK.git`
- 安装依赖 `pip install -r requirements.txt`
- 导入API进行使用(具体查看`test.py`中的示例)
```python
from main import NeteaseCloudMusicApi
import os

netease_cloud_music_api = NeteaseCloudMusicApi()  # 初始化API
netease_cloud_music_api.cookie = os.getenv("COOKIE")  # 设置cookie
response = netease_cloud_music_api.api("song_url_v1", {"id": 33894312, "level": "exhigh"})  # 调用API

```

> 注意： api(self, name, query=None) 的第一个参数为API名称，第二个参数为API参数，具体API名称和参数请参考 [NeteaseCloudMusicApi文档](https://docs.neteasecloudmusicapi.binaryify.com)，name支持`/song/url/v1`和`song_url_v1`两种写法。


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

> 精力有限，大部分API未测试，欢迎提交PR
