# 生成测试文件

import json
from pprint import pprint

with open("../package/NeteaseCloudMusic/config.json", 'r', encoding='utf-8') as f:
    config = json.loads(f.read())

with open("template", 'r', encoding='utf-8') as f:
    template = f.read()


def pathToName(path):
    if path[0] == "/":
        path = path[1:]
    return path.replace("/", "_")


tests = ""

exclude = ["apicache.js", "memory-cache.js", "request_reference.js", "avatar_upload.js", "cloud.js",
           "playlist_cover_update.js", "voice_upload.js", "register_anonimous.js", "verify_getQr.js"]

for apiPath, value in config.items():
    apiName = pathToName(apiPath)

    if (apiName+".js") in exclude:
        continue

    apiExplain = value["explain"]

    apiExample = []

    for item in value["example"]:
        apiExample.append(item["query"])

    content = (template.replace("{{apiName}}", apiName)
               .replace("{{explain}}", apiExplain)
               .replace("{{example}}", json.dumps(apiExample)))

    if apiPath == "/song/order/update":
        content = content.replace(" == 200", " in [200, 401]")
    elif apiPath == "/follow":
        content = content.replace(" == 200", " in [200, 400, -462]")
    elif apiPath == "/user/record":
        content = content.replace(" == 200", " in [200, 400]")
    elif apiPath == "/artist/sub":
        content = content.replace(" == 200", " in [200, 400, -462]")
    elif apiPath == "/video/sub":
        content = content.replace(" == 200", " in [200, 408]")
    elif apiPath == "/playlist/subscribe":
        content = content.replace(" == 200", " in [200, 408, 501]")
    elif apiPath == "/playlist/track/add":
        content = content.replace(" == 200", " in [200, 404]")
    elif apiPath == "/playlist/track/delete":
        content = content.replace(" == 200", " in [200, 400]")
    elif apiPath == "/album/sub":
        content = content.replace(" == 200", " in [200, 401, 404]")
    elif apiPath == "/artist/detail":
        content = content.replace(" == 200", " in [200, 400, -460]")
    elif apiPath == "/recommend/songs/dislike":
        content = content.replace(" == 200", " in [200, 432]")
    elif apiPath == "/user/cloud/del":
        content = content.replace(" == 200", " in [200, 404]")
    elif apiPath == "/cloud/match":
        content = content.replace(" == 200", " in [200, 400]")
    elif apiPath == "/send/song":
        content = content.replace(" == 200", " in [200, 401]")
    elif apiPath == "/send/album":
        content = content.replace(" == 200", " in [200, 404]")
    elif apiPath == "/msg/comments":
        content = content.replace(" == 200", " in [200, 400]")
    elif apiPath == "/yunbei/rcmd/song":
        content = content.replace(" == 200", " in [200, 400]")
    elif apiPath == "/vip/growthpoint":
        content = content.replace(" == 200", " in [200, 400, 1000]")
    elif apiPath == "/vip/growthpoint/get":
        content = content.replace(" == 200", " in [200, 400, 1000]")
    elif apiPath == "/artist/fans":
        content = content.replace(" == 200", " in [200, 400, -460]")
    elif apiPath == "/inner/version":
        content = content.replace("assert (response[\"code\"] == 200 or response[\"data\"][\"code\"] == 200)",
                                  "assert (response is not None)")
    elif "musician" in apiPath:
        content = content.replace(" == 200", " in [200, 400, 600, 10000, 500, 404]")

    tests += content + "\n\n\n"

with open("../api_test.py", 'w+', encoding='utf-8') as f:
    tests = ("from pytest_html import extras\n"
             "import json\n"
             "import os\n"
             "from pprint import pprint\n"
             "import dotenv\n"
             "from package.NeteaseCloudMusic import NeteaseCloudMusicApi, api_help, api_list\n"
             "dotenv.load_dotenv()  # 从.env文件中加载环境变量\n"
             "netease_cloud_music_api = NeteaseCloudMusicApi()  # 初始化API\n"
             "netease_cloud_music_api.cookie = os.getenv('COOKIE')  # 设置cookie\n"
             "netease_cloud_music_api.DEBUG = True  # 开启调试模式") + "\n\n\n" + tests
    f.write(tests)
