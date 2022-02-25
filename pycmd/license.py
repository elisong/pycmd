# -*- coding: utf-8 -*-
# Description: Short for fetch .gitignore file form github
# Usage: ignore python
import argparse
from urllib.request import urlopen
import json
import subprocess
from datetime import datetime

LICENSE_FILE = "LICENSE"

parser = argparse.ArgumentParser(prog="license", description="Fetch license from github api")
parser.add_argument("key", type=str, help="License key")
args = parser.parse_args()
key = args.key.lower()
license_year = str(datetime.now().year)
license_user = subprocess.check_output(["git", "config", "--get", "user.name"], encoding="utf8").strip()


def main():
    url = "https://api.github.com/licenses/" + key
    body = json.load(urlopen(url))["body"]
    if key in ("mit", "bsd-3-claus", "bsd-2-clause"):
        output = body.replace("[year]", license_year).replace("[fullname]", license_user)
    elif key == "apache-2.0":
        output = body.replace("[yyyy]", license_year).replace("[name of copyright owner]", license_user)
    else:
        output = body
    with open(LICENSE_FILE, "w+") as f:
        f.write(output)


if __name__ == "__main__":
    main()
