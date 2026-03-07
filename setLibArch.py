import os
import requests

ARCH_TO_FILE = {
    "AMD64": "windows-x64.zip",
    "x86": "windows-x86.zip",
    "ARM64": "windows-arm64.zip"
}

REPO = "2061360308/MusicLibrary"
GITHUB_API = f"https://api.github.com/repos/{REPO}/releases/latest"

def download_file(url, filename):
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

def main(arch):
    filename = ARCH_TO_FILE.get(arch)
    if not filename:
        print(f"未知架构: {arch}")
        return
    if os.path.exists(filename):
        print(f"{filename} 已存在")
    else:
        # 获取最新 release
        resp = requests.get(GITHUB_API)
        resp.raise_for_status()
        assets = resp.json().get("assets", [])
        for asset in assets:
            if asset["name"] == filename:
                print(f"正在下载 {filename} ...")
                download_file(asset["browser_download_url"], filename)
                print("下载完成")
                break
        else:
            print(f"未找到 {filename} 的 release 资源")
            return

    # 删除 MusicLibrary/include 和 lib 目录
    import shutil
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MusicLibrary")
    for subdir in ["include", "lib"]:
        target = os.path.join(base_dir, subdir)
        if os.path.exists(target):
            print(f"删除目录: {target}")
            shutil.rmtree(target)

    # 解压 zip 到 MusicLibrary/，但只保留 lib 目录下的 DLL 文件
    import zipfile
    with zipfile.ZipFile(filename, "r") as zip_ref:
        for member in zip_ref.infolist():
            # 统一使用 / 判断路径前缀
            name = member.filename.replace("\\", "/")

            # 跳过目录条目
            if name.endswith("/"):
                continue

            # lib/ 下只保留 .dll，其它（.lib/.exp 等）跳过
            if name.startswith("lib/"):
                if not name.lower().endswith(".dll"):
                    continue

            zip_ref.extract(member, base_dir)

    print(f"已解压 {filename} 到 {base_dir}")
    
    print(f"已为 {arch} 架构更换配置")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("用法: python script.py <arch>")
    else:
        main(sys.argv[1])