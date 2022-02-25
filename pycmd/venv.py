# -*- coding: utf-8 -*-
# Description: Create python virtual environment on MacOS.
# Usage: venv
from pathlib import Path
import shutil
import subprocess
from simple_term_menu import TerminalMenu
from .console import Console


def choose_pyvern():
    Console.plain("🔨 Which python prefer ?")
    cellar = Path("/usr/local/Cellar")
    verns = sorted(x.name for x in cellar.glob("python@3*"))
    paths = sorted(str(x) for x in cellar.glob("python@3*/3.*/bin/python3"))
    menu = TerminalMenu(verns)
    index = menu.show()
    vern = verns[index]
    path = paths[index]
    Console.ok(vern)
    return vern, path


def create_venv(vern, path):
    Console.plain("🔨 Create virtual environment")
    try:
        shutil.rmtree(".venv")
    except FileNotFoundError:
        pass
    subprocess.run([path, "-m", "venv", ".venv"])
    Console.ok("created in .venv/")

    Console.plain("🔨 Upgrade pip itself")
    subprocess.run([".venv/bin/pip", "install", "-U", "pip"], stdout=subprocess.DEVNULL)
    pip_vern = subprocess.run(".venv/bin/pip --version | awk '{print $2}'", shell=True, stdout=subprocess.DEVNULL)
    Console.ok(f"upgraded to {pip_vern}")


def switch_mirror():
    Console.plain("🔨 Switch pip mirror")
    mirrors = [
        "skip",
        "https://mirrors.cloud.tencent.com/pypi/simple",
        "https://pypi.tuna.tsinghua.edu.cn/simple",
        "https://pypi.mirrors.ustc.edu.cn/simple/",
    ]
    menu = TerminalMenu(mirrors)
    index = menu.show()
    mirror = mirrors[index]
    if index > 0:
        subprocess.run([".venv/bin/pip", "config", "--site", "-q", "set", "global.index-url", mirror])
    Console.ok(mirror)


def install_deps():
    req_files = sorted(x.name for x in Path(".").glob("requirements*.txt"))
    if not req_files:
        return

    Console.plain("🔨 Install deps from requirements*.txt ?")
    req_files.insert(0, "skip")
    menu = TerminalMenu(req_files)
    index = menu.show()
    req_file = req_files[index]
    if index > 0:
        subprocess.run([".venv/bin/pip", "install", "-r", req_file])
    Console.ok(req_file)


def main():
    vern, path = choose_pyvern()
    create_venv(vern, path)
    switch_mirror()
    install_deps()
    Console.ok("☕️ Ok, activate by 'source .venv/bin/activate'")


if __name__ == "__main__":
    main()
