import ctypes
from ctypes import CDLL, Structure, c_char_p, c_void_p, c_int, POINTER
from .core import (
    load_kugou,
    engine,
    _Engine,
    _KugouProcessEnv as KugouProcessEnv,
    _Platform as Platform,
    _KugouContextManager,
)
from .common import to_bytes, Response
import json
from enum import Enum

__all__ = ["KuGouMusicApi", "KugouProcessEnv"]


class KuGouMusicApi:
    def __init__(self, env: KugouProcessEnv = None):
        self.kugou = load_kugou()

        _Engine()
        _KugouContextManager.init(env)
        self.env = env or _KugouContextManager._env
        self.ctx = _KugouContextManager.get_ctx()
        self._destroyed = False

    def request(self, path, cookie="", env: KugouProcessEnv = None, **query) -> Response:
        if env is None:
            env = self.env

        # 剔除值为 None 的参数
        print(f"Original query: {query}")
        query = {k: v for k, v in query.items() if v is not None}
        query = json.dumps(query) if query else ""

        path = to_bytes(path)
        query = to_bytes(query)
        cookie = to_bytes(cookie)

        ptr = self.kugou.kugou_request(
            self.ctx,
            path,
            cookie,
            query,
            ctypes.byref(env),
        )
        if ptr:
            result = ctypes.cast(ptr, ctypes.c_char_p).value
            res_str = result.decode("utf-8")
            engine.response_free(ptr)
            return Response(res_str)
        return Response(status="error", body="Failed to get response")

    def destroy(self):
        if not self._destroyed:
            try:
                engine.destroy_context(self.ctx)
                self._destroyed = True
            except Exception as e:
                # 可根据需要打印日志或忽略
                # Todo
                pass

    def __del__(self):
        self.destroy()

    def login_token(self, token=None, userid=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        刷新登录
        说明 : 调用此接口，可刷新登录状态，可以延长 token 过期时间
        可选参数：
        token: 登录后获取的 token
        userid: 用户 id
        接口地址： /login/token
        调用例子： /login/token /login/token?token=xxx&userid=xxx
        '''
        return self.request("/login/token", cookie, env, token=token, userid=userid)
    def captcha_sent(self, mobile, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        发送验证码
        说明: 调用此接口 ,传入手机号码, 可发送验证码
        必选参数：
        mobile: 手机号码
        接口地址： /captcha/sent
        调用例子： /captcha/sent?mobile=xxx
        '''
        return self.request("/captcha/sent", cookie, env, mobile=mobile)
    def register_dev(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        dfid 获取
        接口地址： /register/dev
        调用例子： /register/dev
        '''
        return self.request("/register/dev", cookie, env)
    def user_detail(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取用户额外信息
        说明：登陆后调用此接口，可以获取用户额外信息
        接口地址： /user/detail
        '''
        return self.request("/user/detail", cookie, env)
    def user_vip_detail(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取用户 vip 信息
        说明：登陆后调用此接口，可以获取用户 vip 信息
        接口地址： /user/vip/detail
        '''
        return self.request("/user/vip/detail", cookie, env)
    def user_playlist(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取用户歌单
        说明：登录后调用此接口，可以获取用户的所有创建以及收藏的歌单
        可选参数：
        page：页数
        pagesize : 每页页数, 默认为 30
        接口地址： /user/playlist
        调用例子： /user/playlist
        '''
        return self.request("/user/playlist", cookie, env)
    def user_follow(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取用户关注歌手
        说明：登录后调用此接口，可以获取用户的所有关注的歌手/用户
        接口地址： /user/follow
        调用例子： /user/follow
        '''
        return self.request("/user/follow", cookie, env)
    def user_cloud(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取用户云盘
        说明：登录后调用此接口可以获取用户上传到云盘的音乐（需要登录）
        可选参数
        page : 页数
        pagesize : 每页页数, 默认为 30
        接口地址： /user/cloud
        调用例子： /user/cloud
        '''
        return self.request("/user/cloud", cookie, env)
    def user_cloud_url(self, hash, album_id=None, name=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取用户云盘音乐 URL
        说明：登录后调用此接口可以获取用户上传到云盘的音乐 URL，部分可以直接用 /song/url 直接获取 URL（需要登录，目前获取到的文件大小都约为 10M 左右）
        必选参数：
        hash: 音乐 hash
        可选参数：
        album_id: 专辑 id
        name: 云盘音乐名称
        album_audio_id：专辑音频 id
        接口地址： /user/cloud/url
        调用例子： /user/cloud/url
        '''
        return self.request("/user/cloud/url", cookie, env, hash=hash, album_id=album_id, name=name)
    def user_video_collect(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取用户收藏的视频
        说明：登录后调用此接口可以获取用户收藏的视频（需要登录）
        可选参数
        page : 页数
        pagesize : 每页页数, 默认为 30
        接口地址： /user/video/collect
        调用例子： /user/video/collect
        '''
        return self.request("/user/video/collect", cookie, env)
    def user_video_love(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取用户喜欢的视频
        说明：登录后调用此接口可以获取用户喜欢的视频（需要登录）
        可选参数
        pagesize : 每页页数, 默认为 30
        接口地址： /user/video/love
        调用例子： /user/video/love
        '''
        return self.request("/user/video/love", cookie, env)
    def user_listen(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取用户听歌历史排行
        说明：登录后调用此接口，可以获取用户听歌历史排行
        可选参数：
        type：0 为获取最近一周前 120 首歌曲，1：获取全部累计前 120 首歌曲
        接口地址： /user/listen
        调用例子： /user/listen
        '''
        return self.request("/user/listen", cookie, env)
    def user_history(self, bp=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取用户最近听歌历史
        说明：登录后调用此接口，可以近期的听歌历史记录(需要登陆)
        可选参数：
        bp: 可以更加上一次返回值传入
        接口地址： /user/history
        调用例子： /user/history
        '''
        return self.request("/user/history", cookie, env, bp=bp)
    def lastest_songs_listen(self, pagesize=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取继续播放信息（对应手机版首页显示继续播放入口）
        说明：登录后调用此接口，可以最后设备播放信息(需要登陆)
        可选参数：
        pagesize: 每页页数, 默认为 30
        接口地址： /lastest/songs/listen
        调用例子： /lastest/songs/listen
        '''
        return self.request("/lastest/songs/listen", cookie, env, pagesize=pagesize)
    def playlist_add(self, name, list_create_userid, list_create_listid, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        收藏歌单/新建歌单
        说明 : 调用此接口, 可收藏歌单/新建歌单( 需要登录 ), 收藏成功后建议使用 [/playlist/tracks/add](#对歌单添加歌曲) 把原歌单下的歌曲添加到新的歌单
        必选参数：
        name: 歌单名称
        list_create_userid: 歌单 list_create_userid
        list_create_listid: 歌单 list_create_listid
        可选参数
        is_pri: 是否设为隐私，0：公开，1：隐私，仅支持创建歌单时传入
        type: 1：为收藏歌单，0：创建歌单, 默认为 0
        list_create_gid：歌单 list_create_gid
        接口地址： /playlist/add
        调用例子： /playlist/add?source=1&name=音乐一响%20纯爱登场.&list_create_userid=1782943844&list_create_listid=87
        '''
        return self.request("/playlist/add", cookie, env, name=name, list_create_userid=list_create_userid, list_create_listid=list_create_listid)
    def playlist_del(self, listid, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        取消收藏歌单/删除歌单
        说明 : 调用此接口 , 取消收藏歌单( 需要登录 )
        必选参数：
        listid: 用户歌单 listid
        接口地址： /playlist/del
        接口地址： /playlist/del?listid=xxx
        '''
        return self.request("/playlist/del", cookie, env, listid=listid)
    def playlist_tracks_add(self, listid, data, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        对歌单添加歌曲
        说明 : 调用此接口 , 可以添加歌曲到歌单 ( 需要登录 )
        必选参数：
        listid: 用户歌单 listid
        data: 歌曲数据, 格式为 歌曲名称|歌曲 hash|专辑 id|(mixsongid/album_audio_id)，最少需要 歌曲名称以及歌曲 hash(若返回错误则需要全部参数)， 支持多个，每
        个以逗号分隔
        接口地址： /playlist/tracks/add
        调用例子： /playlist/tracks/add?listid=1&data=我们应该算爱过吧|8E10D8825DDE03BCABBDE13E5A4150D2
        /playlist/tracks/add?listid=1&data=我们应该算爱过吧|8E10D8825DDE03BCABBDE13E5A4150D2|67026620|477417208
        /playlist/tracks/add?listid=1&data=我们应该算爱过吧|8E10D8825DDE03BCABBDE13E5A4150D2,我们应该算爱过吧|5015FC3FAB5B0C245556A1CC3C4DE355
        '''
        return self.request("/playlist/tracks/add", cookie, env, listid=listid, data=data)
    def playlist_tracks_del(self, listid, fileids, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        对歌单删除歌曲
        说明 : 调用此接口 , 可以删除歌单某首歌曲 ( 需要登录 )
        必选参数：
        listid: 用户歌单 listid
        fileids: 歌单中歌曲的 fileid，可多个,用逗号隔开
        接口地址： /playlist/tracks/del
        调用例子： /playlist/tracks/del?listid=1&fileids=xx /playlist/tracks/del?listid=1&fileids=xx,xx
        '''
        return self.request("/playlist/tracks/del", cookie, env, listid=listid, fileids=fileids)
    def top_album(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        新碟上架
        说明: 调用此接口 , 可获取新碟上架列表, 如需要专辑详细信息需要调用[album/detail](#专辑详情), 如需要获取专辑音乐列表需调
        用[album/songs](#专辑音乐列表)
        可选参数：
        type : 1：华语；2：欧美；3：日本；4：韩国；推荐为空，默认为空
        page : 页数
        pagesize : 每页页数, 默认为 30
        接口地址： /top/album
        调用例子： /top/album
        '''
        return self.request("/top/album", cookie, env)
    def album(self, album_id, fields=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        专辑信息
        说明: 调用此接口 ,传入专辑 id 可获取专辑相关信息
        必选参数：
        album_id: 专辑 id,可以传多个，以逗号分割
        可选参数：
        fields: 需要返回的信息，可以传多个，以逗号分割，支持的值有 trans_param special_tag authors album_name publish_date cover intro
        publish_company type album_id language_id is_publish heat grade quality exclusive grade_count author_name sizable_cover
        language category
        接口地址： /album
        调用例子： /album?album_id=xxx, /album?album_id=xxx,xxx, /album?album_id=xxx&fields=language,authors
        '''
        return self.request("/album", cookie, env, album_id=album_id, fields=fields)
    def album_detail(self, id, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        专辑详情
        说明: 调用此接口 ,传入专辑 id 可获取专辑详情
        必选参数：
        id: 专辑 id
        接口地址： /album/detail
        调用例子： /album/detail?id=10729818
        '''
        return self.request("/album/detail", cookie, env, id=id)
    def album_songs(self, id, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        专辑音乐列表
        说明: 调用此接口 ,传入专辑 id 可获取专辑音乐列表
        必选参数：
        id: 专辑 id
        可选参数：
        page : 页数
        pagesize : 每页页数, 默认为 30
        接口地址： /album/songs
        调用例子： /album/songs?id=10729818
        '''
        return self.request("/album/songs", cookie, env, id=id)
    def song_url(self, hash, album_id=None, free_part=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取音乐 URL
        说明: 调用此接口, 传入的音乐 hash, 可以获取对应的音乐的 url, 未登录状态或者非会员可能会返回为空。
        ⚠️ 注意：因接口问题，目前获取 url 接口数据需要先调用 /register/dev 接口获取 dfid，否则会提示 本次请求需要验证
        必选参数：
        hash: 音乐 hash
        可选参数：
        album_id: 专辑 id
        free_part: 是否返回试听部分（仅部分歌曲）
        album_audio_id：专辑音频 id
        quality：获取不同音质的 url
        quality 支持的参数
        piano：对应手机端魔法音乐 钢琴，仅部分音乐支持
        acappella：对应手机端魔法音乐 人声 伴奏，仅部分音乐支持，该模式下返回的音频后缀为 mkv 格式，该文加存在 人声 和 伴奏 两个音轨
        subwoofer：对应手机端魔法音乐 骨笛，仅部分音乐支持
        ancient：对应手机端魔法音乐 尤克里里，仅部分音乐支持
        surnay：对应手机端魔法音乐 唢呐，仅部分音乐支持
        dj：对应手机端魔法音乐 DJ，仅部分音乐支持
        128：返回 128 码率 mp3 格式
        320：返回 320 码率 mp3 格式
        flac：返回 flac 格式音频
        high：返回无损格式音频
        viper_atmos：蝰蛇全景声，仅部分音乐支持
        viper_clear：蝰蛇超清音质
        viper_tape：蝰蛇母带，仅部分音乐支持, 该音质需要转码，关于转码相关的技术还不会
        接口地址： /song/url
        调用例子： /song/url?hash=xxx
        '''
        return self.request("/song/url", cookie, env, hash=hash, album_id=album_id, free_part=free_part)
    def song_url_new(self, hash, free_part=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取音乐 URL（新版）
        说明: 调用此接口, 传入的音乐 hash, 可以获取对应的音乐的 url, 未登录状态或者非会员可能会返回为空，该接口会一次性返回支持的音质的音频 url, 但该接口存
        在音频加密（目前无法解码），请谨慎使用
        ⚠️ 注意：因接口问题，目前获取 url 接口数据需要先调用 /register/dev 接口获取 dfid，否则会提示 本次请求需要验证
        必选参数：
        hash: 音乐 hash
        可选参数：
        album_audio_id：专辑音频 id
        free_part: 是否返回试听部分（仅部分歌曲）
        album_audio_id：专辑音频 id
        接口地址： /song/url/new
        调用例子： /song/url/new?hash=xxx
        '''
        return self.request("/song/url/new", cookie, env, hash=hash, free_part=free_part)
    def song_climax(self, hash, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取歌曲高潮部分
        说明: 调用此接口, 传入的音乐 hash, 可以获取对应的音乐的高潮时间
        必选参数：
        hash: 音乐 hash, 可以传多个，以逗号分割
        接口地址： /song/climax
        调用例子： /song/climax?hash=xxx
        '''
        return self.request("/song/climax", cookie, env, hash=hash)
    def search(self, keywords, type=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        搜索
        说明: 调用此接口 , 传入搜索关键词可以搜索该音乐 / mv / 歌单 / 歌词 / 专辑 / 歌手
        必选参数：
        keywords: 关键词
        可选参数：
        page : 页数
        pagesize : 每页页数, 默认为 30
        type: 搜索类型；默认为单曲，special：歌单，lyric：歌词，song：单曲，album：专辑，author：歌手，mv：mv
        接口地址： /search
        调用例子： /search?keywords=海阔天空
        '''
        return self.request("/search", cookie, env, keywords=keywords, type=type)
    def search_default(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        默认搜索关键词
        说明 : 调用此接口 , 可获取默认搜索关键词
        接口地址： /search/default
        '''
        return self.request("/search/default", cookie, env)
    def search_complex(self, keywords, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        综合搜索
        说明: 调用此接口, 传入搜索关键词可以获得综合搜索，搜索结果同时包含单曲 , 歌手 , 歌单等信息
        必选参数：
        keywords: 关键词
        可选参数：
        page : 页数
        pagesize : 每页页数, 默认为 30
        接口地址： /search/complex
        调用例子： /search/complex?keywords=海阔天空
        '''
        return self.request("/search/complex", cookie, env, keywords=keywords)
    def search_hot(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        热搜列表
        说明 : 调用此接口,可获取热门搜索列表
        接口地址： /search/hot
        调用例子： /search/hot
        '''
        return self.request("/search/hot", cookie, env)
    def search_suggest(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        搜索建议
        说明 : 调用此接口 , 传入搜索关键词可获得搜索建议 , 搜索结果同时包含单曲 , 歌手 , 歌单信息
        可选参数：
        albumTipCount : 专辑返回数量
        correctTipCount : 目前未知，可能是歌单
        mvTipCount : MV 返回数量
        musicTipCount : 音乐返回数量
        接口地址： /search/suggest
        调用例子： /search/suggest?keywords=海阔天空
        '''
        return self.request("/search/suggest", cookie, env)
    def search_lyric(self, keywords, hash, album_audio_id=None, man=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        歌词搜索
        说明: 调用此接口, 可以搜索歌词，该接口需配合 [/lyric](#获取歌词) 使用。
        必选参数：
        keywords: 关键词，与 hash 二选一
        hash: 歌曲 hash，与 keyword 二选一
        可选参数：
        album_audio_id: 专辑音乐 id,
        man: 是否返回多个歌词，yes：返回多个， no：返回一个。 默认为no
        接口地址： /search/lyric
        调用例子： /search/lyric?keywords=xxx /search/lyric?keywords=xxx&hash=xxx
        '''
        return self.request("/search/lyric", cookie, env, keywords=keywords, hash=hash, album_audio_id=album_audio_id, man=man)
    def lyric(self, id, accesskey, fmt=None, decode=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取歌词
        说明 : 调用此接口，可以获取歌词，调用该接口前则需要调用[/search/lyric](#歌词搜索) 获取完整参数
        必选参数：
        id: 歌词 id, 可以从 [/search/lyric](#歌词搜搜) 接口中获取
        accesskey: 歌词 accesskey, 可以从 [/search/lyric](#歌词搜搜) 接口中获取
        可选参数：
        fmt: 歌词类型，lrc 为普通歌词，krc 为逐字歌词
        decode: 是否解码，传入该参数这返回解码后的歌词
        接口地址： /lyric
        调用例子： /lyric?id=xxx&accesskey=xxx /lyric?id=xxx&accesskey=xxx&fmt=lrc /lyric?id=xxx&accesskey=xxx&decode=true
        '''
        return self.request("/lyric", cookie, env, id=id, accesskey=accesskey, fmt=fmt, decode=decode)
    def playlist_tags(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        歌单分类
        说明 : 调用此接口,可获取歌单分类,包含 category 信息
        接口地址： /playlist/tags
        调用例子： /playlist/tags
        '''
        return self.request("/playlist/tags", cookie, env)
    def top_playlist(self, category_id, withsong=None, withtag=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        歌单
        说明 : 调用此接口 , 可获取歌单
        必选参数：
        category_id: tag，0：推荐，11292：HI-RES，其他可以从 [/playlist/tags](#歌单分类) 接口中获取（接口下的 tag_id 为 category_id的值）
        可选参数：
        withsong: 是否返回歌曲列表（不全），0：不返回，1：返回
        withtag: 是否返回歌单分类，0：不返回，1：返回
        接口地址： /top/playlist
        调用例子： /top/playlist?category_id=0
        '''
        return self.request("/top/playlist", cookie, env, category_id=category_id, withsong=withsong, withtag=withtag)
    def theme_playlist(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        主题歌单
        说明 : 调用此接口 , 可获取主题歌单, 通过 [/theme/playlist/track](#获取主题歌单所有歌曲) 可以获取主题个单下的歌曲
        接口地址： /theme/playlist
        调用例子： /theme/playlist
        '''
        return self.request("/theme/playlist", cookie, env)
    def playlist_effect(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        音效歌单
        说明 : 调用此接口 , 可获取音效歌单
        可选参数：
        page : 页数
        pagesize : 每页页数, 默认为 30
        接口地址： /playlist/effect
        调用例子： /playlist/effect
        '''
        return self.request("/playlist/effect", cookie, env)
    def playlist_detail(self, ids, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取歌单详情
        说明: 调用此接口 , 可获取歌单详细信息
        必选参数：
        ids: 歌单中的 global_collection_id，可以传多个，用逗号分隔
        接口地址： /playlist/detail
        调用例子： /playlist/detail?ids=collection_3_1863870844_4_0 /playlist/detail?ids=collection_3_1863870844_4_0,collection_3_2093906551_8_0
        '''
        return self.request("/playlist/detail", cookie, env, ids=ids)
    def playlist_track_all(self, id, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取歌单所有歌曲
        说明 : 调用此接口，传入对应的歌单 global_collection_id，即可获得对应的所有歌曲
        必选参数：
        id: 歌单中的 global_collection_id
        可选参数：
        page : 页数
        pagesize : 每页页数, 默认为 30
        接口地址： /playlist/track/all
        调用例子： /playlist/track/all?id=collection_3_1863870844_4_0
        '''
        return self.request("/playlist/track/all", cookie, env, id=id)
    def playlist_track_all_new(self, lisdid, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取歌单所有歌曲(新版)
        说明 : 调用此接口，传入对应的歌单 listid，即可获得对应的所有歌曲, 目前该接口仅支持 用户所创建及收藏的歌单
        必选参数：
        lisdid: 歌单中的 listid
        可选参数：
        page : 页数
        pagesize : 每页页数, 默认为 30
        接口地址： /playlist/track/all/new
        调用例子： /playlist/track/all/new?listid=xxx
        '''
        return self.request("/playlist/track/all/new", cookie, env, lisdid=lisdid)
    def playlist_similar(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        相似歌单
        说明 : 调用此接口，根据歌单 id 获取相似歌单
        必选参数：
        ids：歌单 global_collection_id，支持多个，每个以逗号分隔
        接口地址： /playlist/similar
        调用例子： /playlist/similar?ids=collection_1_1341266283_964007_0
        /playlist/similar?ids=collection_1_1341266283_964007_0,collection_3_1041185112_11_0
        '''
        return self.request("/playlist/similar", cookie, env)
    def theme_playlist_track(self, theme_id, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取主题歌单所有歌曲
        必选参数：
        theme_id: 主题歌单 id
        接口地址： /theme/playlist/track
        调用例子： /theme/playlist/track?theme_id=18
        '''
        return self.request("/theme/playlist/track", cookie, env, theme_id=theme_id)
    def theme_music(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取主题音乐
        说明 : 调用此接口，可以获取主题音乐，调用 [/theme/music/detail](#) 可以获取主题音乐详情
        接口地址： /theme/music
        调用例子： /theme/music
        '''
        return self.request("/theme/music", cookie, env)
    def theme_music_detail(self, id, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取主题音乐详情
        说明 : 调用此接口，传入对应的主题 id 可以获取主题音乐详情.
        必选参数：
        id: 主题音乐 id
        接口地址： /theme/music/detail
        调用例子： /theme/music/detail?id=1002
        '''
        return self.request("/theme/music/detail", cookie, env, id=id)
    def top_card(self, card_id, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        歌曲推荐
        说明 : 调用此接口，可以获取歌曲推荐.
        必选参数：
        card_id: 1：对应安卓 精选好歌随心听 || 私人专属好歌，2：对应安卓 经典怀旧金曲，3：对应安卓 热门好歌精选，4：对应安卓 小众宝藏佳作，5：未知，6：对应
        vip 专属推荐
        接口地址： /top/card
        调用例子： /top/card?card_id=1
        '''
        return self.request("/top/card", cookie, env, card_id=card_id)
    def top_card(self, card_id, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        歌曲推荐（概念版）
        说明 : 调用此接口，可以获取歌曲推荐
        必选参数：
        card_id: 3006: VIP 专属推荐，3001: 私人专属好歌，3004: 小众宝藏佳作，3014: 喜欢这首歌的 TA 也喜欢，3101: 概念 er 新推，3005: 潮流尝鲜
        可选参数
        pagesize: 每页页数, 默认为 30
        接口地址： /top/card
        调用例子： /top/card/youth?card_id=3006
        '''
        return self.request("/top/card", cookie, env, card_id=card_id)
    def images(self, hash, album_id=None, album_audio_id=None, count=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取歌手和专辑图片
        说明 : 调用此接口，可以获取歌手和专辑图片.
        必选参数：
        hash: 歌曲 hash, 可以传多个，每个以逗号分开
        可选参数：
        album_id: 专辑 id, 可以传多个，每个以逗号分开
        album_audio_id: 专辑音乐 id, 可以传多个，每个以逗号分开
        count: 最多返回多少张图片，默认为 5
        接口地址： /images
        调用例子： /images?hash=B04ED0F01ABBB62B9D22EC4616ED8AFE
        /image?hash=B04ED0F01ABBB62B9D22EC4616ED8AFE,55603312694BF99AD6000C2D0D72D368&album_id=,75013431
        '''
        return self.request("/images", cookie, env, hash=hash, album_id=album_id, album_audio_id=album_audio_id, count=count)
    def images_audio(self, hash, audio_id=None, album_audio_id=None, filename=None, count=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取歌手图片
        说明 : 调用此接口，可以获取歌手图片.
        必选参数：
        hash: 歌曲 hash, 可以传多个，每个以逗号分开
        可选参数：
        audio_id: 音乐 id, 可以传多个，每个以逗号分开
        album_audio_id: 专辑音乐 id, 可以传多个，每个以逗号分开
        filename: 音乐文件名称, 可以传多个，每个以逗号分开
        count: 最多返回多少张图片，默认为 5
        接口地址： /images/audio
        调用例子： /images/audio?hash=B04ED0F01ABBB62B9D22EC4616ED8AFE
        /image/audio?hash=B04ED0F01ABBB62B9D22EC4616ED8AFE,55603312694BF99AD6000C2D0D72D368
        '''
        return self.request("/images/audio", cookie, env, hash=hash, audio_id=audio_id, album_audio_id=album_audio_id, filename=filename, count=count)
    def audio(self, hash, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取音乐相关信息
        说明：调用此接口，可以获取音乐相关信息
        必选参数：
        hash: 歌曲 hash, 可以传多个，每个以逗号分开
        接口地址： /audio
        调用例子： /audio?hash=B04ED0F01ABBB62B9D22EC4616ED8AFE /audio?hash=B04ED0F01ABBB62B9D22EC4616ED8AFE,55603312694BF99AD6000C2D0D72D368
        '''
        return self.request("/audio", cookie, env, hash=hash)
    def audio_related(self, pagesize=None, type=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取更多音乐版本
        说明：调用此接口，可以获取更多版本音乐
        必选参数：
        album_audio_id：音乐的 mixsongid/album_audio_id
        可选参数：
        page： 页码
        pagesize: 每页页数, 默认为 30
        show_type：是否返回分类
        sort：排序，支持 all，hot，new
        type: 分类
        show_detail：是否返回详情，否则只返回总数，0：只返回总数，不传或者其他都返回详情
        接口地址： /audio/related
        调用例子： /audio/related?album_audio_id=573120919 /audio/related?album_audio_id=573120919&show_detail=0
        '''
        return self.request("/audio/related", cookie, env, pagesize=pagesize, type=type)
    def audio_accompany_matching(self, fileName, mixid, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取音乐伴奏信息
        说明：调用此接口，可以获取最佳伴奏信息
        必选参数：
        hash：音乐 hash
        fileName: 音乐 fileName
        mixid: 音乐的 mixsongid/album_audio_id
        接口地址： /audio/accompany/matching
        调用例子： /audio/accompany/matching?fileName=希林娜依高 - Shine Brighter (愈加璀璨)&mixId=637735200&hash=6D431B0507587447B3D7345434DC5825
        '''
        return self.request("/audio/accompany/matching", cookie, env, fileName=fileName, mixid=mixid)
    def audio_ktv_total(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取音乐 K 歌数量
        说明：调用此接口，可以获取音乐 K 歌数量，参数信息均来自[获取音乐伴奏信息](#获取音乐伴奏信息)
        必选参数：
        songId：音乐 songid, 该字段需要请求 [获取音乐伴奏信息](#获取音乐伴奏信息) 获取
        singerName：歌手名称，多个以 、 隔开，也可以到 [获取音乐伴奏信息](#获取音乐伴奏信息) 中获取
        songHash：音乐 hash, 该字段需要请求 [获取音乐伴奏信息](#获取音乐伴奏信息) 获取
        接口地址： /audio/ktv/total
        调用例子： /audio/ktv/total?songId=43522508&singerName=希林娜依高&songHash=99AE5A7B04FF76550E380C3757D3E273
        '''
        return self.request("/audio/ktv/total", cookie, env)
    def privilege_lite(self, hash, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取音乐详情
        说明：调用此接口，可以获取音乐详情
        必选参数：
        hash: 歌曲 hash, 可以传多个，每个以逗号分开
        接口地址： /privilege/lite
        调用例子： /privilege/lite?hash=B04ED0F01ABBB62B9D22EC4616ED8AFE
        /privilege/lite?hash=B04ED0F01ABBB62B9D22EC4616ED8AFE,55603312694BF99AD6000C2D0D72D368
        '''
        return self.request("/privilege/lite", cookie, env, hash=hash)
    def krm_audio(self, album_audio_id, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取音乐专辑/歌手信息
        说明：调用此接口，可以获取音乐专辑/歌手信息
        必选参数：
        album_audio_id: 专辑音乐 id (album_audio_id/MixSongID 均可以), 可以传多个，每个以逗号分开
        可选参数
        fields: 可以传 album_info authors.base base audio_info, authors.ip, extra, tags, tagmap 每个 field 以逗号分开
        接口地址： /krm/audio
        调用例子： /krm/audio?album_audio_id=32155307 /krm/audio?album_audio_id=32155307&fields=album_info,base,authors.base
        '''
        return self.request("/krm/audio", cookie, env, album_audio_id=album_audio_id)
    def personal_fm(self, hash=None, songid=None, playtime=None, mode=None, action=None, is_overplay=None, remain_songcnt=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        私人 FM(对应手机和 pc 端的猜你喜欢)
        说明 : 私人 FM
        可选参数：
        hash: 音乐 hash, 建议
        songid: 音乐 songid, 建议
        playtime: 已播放时间, 建议
        mode: 获取模式，默认为 normal, normal：发现，small： 小众，peak：30s
        action: 默认为 play, garbage: 为不喜欢
        song_pool_id： 手机版的 AI，0：Alpha 根据口味推荐相似歌曲, 1：Beta 根据风格推荐相似歌曲, 2：Gamma
        is_overplay: 是否已播放完成
        remain_songcnt: 剩余未播放歌曲数, 默认为 0，大于 4 不返回推荐歌曲，建议
        接口地址： /personal/fm
        调用例子： /personal/fm
        '''
        return self.request("/personal/fm", cookie, env, hash=hash, songid=songid, playtime=playtime, mode=mode, action=action, is_overplay=is_overplay, remain_songcnt=remain_songcnt)
    def pc_diantai(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        banner
        说明 : 调用此接口 , 可获取 banner( 轮播图 ) 数据
        接口地址： /pc/diantai
        调用例子： /pc/diantai
        '''
        return self.request("/pc/diantai", cookie, env)
    def yueku_banner(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        乐库 banner
        说明 : 调用此接口 , 可获取 乐库 banner( 轮播图 ) 数据
        接口地址： /yueku/banner
        调用例子： /yueku/banner
        '''
        return self.request("/yueku/banner", cookie, env)
    def yueku_fm(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        乐库电台
        说明 : 调用此接口 , 可获取乐库电台数据
        接口地址： /yueku/fm
        调用例子： /yueku/fm
        '''
        return self.request("/yueku/fm", cookie, env)
    def yueku(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        乐库
        说明 : 调用此接口 , 可获取手机端乐库数据
        接口地址： /yueku
        调用例子： /yueku
        '''
        return self.request("/yueku", cookie, env)
    def fm_class(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        电台
        说明 : 调用此接口 , 可获取所有电台数据
        接口地址： /fm/class
        调用例子： /fm/class
        '''
        return self.request("/fm/class", cookie, env)
    def fm_recommend(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        电台 - 推荐
        说明 : 调用此接口 , 可获取推荐电台
        接口地址： /fm/recommend
        调用例子： /fm/recommend
        '''
        return self.request("/fm/recommend", cookie, env)
    def fm_image(self, fmid, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        电台 - 图片
        说明 : 调用此接口 , 可获取对应电台的图片
        必选参数：
        fmid: fmid，可以传多个，以逗号分割
        接口地址： /fm/image
        调用例子： /fm/image?fmid=693 /fm/image?fmid=693,37
        '''
        return self.request("/fm/image", cookie, env, fmid=fmid)
    def fm_songs(self, fmid, fmtype=None, fmoffset=None, fmsize=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        电台 - 音乐列表
        说明 : 调用此接口 , 可获取对应电台的音乐列表
        必选参数：
        fmid: fmid，可以传多个，以逗号分割
        可选参数：
        fmtype: fmtype, 可以传多个，以逗号分割
        fmoffset: 歌曲偏移，可以传多个，以逗号分割
        fmsize: 歌曲列表大小，可以传多个，以逗号分割
        接口地址： /fm/songs
        调用例子： /fm/image?fmid=693 /fm/image?fmid=693,37&fmtype=2,2&fmoffset=,5&fmsize5,3
        '''
        return self.request("/fm/songs", cookie, env, fmid=fmid, fmtype=fmtype, fmoffset=fmoffset, fmsize=fmsize)
    def top_ip(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        编辑精选
        说明 : 调用此接口 , 可获取编辑精选数据
        接口地址： /top/ip
        调用例子： /top/ip
        '''
        return self.request("/top/ip", cookie, env)
    def ip(self, id, type=None, pagesize=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        编辑精选数据
        说明 : 调用此接口 , 可获取编辑对应数据
        必选参数：
        id: ip id
        可选参数：
        type: 数据类型，audios: 音乐, albums: 专辑, videos: 视频, author_list: 歌手
        page： 页码
        pagesize: 每页页数, 默认为 30
        接口地址： /ip
        调用例子： /ip?id=87473 ip?id=87473&type=author_list
        '''
        return self.request("/ip", cookie, env, id=id, type=type, pagesize=pagesize)
    def ip_playlist(self, id, pagesize=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        编辑精选歌单
        说明：调用此接口，可获取编辑精选歌单数据
        必选参数：
        id: ip id
        可选参数：
        page： 页码
        pagesize: 每页页数, 默认为 30
        接口地址： /ip/playlist
        调用例子： /ip/playlist?id=87473
        '''
        return self.request("/ip/playlist", cookie, env, id=id, pagesize=pagesize)
    def ip_zone(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        编辑精选专区
        说明：调用此接口，可获取编辑精选专区相关内容，若数据中没有 ip_id，可使用[/ip/zone/home](#编辑精选专区详情)来获取数据
        接口地址： /ip/zone
        调用例子： /ip/zone
        '''
        return self.request("/ip/zone", cookie, env)
    def ip_zone_home(self, id, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        编辑精选专区详情
        说明：调用此接口，可获取编辑精选专区详情，若[/ip/zone](#编辑精选专区) 数据中没有 ip_id，可使用该接口获取数据
        必选参数：
        id: ip id
        接口地址： /ip/zone/home
        调用例子： /ip/zone/home?id=329
        '''
        return self.request("/ip/zone/home", cookie, env, id=id)
    def youth_vip(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        领取 VIP（需要登陆，该接口为测试接口,仅限概念版使用，该接口目前不可使用）
        说明 : 调用此接口 , 每天可领取 1 天 VIP 时长，需要领取 8 次，每次增加 3 小时，该接口来自 KG 概念版，非会员用户需要自行测试是否可用(尽量别频繁调用)
        接口地址： /youth/vip
        调用例子： /youth/vip
        '''
        return self.request("/youth/vip", cookie, env)
    def youth_day_vip(self, receive_day, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        领取一天 VIP（需要登陆，该接口为测试接口,仅限概念版使用）
        说明 : 调用此接口 , 领取概念版 VIP，传入日期可领取改日期一天 VIP，该接口来自 KG 概念版，非会员用户需要自行测试是否可用(尽量别频繁调用)
        注意 ⚠️：建议不要领太多天
        必选参数：
        receive_day: 领取 VIP 日期，格式为：2026-01-30
        接口地址： /youth/day/vip
        调用例子： /youth/day/vip
        '''
        return self.request("/youth/day/vip", cookie, env, receive_day=receive_day)
    def youth_day_vip_upgrade(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        升级概念版 VIP（需要登录，需要先领取一天 VIP，该接口为测试接口,仅限概念版使用）
        说明 : 调用此接口 , 可以升级成畅听 VIP，该接口需要先领取一天 VIP（/youth/day/vip），该接口来自 KG 概念版，非会员用户需要自行测试是否可用(尽量别频繁
        调用)
        接口地址： /youth/day/vip/upgrade
        调用例子： /youth/day/vip/upgrade
        '''
        return self.request("/youth/day/vip/upgrade", cookie, env)
    def youth_month_vip_record(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取当月已领取 VIP 天数（需要登陆，该接口为测试接口,仅限概念版使用）
        说明 : 调用此接口 ,获取当月已领取 VIP 天数
        接口地址： /youth/month/vip/record
        调用例子： /youth/month/vip/record
        '''
        return self.request("/youth/month/vip/record", cookie, env)
    def youth_union_vip(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取已领取 VIP 状态（需要登陆，该接口为测试接口,仅限概念版使用）
        说明 : 调用此接口 ,获取已领取 VIP 状态
        接口地址： /youth/union/vip
        调用例子： /youth/union/vip
        '''
        return self.request("/youth/union/vip", cookie, env)
    def artist_lists(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取歌手列表
        说明 : 调用此接口，可以获取歌手列表.
        可选参数：
        sextypes：性别类型，0：全部，1：男，2：女，3：组合
        type：类型，0：全部，1：华语，2：欧美，3：日韩，4：其他，5：日本，6：韩国
        musician：音乐人，3：为音乐人,0：默认
        hotsize：返回热门数量，默认 30
        接口地址： /artist/lists
        调用例子： /artist/lists
        '''
        return self.request("/artist/lists", cookie, env)
    def artist_detail(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取歌手详情
        说明 : 调用此接口 , 传入歌手 id, 可获得歌手信息
        必选参数：
        id： 歌手 id
        接口地址： /artist/detail
        调用例子： /artist/detail?id=6539
        '''
        return self.request("/artist/detail", cookie, env)
    def artist_albums(self, pagesize=None, sort=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取歌手专辑
        说明 : 调用此接口 , 传入歌手 id, 可获得歌手专辑
        必选参数：
        id： 歌手 id
        可选参数：
        page： 页码
        pagesize: 每页页数, 默认为 30
        sort: 排序，hot : 热门, new: 最新
        接口地址： /artist/albums
        调用例子： /artist/albums?id=6539
        '''
        return self.request("/artist/albums", cookie, env, pagesize=pagesize, sort=sort)
    def artist_audios(self, pagesize=None, sort=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取歌手单曲
        说明 : 调用此接口 , 传入歌手 id, 可获得歌手歌曲
        必选参数：
        id： 歌手 id
        可选参数：
        page： 页码
        pagesize: 每页页数, 默认为 30
        sort: 排序，hot : 热门, new: 最新
        接口地址： /artist/audios
        调用例子： /artist/audios?id=6539
        '''
        return self.request("/artist/audios", cookie, env, pagesize=pagesize, sort=sort)
    def artist_videos(self, pagesize=None, tag=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取歌手 MV
        说明 : 调用此接口 , 传入歌手 id, 可获得歌手 MV
        必选参数：
        id： 歌手 id
        可选参数：
        page： 页码
        pagesize: 每页页数, 默认为 30
        tag: official: 官方版本，live：现场版本，fan：饭制版本，artist: 歌手发布, all: 获取全部，默认为获取全部
        接口地址： /artist/videos
        调用例子： /artist/videos?id=6539
        '''
        return self.request("/artist/videos", cookie, env, pagesize=pagesize, tag=tag)
    def artist_follow(self, id, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        关注歌手
        说明：调用此接口, 传入歌手 id, 可以关注该歌手（需要登录）
        必选参数：
        id: 歌手 id
        接口地址： /artist/follow
        调用例子： /artist/follow?id=6539
        '''
        return self.request("/artist/follow", cookie, env, id=id)
    def artist_unfollow(self, id, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        取消关注歌手
        说明：调用此接口, 传入歌手 id, 可以取消关注该歌手（需要登录）
        必选参数：
        id: 歌手 id
        接口地址： /artist/unfollow
        调用例子： /artist/unfollow?id=6539
        '''
        return self.request("/artist/unfollow", cookie, env, id=id)
    def artist_follow_newsongs(self, last_album_id=None, pagesize=None, opt_sort=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取关注歌手新歌
        说明：调用此接口, 可以获取用户已关注的歌手新歌（需要登录）
        可选参数：
        last_album_id: 最后专辑 id
        pagesize: 每页页数, 默认为 30,
        opt_sort: 排序，1：时间，2：亲密度，默认为 1(时间)
        接口地址： /artist/follow/newsongs
        调用例子： /artist/follow/newsongs
        '''
        return self.request("/artist/follow/newsongs", cookie, env, last_album_id=last_album_id, pagesize=pagesize, opt_sort=opt_sort)
    def video_url(self, hash, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取视频 url
        说明 : 传入的视频的 hash, 可以获取对应的视频的 url
        必选参数：
        hash: 视频 hash
        接口地址： /video/url
        调用例子： /video/url?hash=3B5EE16299F703AEB0E5C28CB152EDF0
        '''
        return self.request("/video/url", cookie, env, hash=hash)
    def kmr_audio_mv(self, album_audio_id, fields=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取歌曲 MV
        说明 : 传入 album_audio_id/MixSongID 获取歌曲 相对应的 mv
        必选参数：
        album_audio_id: 专辑音乐 id (album_audio_id/MixSongID 均可以), 可以传多个，每个以逗号分开,
        可选参数：
        fields: 支持多个，每个以逗号分隔，支持的值有：mkv,tags,h264,h265,authors
        接口地址： /kmr/audio/mv
        调用例子： /kmr/audio/mv?album_audio_id=32155307 /kmr/audio/mv?album_audio_id=32155307&fields=mkv,tags
        '''
        return self.request("/kmr/audio/mv", cookie, env, album_audio_id=album_audio_id, fields=fields)
    def video_privilege(self, hash, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取视频相关信息
        说明 : 传入的视频的 hash, 可以获取对应的视频的相关信息
        必选参数：
        hash: 视频 hash，可以传多个，以逗号隔开
        接口地址： /video/privilege
        调用例子： /video/privilege?hash=3B5EE16299F703AEB0E5C28CB152EDF0
        '''
        return self.request("/video/privilege", cookie, env, hash=hash)
    def video_detail(self, id, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取视频详情
        说明：调用此接口，可以获取视频详情，可以获取更高清的视频 hash
        必选参数：
        id: 视频 id/video id
        接口地址： /video/detail
        调用例子： /video/detail?id=11517822
        '''
        return self.request("/video/detail", cookie, env, id=id)
    def top_song(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        新歌速递
        说明：调用此接口，可以获取新歌速递
        接口地址： /top/song
        调用例子： /top/song
        '''
        return self.request("/top/song", cookie, env)
    def scene_lists(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        场景音乐列表
        说明：调用此接口，可以场景音乐列表
        接口地址： /scene/lists
        调用例子： /scene/lists
        '''
        return self.request("/scene/lists", cookie, env)
    def scene_module(self, id, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        场景音乐详情
        说明：调用此接口，可以场景音乐详情
        必选参数：
        id: 场景音乐 scene_id
        接口地址： /scene/module
        调用例子： /scene/module?id=9
        '''
        return self.request("/scene/module", cookie, env, id=id)
    def scene_list_v2(self, pagesize=None, sort=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取场景音乐讨论区
        说明：调用此接口，可以获取场景音乐讨论区
        必选参数
        id: 场景音乐 scene_id
        可选参数：
        page： 页码
        pagesize: 每页页数, 默认为 30
        sort: 排序，rec: 推荐，hot: 热门，new: 最新, 默认为推荐
        接口地址： /scene/list/v2
        调用例子： /scene/list/?id=9
        '''
        return self.request("/scene/list/v2", cookie, env, pagesize=pagesize, sort=sort)
    def scene_module_info(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取场景音乐模块 Tag
        说明：调用此接口，可以获取场景模块 Tag
        必选参数
        id: 场景音乐 scene_id
        module_id: 场景音乐 module_id
        可选参数：
        接口地址： /scene/module/info
        调用例子： /scene/module/info?id=9&module_id=83
        '''
        return self.request("/scene/module/info", cookie, env)
    def scene_collection_list(self, pagesize=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取场景音乐歌单列表
        说明：调用此接口，可以获取场景音乐歌单列表
        必选参数
        tag_id: 场景音乐 tag_id
        可选参数：
        page： 页码
        pagesize: 每页页数, 默认为 30
        接口地址： /scene/collection/list
        调用例子： /scene/collection/list?tag_id=42391
        '''
        return self.request("/scene/collection/list", cookie, env, pagesize=pagesize)
    def scene_video_list(self, pagesize=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取场景音乐视频列表
        说明：调用此接口，可以获取场景音乐视频列表
        必选参数
        tag_id: 场景音乐视频 tag_id
        可选参数：
        page： 页码
        pagesize: 每页页数, 默认为 30
        接口地址： /scene/video/list
        调用例子： /scene/video/list?tag_id=42399
        '''
        return self.request("/scene/video/list", cookie, env, pagesize=pagesize)
    def scene_audio_list(self, pagesize=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取场景音乐音乐列表
        说明：调用此接口，可以获取场景音乐音乐列表
        必选参数
        id: 场景音乐 scene_id
        module_id: 场景音乐 module_id
        tag: 场景音乐 tag_id
        可选参数：
        page： 页码
        pagesize: 每页页数, 默认为 30
        接口地址： /scene/audio/list
        调用例子： /scene/audio/list?id=9&module_id=173&tag=42391
        '''
        return self.request("/scene/audio/list", cookie, env, pagesize=pagesize)
    def everyday_recommend(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        每日推荐
        说明：调用此接口，可以获取每日推荐列表
        可选参数：
        platform：设备类型，默认为 ios,支持 android 和 ios
        接口地址： /everyday/recommend
        调用例子： /everyday/recommend
        '''
        return self.request("/everyday/recommend", cookie, env)
    def everyday_history(self, history_name=None, date=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        历史推荐
        说明：调用此接口，可以获取历史推荐
        可选参数：
        mode：当 mode 为 list 时，则返回历史推荐列表，当 mode 为 song 时则返回当前歌曲列表，支持参数为：list 和 song,
        history_name: 当 mode 为 song 该参数为必选参数。
        date: 当 mode 为 song 该参数为必选参数。
        platform：设备类型，默认为 ios,支持 android 和 ios
        接口地址： /everyday/history
        调用例子： /everyday/history /everyday/history?mode=song&history_name=RT_336d5ebc5436534e61d16e63ddfca327_20240106&date=20240106
        '''
        return self.request("/everyday/history", cookie, env, history_name=history_name, date=date)
    def everyday_style_recommend(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        风格推荐
        说明：调用此接口，可以获取风格推荐
        可选参数：
        platform：设备类型，默认为 ios,支持 android 和 ios
        tagids：支持多个，每个以逗号分隔，该接口下可获取 tag 信息
        接口地址： /everyday/style/recommend
        调用例子： /everyday/style/recommend /everyday/style/recommend?tagids=S14,S15,S16
        '''
        return self.request("/everyday/style/recommend", cookie, env)
    def rank_list(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        排行列表
        说明：调用此接口，可以获取排行榜列表
        可选参数：
        withsong：是否返回歌曲（部分）
        接口地址： /rank/list
        调用例子： /rank/list
        '''
        return self.request("/rank/list", cookie, env)
    def rank_top(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        排行榜推荐列表
        说明：调用此接口，可以获取排行榜推荐列表
        接口地址： /rank/top
        调用例子： /rank/top
        '''
        return self.request("/rank/top", cookie, env)
    def rank_vol(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        排行榜往期列表
        说明：调用此接口，可以获取排行榜往期列表
        必选参数：
        rankid：排行榜 id
        可选参数：
        rank_cid：排行榜 cid
        接口地址： /rank/vol
        调用例子： /rank/vol?rankid=8888
        '''
        return self.request("/rank/vol", cookie, env)
    def rank_info(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        排行榜信息
        说明：调用此接口，可以获取排行榜信息
        必选参数：
        rankid：排行榜 id
        可选参数：
        rank_cid：排行榜 cid
        album_img：是否返回专辑图片，1：返回，0：不返回，默认返回
        zone：排行榜 zone
        接口地址： /rank/info
        调用例子： /rank/info?rankid=8888
        '''
        return self.request("/rank/info", cookie, env)
    def rank_audio(self, pagesize=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        排行榜歌曲列表
        说明：调用此接口，可以获排行榜歌曲列表
        必选参数：
        rankid：排行榜 id
        可选参数：
        rank_cid：若需要返回往期歌曲列表，则该参数为必填，否则默认返回最新一期，[/rank/vol](#排行榜往期列表) 返回值中，volid 则为该参数
        page： 页码
        pagesize: 每页页数, 默认为 30
        接口地址： /rank/audio
        调用例子： /rank/audio?rankid=8888 /rank/audio?rankid=8888&rank_cid=76442
        '''
        return self.request("/rank/audio", cookie, env, pagesize=pagesize)
    def favorite_count(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        歌曲收藏数
        说明 : 调用此接口 , 传入音乐 mixsongids 参数 , 可获得该音乐的收藏数( 不需要登录 )
        必选参数：
        mixsongids：音乐 mixsongid，多个以逗号分隔
        接口地址： /favorite/count
        调用例子： /favorite/count?mixsongids=368015985,368015986 /favorite/count?mixsongids=368015985
        '''
        return self.request("/favorite/count", cookie, env)
    def comment_count(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        歌曲评论数
        说明 : 调用此接口 , 传入音乐 hash/special_id 参数 , 可获得该音乐的评论数( 不需要登录 )
        必选参数：
        hash：音乐 hash
        special_id：为 评论下的 special_child_id 字段
        接口地址： /comment/count
        调用例子： /comment/count?hash=98eb07ad8eaf74bf56dece55518ad63e /comment/count?special_id=20505418
        '''
        return self.request("/comment/count", cookie, env)
    def comment_music(self, pagesize=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        歌曲评论
        说明 : 调用此接口 , 传入音乐 mixsongid 参数 , 可获得该音乐的所有评论 ( 不需要登录 )
        必选参数：
        mixsongid：音乐 mixsongid
        可选参数：
        page： 页码
        pagesize: 每页页数, 默认为 30
        show_classify： 是否返回分类列表，0 为不返回，1 为返回
        show_hotword_list：是否返回热词，0 为不返回，1 为返回
        接口地址： /comment/music
        调用例子： /comment/music?mixsongid=302362878
        '''
        return self.request("/comment/music", cookie, env, pagesize=pagesize)
    def comment_music_classify(self, pagesize=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        歌曲评论-根据分类返回
        说明 : 调用此接口 , 传入音乐 mixsongid 和 type_id 参数 , 可获得该音乐的分类评论 ( 不需要登录 )
        必选参数：
        mixsongid：音乐 mixsongid
        type_id：分类 id
        可选参数：
        page： 页码
        pagesize: 每页页数, 默认为 30
        sort：排序，1 为正序，2 为倒序
        接口地址： /comment/music/classify
        调用例子： /comment/music/classify?mixsongid=302362878&type_id=12
        '''
        return self.request("/comment/music/classify", cookie, env, pagesize=pagesize)
    def comment_music_hotword(self, pagesize=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        歌曲评论-根据热词返回
        说明 : 调用此接口 , 传入音乐 mixsongid 和 hot_word 参数 , 可获得该音乐的热词评论 ( 不需要登录 )
        必选参数：
        mixsongid：音乐 mixsongid
        hot_word：热词
        可选参数：
        page： 页码
        pagesize: 每页页数, 默认为 30
        接口地址： /comment/music/hotword
        调用例子： /comment/music/hotword?mixsongid=302362878&hot_word=生活
        '''
        return self.request("/comment/music/hotword", cookie, env, pagesize=pagesize)
    def comment_floor(self, pagesize=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        楼层评论
        说明 : 调用此接口 , 传入资源 special_id 和资源类型 tid 和资源 mixsongid 参数, 可获得该资源的歌曲楼层评论
        必选参数：
        special_id：为 评论下的 special_child_id 字段
        mixsongid：为 歌曲的 mixsongid
        tid：评论 id
        可选参数：
        page： 页码
        pagesize: 每页页数, 默认为 30
        接口地址： /comment/floor
        调用例子： /comment/floor?special_id=100285259&mixsongid=302362878&tid=678433417
        '''
        return self.request("/comment/floor", cookie, env, pagesize=pagesize)
    def comment_playlist(self, pagesize=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        歌单评论
        说明 : 调用此接口 , 传入歌单 id 参数 , 可获得该歌单的所有评论 ( 不需要登录 )
        必选参数：
        id：歌单 global_collection_id
        可选参数：
        page： 页码
        pagesize: 每页页数, 默认为 30
        show_classify： 是否返回分类列表，0 为不返回，1 为返回
        show_hotword_list：是否返回热词，0 为不返回，1 为返回
        接口地址： /comment/playlist
        调用例子： /comment/playlist?id=collection_3_1373407643_366_0
        '''
        return self.request("/comment/playlist", cookie, env, pagesize=pagesize)
    def comment_album(self, pagesize=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        专辑评论
        说明 : 调用此接口 , 传入 专辑 id 参数 , 可获得该专辑的所有评论 ( 不需要登录 )
        id：专辑 id
        可选参数：
        page： 页码
        pagesize: 每页页数, 默认为 30
        show_classify： 是否返回分类列表，0 为不返回，1 为返回
        show_hotword_list：是否返回热词，0 为不返回，1 为返回
        接口地址： /comment/album
        调用例子： /comment/album?id=collection_3_1373407643_366_0
        '''
        return self.request("/comment/album", cookie, env, pagesize=pagesize)
    def sheet_list(self, pagesize=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        歌曲曲谱
        说明 : 调用此接口，传入歌曲 album_audio_id 可获得该歌曲的曲谱，注意：ai 曲谱为 xml 文件，需要自己解析，别问我，我也看不懂
        必选参数：
        album_audio_id：音乐的 mixsongid/album_audio_id
        可选参数：
        opern_type：曲谱类型，0：全部，1：钢琴，2：吉他，3：鼓，98：简谱，99：其他
        page： 页码
        pagesize: 每页页数, 默认为 30
        接口地址： /sheet/list
        调用例子： /sheet/list?album_audio_id=302362878
        '''
        return self.request("/sheet/list", cookie, env, pagesize=pagesize)
    def sheet_detail(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        曲谱详情
        说明 : 调用此接口，传入曲谱 id 和 曲谱 source 可获得该曲谱详情，注意：ai 曲谱为 xml 文件，需要自己解析，别问我，我也看不懂
        必选参数：
        id：曲谱 id,
        source：曲谱 source,
        接口地址： /sheet/detail
        调用例子： /sheet/detail?id=1564334343483305984&source=2
        '''
        return self.request("/sheet/detail", cookie, env)
    def sheet_hot(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        推荐曲谱
        说明 : 调用此接口，可以获取推荐曲谱
        可选参数：
        opern_type：曲谱类型，1：钢琴，2：吉他，3：鼓，98：简谱，99：其他
        接口地址： /sheet/hot
        调用例子： /sheet/hot
        '''
        return self.request("/sheet/hot", cookie, env)
    def sheet_collection(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        曲谱合集
        说明 : 调用此接口，可以获取曲谱合集
        可选参数：
        position：2：精选谱单，3：音乐教材，4：古典钢琴
        接口地址： /sheet/collection
        调用例子： /sheet/collection
        '''
        return self.request("/sheet/collection", cookie, env)
    def sheet_collection(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        曲谱合集详情
        说明 : 调用此接口，可以获取曲谱合集详情
        可选参数：
        collection_id：合集 id
        page： 页码
        接口地址： /sheet/collection
        调用例子： /sheet/collection
        '''
        return self.request("/sheet/collection", cookie, env)
    def playhistory_upload(self, pc=None, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        提交听歌历史
        说明：提交听歌历史后，支持在其他设备上查看听歌历史
        必选参数：
        mxid： 专辑音乐 id (album_audio_id/MixSongID 均可以)
        可选参数：
        ot：当前时间戳, 秒级，不要传入毫秒级，否者会返回错误，或者从 [获取服务器时间](#获取服务器时间) 中获取
        pc: 当前播放次数，更新播放次数，当服务器的值大于传入值时，将维持服务最大值，否则更新
        接口地址： /playhistory/upload
        调用例子： /playhistory/upload?mxid=32155307
        '''
        return self.request("/playhistory/upload", cookie, env, pc=pc)
    def server_now(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取服务器时间
        说明：获取服务器时间，返回服务器时间戳
        接口地址： /server/now
        调用例子： /server/now
        '''
        return self.request("/server/now", cookie, env)
    def brush(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        刷刷
        说明：获取刷刷视频
        接口地址： /brush
        调用例子： /brush
        '''
        return self.request("/brush", cookie, env)
    def ai_recommend(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        AI 推荐
        说明：传入 album_audio_id/MixSongID 获取 AI 推荐歌曲
        必选参数：
        album_audio_id： 专辑音乐 id (album_audio_id/MixSongID 均可以), 可以传多个，每个以逗号分开,
        接口地址： /ai/recommend
        调用例子： /ai/recommend?album_audio_id=274565080 /ai/recommend?album_audio_id=274565080,68435124
        '''
        return self.request("/ai/recommend", cookie, env)
    def youth_channel_all(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        频道 - 获取用户所有频道
        说明：登录后调用此接口，可以获取用户所有订阅的频道
        可选参数：
        page：页数
        pagesize : 每页页数, 默认为 30
        接口地址： /youth/channel/all
        调用例子： /youth/channel/all
        '''
        return self.request("/youth/channel/all", cookie, env)
    def youth_channel_detail(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        频道 - 详情
        说明：调用此接口，传入 global_collection_id / channel_id 可以获取频道详情
        必选参数：
        global_collection_id：频道 id (global_collection_id / channel_id 均可以), 可以传多个，每个以逗号分开,
        接口地址： /youth/channel/detail
        调用例子： /youth/channel/detail?global_collection_id=11576464149
        '''
        return self.request("/youth/channel/detail", cookie, env)
    def youth_channel_amway(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        频道 - 频道安利
        说明：调用此接口，传入 global_collection_id / channel_id 可以获取频道安利
        必选参数：
        global_collection_id：频道 id (global_collection_id / channel_id 均可以)
        接口地址： /youth/channel/amway
        调用例子： /youth/channel/amway?global_collection_id=11576464149
        '''
        return self.request("/youth/channel/amway", cookie, env)
    def youth_channel_similar(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        频道 - 相似频道
        说明：调用此接口，传入 global_collection_id / channel_id 可以获取相似频道
        必选参数：
        channel_id：频道 id (global_collection_id / channel_id 均可以)
        接口地址： /youth/channel/similar
        调用例子： /youth/channel/similar?channel_id=11576464149
        '''
        return self.request("/youth/channel/similar", cookie, env)
    def youth_channel_sub(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        频道 - 订阅
        说明：登录后调用此接口， 传入 global_collection_id / channel_id 可订阅频道
        必选参数：
        global_collection_id：频道 id (global_collection_id / channel_id 均可以)
        可选参数：
        t：1 为订阅，0 为取消订阅，不传默认为订阅
        接口地址： /youth/channel/sub
        调用例子： /youth/channel/sub?global_collection_id=11576464149 /youth/channel/sub?global_collection_id=11576464149&t=0
        '''
        return self.request("/youth/channel/sub", cookie, env)
    def youth_channel_song(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        频道 - 音乐故事
        说明：调用此接口，传入 global_collection_id / channel_id 可以获取音乐故事
        必选参数：
        global_collection_id：频道 id (global_collection_id / channel_id 均可以)
        可选参数：
        page：页数
        pagesize : 每页页数, 默认为 30
        接口地址： /youth/channel/song
        调用例子： /youth/channel/song?global_collection_id=11576464149
        '''
        return self.request("/youth/channel/song", cookie, env)
    def youth_channel_song_detail(self, fileid, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        频道 - 音乐故事详情
        说明：调用此接口，传入 global_collection_id / channel_id 和 fileid 可以获取音乐故事详情
        必选参数：
        global_collection_id：频道 id (global_collection_id / channel_id 均可以)
        fileid: 音乐故事 fileid
        接口地址： /youth/channel/song/detail
        调用例子： /youth/channel/song/detail?global_collection_id=11576464149&fileid=1720958083456581
        '''
        return self.request("/youth/channel/song/detail", cookie, env, fileid=fileid)
    def youth_dynamic_recent(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        动态 - 最常访问
        说明：登录后调用此接口，可以获取经常访问的频道和用户
        接口地址： /youth/dynamic/recent
        调用例子： /youth/dynamic/recent
        '''
        return self.request("/youth/dynamic/recent", cookie, env)
    def youth_user_song(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        获取用户公开的音乐
        说明：调用此接口，可以获取用户公开的音乐
        必选参数：
        userid：用户 id
        可选参数：
        page：页数
        pagesize : 每页页数, 默认为 30
        接口地址： /youth/user/song
        调用例子： /youth/user/song?userid=1354894105
        '''
        return self.request("/youth/user/song", cookie, env)
    def longaudio_daily_recommend(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        听书 - 每日推荐
        可选参数：
        page：页数
        pagesize : 每页页数, 默认为 30
        接口地址： /longaudio/daily/recommend
        调用例子： /longaudio/daily/recommend
        '''
        return self.request("/longaudio/daily/recommend", cookie, env)
    def longaudio_rank_recommend(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        听书 - 排行榜推荐
        接口地址： /longaudio/rank/recommend
        调用例子： /longaudio/rank/recommend
        '''
        return self.request("/longaudio/rank/recommend", cookie, env)
    def longaudio_vip_recommend(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        听书 - VIP 推荐
        接口地址： /longaudio/vip/recommend
        调用例子： /longaudio/vip/recommend
        '''
        return self.request("/longaudio/vip/recommend", cookie, env)
    def longaudio_week_recommend(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        听书 - 每周推荐
        接口地址： /longaudio/week/recommend
        调用例子： /longaudio/week/recommend
        '''
        return self.request("/longaudio/week/recommend", cookie, env)
    def longaudio_album_detail(self, album_id, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        听书 - 专辑详情
        必选参数：
        album_id: 专辑 id 可以传多个，每个以逗号分开,
        接口地址： /longaudio/album/detail
        调用例子： /longaudio/album/detail?album_id=56655759
        '''
        return self.request("/longaudio/album/detail", cookie, env, album_id=album_id)
    def longaudio_album_audios(self, album_id, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        听书 - 专辑音乐列表
        必选参数：
        album_id: 专辑 id 可以传多个
        接口地址： /longaudio/album/audios
        调用例子： /longaudio/album/audios?album_id=56655759
        '''
        return self.request("/longaudio/album/audios", cookie, env, album_id=album_id)
    def song_ranking(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        歌曲详情 - 歌曲成绩单
        说明：调用此接口，可以获取歌曲详情里面的歌曲成绩单信息
        必选参数：
        album_audio_id： 专辑音乐 id (album_audio_id/MixSongID 均可以),
        接口地址： /song/ranking
        调用例子： /song/ranking?album_audio_id=32155307
        '''
        return self.request("/song/ranking", cookie, env)
    def song_ranking_filter(self, cookie = "", env: KugouProcessEnv = None) -> Response:
        '''
        歌曲详情 - 歌曲成绩单详情
        说明：登陆后调用此接口，可以获取更详细的歌曲成绩单信息
        必选参数：
        album_audio_id： 专辑音乐 id (album_audio_id/MixSongID 均可以),
        可选参数：
        page：页数
        pagesize : 每页页数, 默认为 30
        接口地址： /song/ranking/filter
        调用例子： /song/ranking/filter?album_audio_id=32155307
        '''
        return self.request("/song/ranking/filter", cookie, env)
