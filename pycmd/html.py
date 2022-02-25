# -*- coding: utf-8 -*-
# Description: Short for pandas's read_html
# Usage: html url [-m] [--match MATCH] [-a] [--attr ATTR] [-o] [--output-file OUTPUT-FILE]
import argparse
import pandas as pd
from pathlib import Path


parser = argparse.ArgumentParser(prog="html", description="Short for pandas's read_html")
parser.add_argument("url", type=str, help="target url")
parser.add_argument("-m", "--match", type=str, help="target expression")
parser.add_argument("-a", "--attrs", type=str, help="target html attrs")
parser.add_argument("-o", "--output-file", type=str, help="output file")
args = parser.parse_args()


def main():
    # --attrs 'key1=val1,key2=val2'
    if args.attrs:
        attrs = dict([kv.split("=") for kv in args.attrs.strip().split(",")])
    else:
        attrs = None
    match = args.match or ".+"
    tables = pd.read_html(args.url, match=match, attrs=attrs)
    for table in tables:
        print("\n\n")
        print(table)

    if args.output_file:
        path = Path(args.output_file)
        if len(tables) > 1:
            for i, table in enumerate(tables):
                new_file = f"{path.stem}_{str(i).zfill(2)}{path.suffix}"
                new_path = Path(path.parent, new_file)
                table.to_csv(new_path)
                print(f"☕️ Saved in {new_path.as_posix()}.")
        else:
            tables[0].to_csv(path)
            print(f"☕️ Saved in {path.as_posix()}.")


if __name__ == "__main__":
    main()
