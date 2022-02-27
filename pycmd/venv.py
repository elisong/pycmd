# -*- coding: utf-8 -*-
# Description: Create python virtual environment on MacOS.
# Usage: venv
import argparse
from pathlib import Path
import shutil
import subprocess
from simple_term_menu import TerminalMenu
from .utils import Console

parser = argparse.ArgumentParser(prog="venv", description="Create Python virtual environment")
parser.add_argument("-d", "--directory", type=str, default='.venv', help="directory")
args = parser.parse_args()


def choose_pyvern():
    Console.info("Which Python version prefer ?")
    cellar = []
    if Path("/usr/local/Cellar").is_dir():
        cellar.append(Path("/usr/local/Cellar"))
    if Path("/opt/homebrew/Cellar").is_dir():
        cellar.append(Path("/opt/homebrew/Cellar"))

    verns = sorted(x.name.capitalize() for c in cellar for x in c.glob("python@3*"))
    paths = sorted(str(x) for c in cellar for x in c.glob("python@3*/3.*/bin/python3"))

    menu = TerminalMenu(verns)
    index = menu.show()
    vern = verns[index]
    path = paths[index]
    Console.info(vern)
    return path


def create_venv(path):
    Console.info(f"Create virtual environment in {args.directory}")
    try:
        shutil.rmtree(args.directory)
    except FileNotFoundError:
        pass
    subprocess.run([path, "-m", "venv", args.directory])

    subprocess.run([f"{args.directory}/bin/pip", "install", "-U", "pip"], stdout=subprocess.DEVNULL)
    pip_vern = subprocess.run(f"{args.directory}/bin/pip --version" + " | awk '{print $2}'", shell=True, text=True,capture_output=True)
    Console.info(f"Upgrade pip itself to {pip_vern.stdout.strip()}")


def switch_mirror():
    Console.info("Switch pip mirror ?")
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
        subprocess.run([f"{args.directory}/bin/pip", "config", "--site", "-q", "set", "global.index-url", mirror])
    Console.info(mirror)


def install_deps():
    req_files = sorted(x.name for x in Path(".").glob("requirements*.txt"))
    if not req_files:
        return

    Console.info("Install from requirements*.txt ?")
    req_files.insert(0, "skip")
    menu = TerminalMenu(req_files)
    index = menu.show()
    req_file = req_files[index]
    if index > 0:
        subprocess.run([f"{args.directory}/bin/pip", "install", "-r", req_file])
    Console.info(req_file)


def main():
    path = choose_pyvern()
    create_venv(path)
    switch_mirror()
    install_deps()
    Console.info(f"Activate via 'source {args.directory}/bin/activate' ☕️")


if __name__ == "__main__":
    main()
