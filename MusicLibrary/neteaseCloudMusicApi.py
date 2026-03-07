import ctypes
from ctypes import CDLL, Structure, c_char_p, c_void_p, c_int, POINTER
from .core import (
    load_ncm,
    engine,
    _Engine,
    _NcmProcessEnv as NcmProcessEnv,
    _NcmContextManager,
)
from .common import to_bytes, Response
import json
from enum import Enum

__all__ = ["NeteaseCloudMusicApi", "NcmProcessEnv"]


class NeteaseCloudMusicApi:
    def __init__(self, env: NcmProcessEnv = None):
        self.ncm = load_ncm()

        _Engine()
        _NcmContextManager.init(env)
        self.env = env or _NcmContextManager._env
        self.ctx = _NcmContextManager.get_ctx()
        self._destroyed = False

    def request(self, path, cookie="", env: NcmProcessEnv = None, **query) -> Response:
        if env is None:
            env = self.env

        # 剔除值为 None 的参数
        print(f"Original query: {query}")
        query = {k: v for k, v in query.items() if v is not None}
        query = json.dumps(query) if query else ""

        path = to_bytes(path)
        query = to_bytes(query)
        cookie = to_bytes(cookie)

        ptr = self.ncm.ncm_request(
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
