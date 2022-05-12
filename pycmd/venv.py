# -*- coding: utf-8 -*-
# Description: Create Python Virtual-Env on MacOS.
# Usage: venv [-d DIRECTORY]
import argparse
import shutil
import subprocess
from pathlib import Path

from InquirerPy import prompt

from .utils import Console


parser = argparse.ArgumentParser(prog="venv", description="Create Python Virtual-Env")
parser.add_argument("-d", "--directory", type=str, default=".venv", help="directory")
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

    question = [
        {
            "type": "list",
            "name": "verns",
            "message": "version",
            "choices": verns,
        }
    ]
    vern = prompt(question)["verns"]
    path = paths[verns.index(vern)]
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
    pip_vern = subprocess.run(f"{args.directory}/bin/pip --version", text=True, capture_output=True)
    Console.info(f"Upgrade pip itself to {pip_vern.stdout.strip().split(' ')[1]}")


def switch_mirror():
    Console.info("Switch pip mirror ?")
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
            "message": "mirror",
            "choices": mirrors,
        }
    ]
    mirror = prompt(question)["mirrors"]
    if mirror != "skip":
        subprocess.run([f"{args.directory}/bin/pip", "config", "--site", "-q", "set", "global.index-url", mirror])
    Console.info(mirror)


def install_deps():
    req_files = sorted(x.name for x in Path(".").glob("requirements*.txt"))
    if not req_files:
        return

    Console.info("Install from requirements*.txt ?")
    req_files.insert(0, "skip")
    question = [
        {
            "type": "list",
            "name": "req_files",
            "message": "requirements*.txt",
            "choices": req_files,
        }
    ]
    req_file = prompt(question)["req_files"]

    if req_file != "skip":
        subprocess.run([f"{args.directory}/bin/pip", "install", "-r", req_file])
    Console.info(req_file)


def main():
    path = choose_pyvern()
    create_venv(path)
    switch_mirror()
    install_deps()
    Console.info(f"Activate by 'source {args.directory}/bin/activate' ☕️")


if __name__ == "__main__":
    main()
