# NeteaseCloudMusic_PythonSDK

## 最新消息：***Binaryify/NeteaseCloudMusicApi*** 受到网易法律警告目前已删库且不再维护，该项目也被迫暂停维护

有关***Binaryify/NeteaseCloudMusicApi***最新版本的js其实已经改写完毕了，但是作者懒得继续写Python版本，有意向自己开发的可以扫码加入QQ频道讨论。当然也可以在频道讨论学习什么的。
<div align="center">
<img src="https://github.com/2061360308/NeteaseCloudMusic_PythonSDK/assets/42377282/95b1449d-1f0a-4f38-868b-b260911d82cb" height="260" />
</div>

现已同步原项目接口且测试通过的有200多个 :wave: :wave: :star: 求赞 :star:

![](https://img.shields.io/badge/py_mini_racer-@0.6.0-red.svg) ![License](https://img.shields.io/badge/license-MIT-yellow)[![PyPI Downloads](https://pepy.tech/badge/NeteaseCloudMusic)](https://pepy.tech/project/NeteaseCloudMusic)[![PyPI version](https://badge.fury.io/py/NeteaseCloudMusic.svg)](https://badge.fury.io/py/NeteaseCloudMusic)

> 基于 [NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi) 封装的 Python SDK。
> 网易云API Python版本。
> 已发布到PyPi，可直接使用pip安装。项目地址：[GitHub](https://github.com/2061360308/NeteaseCloudMusic_PythonSDK)
>
> 在此感谢`NeteaseCloudMusicApi`项目及其作者`Binaryify`
>
> 当然也感谢史上最最最好用的听歌软件——网易云音乐
>
> 项目仅用于学习，还望大家合理使用该项目

<div align="center">
<img src="./static/网易云.png" width="144" height="144" /><img src="./static/Python.jpg" width="144" height="144" /><img src="./static/Qt.jpg" width="144" height="144" /><img src="./static/idea.jpg" width="144" height="144" />
</div>

### :four_leaf_clover:项目背景

Binaryify 创建了有趣的项目[NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)提供了较为完善的网易云接口。

但是这个项目是基于Node服务器的，对于不懂Node或是服务器搭建的小伙伴来说不易于上手，而且开发出来的项目开源后也必须依赖于Node后端服务。

这样一来这些衍生的项目在介绍时就离不开告诉使用者“如何搭建后端等等的一系列操作”，增加了项目上手的难度。他人没法快速体验一番你的作品，需要先学习后端的搭建。

事实上，我们知道，除却在网页上独有的限制，只能依赖于服务器转发，在其他平台我们完全可以不需要服务器。

所以这个Python项目诞生了。 :joy: :joy: :joy:

### :heart:作者寄语

本项目使用Python开发，在我印象中这是一门非常活跃的语言，拥有一群怀揣许许多多“奇思妙想”的使用者。[NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)项目开源有好多年了，得到了3万颗星，无疑是一个优质的项目。但在此之前，我发现大多都是“前端们”使用前端技术（vue，electron）进行创作，这次我把这个接口项目封装到Python平台，相信我们的小伙伴们一定能为这个优质项目注入新的活力！

希望你们在开心创作的同时能够有不菲的收获。

<div align="center">
<img src="./static/wish.jpg" width="474" height="266" />
</div>

### :mushroom:项目用途

1. 仿网易云制作出专属于你的音乐软件
2. 赋予你的项目“音乐的力量”
3. 嗯，互联网上“下歌”，“获取歌词”，等等的炫酷操作你也能轻松实现了
4. 其他有待创新……

### :muscle:项目特点

- 完全封装于Python，不含其他知识点，不用自己处理网络请求，小白可用
- 不需要Node后端！！所有内容都封装到了库内部，可以随你的项目直接打包，其他人也可以直接下载体验，无需配置后端
- 发布到PyPI，简单使用
- 基于Python调用ECMScript，没有打包繁重的Node环境，体积小，效率高。

### 依赖于
- [ NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)
- [ NeteaseCloudMusicApi_V8 ](https://github.com/2061360308/NeteaseCloudMusicApi_V8)

### 项目原理
- 通过 `py_mini_racer` 调用 `NeteaseCloudMusicApi_V8` 的 `js` 方法。进一步进行了简单封装。

<div align="center">
<img src="./static/javascript.jpg" width="474" height="266" />
</div>

### :dragon_face:使用方法
- 安装 `pip install NeteaseCloudMusic`
- 导入API进行使用(具体查看[`example.py`](./example.py)中的示例)
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

> api已加入自动缓存（需要自己开启默认关闭），在测试接口时，如果频繁调用获取结果在query里应该加上timestamp参数来区分，例如
> ```python
> response = netease_cloud_music_api.request("song_url_v1", {"id": 33894312, "level": "exhigh", "timestamp": time.time()})
> ```

### :eyes:开发
如果想要参与项目开发，或是自己修改源码，请参照[开发指南](./docs/开发指南.md)。

### 测试

测试文件见[api_test.py](./api_test.py)，测试使用了`pytest`框架

测试结果请见[`report.html`](./report.html)

### :cherry_blossom:功能特性

> 项目初创，一些涉及上传东西的接口等还未进行支持，具体可见下方未支持的接口（急需某个未支持的接口可以发issue，我会优先解决）
>
> 接口文档具体参考原文档[NeteaseCloudMusicApi文档](https://docs.neteasecloudmusicapi.binaryify.com)

1. 登录
2. 刷新登录
3. 发送验证码
4. 校验验证码
5. 注册(修改密码)
6. 获取用户信息 , 歌单，收藏，mv, dj 数量
7. 获取用户歌单
8. 获取用户电台
9. 获取用户关注列表
10. 获取用户粉丝列表
11. 获取用户动态
12. 获取用户播放记录
13. 获取精品歌单
14. 获取歌单详情
15. 搜索
16. 搜索建议
17. 获取歌词
18. 歌曲评论
19. 收藏单曲到歌单
20. 专辑评论
21. 歌单评论
22. mv 评论
23. 电台节目评论
24. banner
25. 获取歌曲详情
26. 获取专辑内容
27. 获取歌手单曲
28. 获取歌手 mv
29. 获取歌手专辑
30. 获取歌手描述
31. 获取相似歌手
32. 获取相似歌单
33. 相似 mv
34. 获取相似音乐
35. 获取最近 5 个听了这首歌的用户
36. 获取每日推荐歌单
37. 获取每日推荐歌曲
38. 私人 FM
39. 签到
40. 喜欢音乐
41. 垃圾桶
42. 歌单 ( 网友精选碟 )
43. 新碟上架
44. 热门歌手
45. 最新 mv
46. 推荐 mv
47. 推荐歌单
48. 推荐新音乐
49. 推荐电台
50. 推荐节目
51. 独家放送
52. mv 排行
53. 获取 mv 数据
54. 播放 mv/视频
55. 排行榜
56. 歌手榜
57. 云盘
58. 电台 - 推荐
59. 电台 - 分类
60. 电台 - 分类推荐
61. 电台 - 订阅
62. 电台 - 详情
63. 电台 - 节目
64. 给评论点赞
65. 获取动态
66. 热搜列表(简略)
67. 发送私信
68. 发送私信歌单
69. 新建歌单
70. 收藏/取消收藏歌单
71. 歌单分类
72. 收藏的歌手列表
73. 订阅的电台列表
74. 相关歌单推荐
75. 付费精选接口
76. 音乐是否可用检查接口
77. 登录状态
78. 获取视频播放地址
79. 发送/删除评论
80. 热门评论
81. 视频评论
82. 退出登录
83. 所有榜单
84. 所有榜单内容摘要
85. 收藏视频
86. 收藏 MV
87. 视频详情
88. 相关视频
89. 关注用户
90. 新歌速递
91. 喜欢音乐列表(无序)
92. 收藏的 MV 列表
93. 获取最新专辑
94. 听歌打卡
95. 获取视频标签/分类下的视频
96. 已收藏专辑列表
97. 获取动态评论
98. 歌单收藏者列表
99. 云盘歌曲删除
100. 热门话题
101. 电台 - 推荐类型
102. 电台 - 非热门类型
103. 电台 - 今日优选
104. 心动模式/智能播放
105. 转发动态
106. 删除动态
107. 分享歌曲、歌单、mv、电台、电台节目到动态
108. 通知-私信
109. 通知-评论
110. 通知-@我
111. 通知-通知
112. 设置
113. 云盘数据详情
114. 私信内容
115. 我的数字专辑
116. batch批量请求接口
117. 获取视频标签列表
118. 全部mv
119. 网易出品mv
120. 收藏/取消收藏专辑
121. 专辑动态信息
122. 热搜列表(详细)
123. 更换绑定手机
124. 检测手机号码是否已注册
125. 初始化昵称
126. 更新歌单描述
127. 更新歌单名
128. 更新歌单标签
129. 默认搜索关键词
130. 删除歌单
131. 电台banner
132. 用户电台
133. 热门电台
134. 电台 - 节目详情
135. 电台 - 节目榜
136. 电台 - 新晋电台榜/热门电台榜
137. 类别热门电台
138. 云村热评
139. 电台24小时节目榜
140. 电台24小时主播榜
141. 电台最热主播榜
142. 电台主播新人榜
143. 电台付费精品榜
144. 歌手热门50首歌曲
145. 购买数字专辑
146. 获取 mv 点赞转发评论数数据
147. 获取视频点赞转发评论数数据
148. 调整歌单顺序
149. 调整歌曲顺序
150. 独家放送列表
151. 获取推荐视频
152. 获取视频分类列表 
153. 获取全部视频列表接口
154. 获取历史日推可用日期列表
155. 获取历史日推详细数据
156. 国家编码列表
157. 首页-发现
158. 首页-发现-圆形图标入口列表
159. 数字专辑-全部新碟
160. 数字专辑-热门新碟
161. 数字专辑&数字单曲-榜单
162. 数字专辑-语种风格馆
163. 数字专辑详情
164. 更新头像
165. 歌单封面上传
166. 楼层评论
167. 歌手全部歌曲
168. 精品歌单标签列表
169. 用户等级信息
170. 电台个性推荐
171. 用户绑定信息
172. 用户绑定手机
173. 新版评论
174. 点赞过的视频
175. 收藏视频到视频歌单
176. 删除视频歌单里的视频
177. 最近播放的视频
178. 音乐日历
179. 电台订阅者列表
180. 云贝签到信息
181. 云贝签到
182. 云贝所有任务
183. 云贝todo任务
184. 云贝今日签到信息
185. 云贝完成任务
186. 云贝收入
187. 云贝支出
188. 云贝账户信息
189. 账号信息
190. 最近联系人
191. 私信音乐
192. 抱一抱评论
193. 评论抱一抱列表
194. 收藏的专栏
195. 关注歌手新歌
196. 关注歌手新MV
197. 歌手详情
198. 云盘上传
199. 二维码登录
200. 话题详情
201. 话题详情热门动态
202. 歌单详情动态
203. 绑定手机
204. 一起听状态
205. 用户历史评论
206. 云盘歌曲信息匹配纠正
207. 云贝推歌
208. 云贝推歌历史记录
209. 已购单曲
210. 获取mlog播放地址
211. 将mlog id转为视频id
212. vip成长值
213. vip成长值获取记录
214. vip任务
215. 领取vip成长值
216. 歌手粉丝
217. 数字专辑详情
218. 数字专辑销量
219. 音乐人数据概况
220. 音乐人播放趋势
221. 音乐人任务
222. 账号云豆数
223. 领取云豆
224. 获取 VIP 信息
225. 音乐人签到
226. 发送文本动态
227. 获取客户端歌曲下载 url
228. 获取歌单所有歌曲
229. 乐签信息
230. 最近播放-歌曲
231. 最近播放-视频
232. 最近播放-声音
233. 最近播放-歌单
234. 最近播放-专辑
235. 最近播放-播客
236. 签到进度
237. 重复昵称检测
238. 歌手粉丝数量
239. 音乐人任务(新)
240. 内部版本接口
241. 歌单更新播放量
242. 黑胶时光机
243. 音乐百科 - 简要信息
244. 乐谱列表
245. 乐谱内容
246. 曲风列表
247. 曲风偏好
248. 曲风详情
249. 曲风-歌曲
250. 曲风-专辑
251. 曲风-歌单
252. 曲风-歌手
253. 私信和通知接口
254. 回忆坐标
255. 播客搜索
256. 播客声音上传
257. 验证接口-二维码生成
258. 验证接口-二维码检测
259. 听歌识曲
260. 根据nickname获取userid接口
261. 播客声音列表
262. 专辑简要百科信息
263. 歌曲简要百科信息
264. 歌手简要百科信息
265. mv简要百科信息
266. 搜索歌手
267. 用户贡献内容
268. 用户贡献条目、积分、云贝数量
269. 年度听歌报告
270. 播客声音搜索

### 改进
> 下列API未支持
>
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
