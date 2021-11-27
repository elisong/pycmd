# -*- coding: utf-8 -*-
# Short for fetch .gitignore file form github.
# Usage: ignore python
import argparse
from urllib.request import urlopen
import json

GITIGNORE_FILE = '.gitignore'
parser = argparse.ArgumentParser(
    prog='ignore', description='Fetch .gitignore from github template')
parser.add_argument('language', type=str, help='Language')
args = parser.parse_args()


def main():
    url = 'https://api.github.com/gitignore/templates/' + args.language.capitalize()
    resp = urlopen(url)
    data = json.load(resp)
    with open(GITIGNORE_FILE, 'w+') as f:
        f.write(data['source'])


if __name__ == "__main__":
    main()
