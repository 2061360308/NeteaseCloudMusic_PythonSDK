import os
import atexit
import ctypes
from ctypes import CDLL, Structure, c_char_p, c_void_p, c_int, POINTER
from .common import to_bytes
from enum import Enum

LIB_DIR = os.path.join(os.path.dirname(__file__), "lib")
engine = CDLL(os.path.join(LIB_DIR, "engine.dll"))

kugou = None
ncm = None

engine.init_engine.restype = c_int
engine.init_engine.argtypes = []

engine.destroy_engine.restype = c_int
engine.destroy_engine.argtypes = []

engine.response_free.restype = None
engine.response_free.argtypes = [c_void_p]

engine.destroy_context.restype = None
engine.destroy_context.argtypes = [c_void_p]


class _Engine:
    __instance = None
    __initialized = False

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if not self.__class__.__initialized:
            if engine.init_engine() != 0:
                raise RuntimeError("Failed to initialize engine")
            self.__class__.__initialized = True

    @classmethod
    def destroy(cls):
        try:
            if cls.__initialized:
                engine.destroy_engine()
                cls.__initialized = False
        except Exception as e:
            # 可根据需要打印日志或忽略
            # Todo
            pass

    def __del__(self):
        pass  # 交由 atexit 统一销毁


class _Platform(Enum):
    LITE = b"lite"
    DEFAULT = b""


class _KugouProcessEnv(Structure):
    _fields_ = [
        ("platform", c_char_p),
        ("KUGOU_API_GUID", c_char_p),
        ("KUGOU_API_DEV", c_char_p),
        ("KUGOU_API_MAC", c_char_p),
    ]

    def __init__(self, platform=_Platform.DEFAULT, guid="", dev="", mac=""):
        super().__init__(
            to_bytes(platform.value), to_bytes(guid), to_bytes(dev), to_bytes(mac)
        )


class _NcmProcessEnv(Structure):
    _fields_ = [
        ("cnIp", c_char_p),
        ("ANONYMOUS_TOKEN", c_char_p),
    ]

    def __init__(self, cnIp="", ANONYMOUS_TOKEN=""):
        super().__init__(to_bytes(cnIp), to_bytes(ANONYMOUS_TOKEN))


def load_kugou():
    global kugou
    if kugou is None:
        kugou = CDLL(os.path.join(LIB_DIR, "kugou_music_api.dll"))
        kugou.kugou_init.restype = c_void_p
        kugou.kugou_init.argtypes = [POINTER(_KugouProcessEnv)]

        kugou.kugou_destroy.restype = c_int
        kugou.kugou_destroy.argtypes = []
        
        kugou.get_kugou_context.restype = c_void_p
        kugou.get_kugou_context.argtypes = []

        kugou.kugou_request.restype = (
            c_void_p  # 用 void_p 避免 ctypes 自动解析，手动 free
        )
        kugou.kugou_request.argtypes = [
            c_void_p,
            c_char_p,
            c_char_p,
            c_char_p,
            POINTER(_KugouProcessEnv),
        ]
    return kugou


def load_ncm():
    global ncm
    if ncm is None:
        ncm = CDLL(os.path.join(LIB_DIR, "ncm_music_api.dll"))
        ncm.ncm_init.restype = c_void_p
        ncm.ncm_init.argtypes = [POINTER(_NcmProcessEnv)]

        ncm.ncm_destroy.restype = c_int
        ncm.ncm_destroy.argtypes = []
        
        ncm.get_ncm_context.restype = c_void_p
        ncm.get_ncm_context.argtypes = []

        ncm.ncm_request.restype = c_void_p  # 用 void_p 避免 ctypes 自动解析，手动 free
        ncm.ncm_request.argtypes = [
            c_void_p,
            c_char_p,
            c_char_p,
            c_char_p,
            POINTER(_NcmProcessEnv),
        ]

        ncm.generate_random_cnIp.restype = c_void_p
        ncm.generate_random_cnIp.argtypes = [c_void_p]

        ncm.generate_anonimous_token.restype = c_void_p
        ncm.generate_anonimous_token.argtypes = [c_void_p]
    return ncm


class _KugouContextManager:
    _ctx = None
    _env = None

    @classmethod
    def init(cls, env=None):
        if cls._ctx is None:
            if env is None:
                env = _KugouProcessEnv()
            cls._env = env
            # init的时候会创建一个上下文,记录保留
            kugou = load_kugou()
            cls._ctx = kugou.kugou_init(ctypes.byref(env))
        return cls._ctx

    @classmethod
    def get_ctx(cls):
        # 优先返回保留的上下文(首次)，多次调用则每次返回新的上下文
        if cls._ctx is not None:
            ctx = cls._ctx
            cls._ctx = None
            return ctx
        else:
            # 返回新的上下文
            return kugou.get_kugou_context()

    @classmethod
    def destroy(cls):
        try:
            if cls._ctx is not None:
                kugou.kugou_destroy()
                cls._ctx = None
                cls._env = None
        except Exception as e:
            # 可记录日志或忽略
            # Todo
            pass


class _NcmContextManager:
    _ctx = None
    _env = None

    @classmethod
    def init(cls, env=None):
        if cls._ctx is None:
            if env is None:
                env = _NcmProcessEnv()
            cls._env = env
            # init的时候会创建一个上下文,记录保留
            ncm = load_ncm()
            cls._ctx = ncm.ncm_init(ctypes.byref(env))
        return cls._ctx

    @classmethod
    def get_ctx(cls):
        # 优先返回保留的上下文(首次)，多次调用则每次返回新的上下文
        if cls._ctx is not None:
            ctx = cls._ctx
            cls._ctx = None
            return ctx
        else:
            # 返回新的上下文
            return ncm.get_ncm_context()

    @classmethod
    def destroy(cls):
        try:
            if cls._ctx is not None:
                ncm.ncm_destroy()
                cls._ctx = None
                cls._env = None
        except Exception as e:
            # 可记录日志或忽略
            # Todo
            pass


atexit.register(_Engine.destroy)
atexit.register(_KugouContextManager.destroy)
atexit.register(_NcmContextManager.destroy)
