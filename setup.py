import os

from setuptools import setup
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


class bdist_wheel(_bdist_wheel):
    """Mark wheels as platform-specific and control platform tag by env var.

    使用环境变量 MUSICLIB_ARCH 来区分目标架构：
    - "AMD64" -> win_amd64
    - "x86"   -> win32
    - "ARM64" -> win_arm64
    """

    def finalize_options(self):
        super().finalize_options()
        # 包含 DLL，必须标记为非纯 Python
        self.root_is_pure = False

    def get_tag(self):
        python, abi, plat = super().get_tag()

        arch = os.environ.get("MUSICLIB_ARCH")
        if arch == "AMD64":
            plat = "win_amd64"
        elif arch == "x86":
            plat = "win32"
        elif arch == "ARM64":
            plat = "win_arm64"

        # 只支持 Python 3，因此强制 py3-none-plat
        return "py3", "none", plat


setup(cmdclass={"bdist_wheel": bdist_wheel})
