# -*- coding: utf-8 -*-
# Description: Fetch License Template
# Usage: license [-h] [-o OUTPUT_FILE] key
import argparse
import json
import subprocess
from datetime import datetime
from urllib.request import urlopen

from .utils import Console


parser = argparse.ArgumentParser(prog="license", description="Fetch License Template")
parser.add_argument("key", type=str, default="mit", help="license key")
parser.add_argument("-o", "--output-file", type=str, default="LICENSE", help="license file")
args = parser.parse_args()


license_year = str(datetime.now().year)
license_user = subprocess.check_output(["git", "config", "--get", "user.name"], encoding="utf8").strip()


def licenses_info():
    url = "https://api.github.com/licenses"
    return json.load(urlopen(url))


def license_content(key):
    url = f"https://api.github.com/licenses/{key}"
    body = json.load(urlopen(url))["body"]
    if key in ("mit", "bsd-3-claus", "bsd-2-clause"):
        content = body.replace("[year]", license_year).replace("[fullname]", license_user)
    elif key == "apache-2.0":
        content = body.replace("[yyyy]", license_year).replace("[name of copyright owner]", license_user)
    else:
        content = body
    return content


def main():
    licenses = licenses_info()
    if args.key.lower() not in [license["key"] for license in licenses]:
        Console.error("Choose license key from below:")
        for license in licenses:
            Console.plain(license["key"])
        return

    content = license_content(args.key.lower())
    with open(args.output_file, "w+") as f:
        f.write(content)
        Console.info(f"Saved in '{args.output_file}' ☕️")


if __name__ == "__main__":
    main()
