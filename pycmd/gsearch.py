# -*- coding: utf-8 -*-
# Description: Search from google
# Usage: gsearch [-h] [--site SITE] [--filetype FILETYPE] [--intitle INTITLE]
#               [--inurl INURL] [--link LINK] [--proxy-host PROXY_HOST]
#               [--proxy-port PROXY_PORT] [-n NUM] [-o OUTPUT_FILE]
#               [-t OUTPUT_TITLE]
#               query
import sys
import argparse
import subprocess

parser = argparse.ArgumentParser(prog="gsearch", description="Google Search Command")
parser.add_argument("query", type=str, help="Query")
parser.add_argument("--site", type=str, help="Restricted to specified site")
parser.add_argument("--filetype", type=str, help="Restricted to specified type documents")
parser.add_argument("--intitle", type=str, help="Restricted to pages with specified title")
parser.add_argument("--inurl", type=str, help="Restricted to pages with specified word in url")
parser.add_argument("--link", type=str, help="Restricted to pages that links to specified web")
parser.add_argument("--proxy-host", type=str, help="Socks5 proxy host")
parser.add_argument("--proxy-port", type=int, help="Socks5 proxy port")
parser.add_argument("-n", "--num", type=int, default=10, help="max number of pages return")
parser.add_argument("-o", "--output-file", type=str, help="output markdown file name")
parser.add_argument("-t", "--output-title", type=str, help="output content title")
args = parser.parse_args()


def check_deps():
    if args.proxy_host and args.proxy_port:
        python = sys.executable
        subprocess.check_call([python, "-m", "pip", "install", "pysocks"], stdout=subprocess.DEVNULL)


check_deps()

if args.proxy_host and args.proxy_port:
    import socket
    import socks

    socks.set_default_proxy(socks.SOCKS5, args.proxy_host, args.proxy_port)
    socket.socket = socks.socksocket
from bs4 import BeautifulSoup
from googlesearch import search, get_page
from mdutils.mdutils import MdUtils


def get_links():
    query = args.query
    query += f" site:{args.site}" if args.site else ""
    query += f" filetype:{args.filetype}" if args.filetype else ""
    query += f" intitle:{args.intitle}" if args.intitle else ""
    query += f" inurl:{args.inurl}" if args.inurl else ""
    query += f" link:{args.link}" if args.link else ""
    links = []
    for url in search(query, stop=args.num):
        try:
            soup = BeautifulSoup(get_page(url), features="lxml")
            link = "[" + soup.title.string + "](" + url + ")"
            print("> - " + link)
            links.append(link)
        except Exception:
            pass
    return links


def main():
    command = " ".join(sys.argv)
    print("> 开始执行`%s`" % command)
    file_name = args.output_file or args.query
    title = args.output_title or args.query
    mdFile = MdUtils(file_name=file_name, title=title)
    print("> 待创建" + file_name + ".md文档\n")
    mdFile.new_paragraph("> 以下内容由命令 `%s` 生成\n" % command)
    links = get_links()
    mdFile.new_list(items=links)
    mdFile.create_md_file()
    print("> 🤠OK")


if __name__ == "__main__":
    main()
