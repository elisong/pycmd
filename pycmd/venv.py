# -*- coding: utf-8 -*-
# Description: Create Python Virtual-Env on MacOS.
# Usage: venv [-d DIR]
import argparse
import shutil
import subprocess
from pathlib import Path

from InquirerPy import prompt

from .utils import Console


parser = argparse.ArgumentParser(prog="venv", description="Create Python Virtual-Env")
parser.add_argument("-d", "--dir", type=str, default=".venv", help="dir")
args = parser.parse_args()


def choose_pyvern():
    cellar = []
    if Path("/usr/local/Cellar").is_dir():
        cellar.append(Path("/usr/local/Cellar"))
    if Path("/opt/homebrew/Cellar").is_dir():
        cellar.append(Path("/opt/homebrew/Cellar"))

    verns = sorted(x.name.capitalize() for c in cellar for x in c.glob("python@3*"))
    paths = sorted(str(x) for c in cellar for x in c.glob("python@3*/3.*/bin/python3"))

    question = [
        {
            "type": "list",
            "name": "verns",
            "message": "Which Python prefer ?",
            "choices": verns,
        }
    ]
    vern = prompt(question)["verns"]
    path = paths[verns.index(vern)]
    return path


def create_venv(path):
    Console.info(f"Create virtual environment in {args.dir}")
    try:
        shutil.rmtree(args.dir)
    except FileNotFoundError:
        pass
    subprocess.run([path, "-m", "venv", args.dir])
    subprocess.run([f"{args.dir}/bin/pip", "install", "-U", "pip"], stdout=subprocess.DEVNULL)


def switch_mirror():
    mirrors = [
        "skip",
        "https://mirrors.cloud.tencent.com/pypi/simple",
        "https://pypi.tuna.tsinghua.edu.cn/simple",
        "https://pypi.mirrors.ustc.edu.cn/simple/",
    ]
    question = [
        {
            "type": "list",
            "name": "mirrors",
            "message": "Which pip mirror prefer ?",
            "choices": mirrors,
        }
    ]
    mirror = prompt(question)["mirrors"]
    if mirror != "skip":
        subprocess.run([f"{args.dir}/bin/pip", "config", "--site", "-q", "set", "global.index-url", mirror])


def install_deps():
    req_files = sorted(x.name for x in Path(".").glob("requirements*.txt"))
    if not req_files:
        return

    req_files.insert(0, "skip")
    question = [
        {
            "type": "list",
            "name": "req_files",
            "message": "Install from requirements*.txt ?",
            "choices": req_files,
        }
    ]
    req_file = prompt(question)["req_files"]

    if req_file != "skip":
        subprocess.run([f"{args.dir}/bin/pip", "install", "-r", req_file])


def main():
    path = choose_pyvern()
    create_venv(path)
    switch_mirror()
    install_deps()
    Console.info(f"☕️ Finished, start by 'source {args.dir}/bin/activate'")


if __name__ == "__main__":
    main()
