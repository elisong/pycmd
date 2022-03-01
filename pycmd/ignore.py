# -*- coding: utf-8 -*-
# Description: Fetch .gitignore Template
# Usage: ignore [-h] language
import argparse
import json
from urllib.request import urlopen

from .utils import Console


parser = argparse.ArgumentParser(prog="ignore", description="Fetch .gitignore Template")
parser.add_argument("language", type=str, default="Python", help="language")
args = parser.parse_args()


def language_info():
    url = "https://api.github.com/gitignore/templates"
    return json.load(urlopen(url))


def gitignore(language):
    url = f"https://api.github.com/gitignore/templates/{language}"
    return json.load(urlopen(url))


def main():
    languages = language_info()
    if args.language.lower() not in [language.lower() for language in languages]:
        Console.error("Choose language from below:")
        for language in languages:
            Console.plain(language)
        return

    language = [language for language in languages if language.lower() == args.language.lower()]
    content = gitignore(language)
    with open(".gitignore", "w+") as f:
        f.write(content["source"])
        Console.info("Saved in '.gitignore' ☕️")


if __name__ == "__main__":
    main()
