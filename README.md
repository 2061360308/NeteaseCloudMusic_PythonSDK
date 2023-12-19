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
- 导入API进行使用(具体查看`example.py`中的示例)
```python
from NeteaseCloudMusic import NeteaseCloudMusicApi, api_help, api_list
import os

netease_cloud_music_api = NeteaseCloudMusicApi()  # 初始化API
netease_cloud_music_api.cookie = "你的cookie"  # 设置cookie， 如果没有cookie需要先登录 具体见example.py
response = netease_cloud_music_api.request("song_url_v1", {"id": 33894312, "level": "exhigh"})  # 调用API

# 获取帮助
print(api_help())
print(api_help('song_url_v1'))
# 获取API列表
print(api_list())
```

> 注意： request(self, name, query=None) 的第一个参数为API名称，第二个参数为API参数，具体API名称和参数请参考 [NeteaseCloudMusicApi文档](https://docs.neteasecloudmusicapi.binaryify.com)，name支持`/song/url/v1`和`song_url_v1`两种写法。

> api已加入自动缓存，在测试接口时，如果频繁调用获取结果在query里应该加上timestamp参数来区分，例如
> ```python
> response = netease_cloud_music_api.request("song_url_v1", {"id": 33894312, "level": "exhigh", "timestamp": time.time()})
> ```

### 开发
- 克隆项目 `git clone git@github.com:2061360308/NeteaseCloudMusic_PythonSDK.git`
- 安装依赖 `pip install -r requirements.txt`
- 目录/文件说明
```
├── package  项目包根目录
├── test_gender  生成测试代码的脚本
├── test.py  手动测试/ 使用示例
```

#### 更新
项目使用towncrier自动生成更新日志

在 newsfragments 目录下，创建一个新的文本文件。这个文件的名字应该是一个唯一的编号，后缀是 .rst。
例如，如果你正在处理编号为 123 的问题，你可以创建一个名为 123.feature.rst 的文件。

注意在 towncrier 中，新闻片段的类型通常由文件名的后缀决定。以下是一些常见的新闻片段类型：
- .feature: 用于描述新的特性或者功能。
- .bugfix: 用于描述一个 bug 修复。
- .doc: 用于描述文档的更改。
- .removal: 用于描述移除的特性或者功能。
- .misc: 用于描述其他类型的更改。
- 
在这个文件中，写下你的更改的描述。这个描述应该是简短的，通常只有一到两句话。
例如`Added support for the XYZ feature.`

#### 发布新版本
自动：
运行 python publish.py

手动：
使用bumpversion自动更新版本号，提交并发布标签
你需要安装bumpversion然后执行
```bash
bumpversion patch  # for a patch level increase (e.g., 1.0.0 to 1.0.1)
bumpversion minor  # for a minor level increase (e.g., 1.0.0 to 1.1.0)
bumpversion major  # for a major level increase (e.g., 1.0.0 to 2.0.0)
```

接下来会自动更新版本号并提交到远程仓库，然后发布一个新的标签
workflow会依据标签自动发布相应资源并且发布到pypi

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

更正request库返回多个cookie时自动用分号拼接导致后续cookie不好解析的问题
添加了对cookie中Max-Age为0的处理
改进判断cookie是否过期的逻辑
添加了自动处理cookie的更新操作
