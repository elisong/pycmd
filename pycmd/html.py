# -*- coding: utf-8 -*-
# Description: Read HTML Table
# Usage: html [-h] [-m MATCH] [-a ATTRS] [-o OUTPUT_FILE] url
import argparse
from pathlib import Path
import pandas as pd
from .utils import Console


parser = argparse.ArgumentParser(prog="html", description="Read HTML Table")
parser.add_argument("-m", "--match", type=str, help="regular expression")
parser.add_argument("-a", "--attrs", type=str, help="html attributes, comma sep")
parser.add_argument("-o", "--output-file", type=str, help="output file")
parser.add_argument("url", type=str, help="target url")
args = parser.parse_args()


def main():
    # --attrs 'key1=val1,key2=val2'
    if args.attrs:
        attrs = dict([kv.split("=") for kv in args.attrs.strip().split(",")])
    else:
        attrs = None
    match = args.match or ".+"
    try:
        tables = pd.read_html(args.url, match=match, attrs=attrs)
        Console.info(f"Crawl {len(tables)} tables")
        [print(f"\n{table}") for table in tables]

        if args.output_file:
            path = Path(args.output_file)
            if len(tables) > 1:
                for i, table in enumerate(tables):
                    new_file = f"{path.stem}_{str(i).zfill(2)}{path.suffix}"
                    new_path = Path(path.parent, new_file)
                    table.to_csv(new_path)
                    Console.info(f"Save in '{new_path.as_posix()}' ☕️")
            else:
                tables[0].to_csv(path)
                Console.info(f"Save in '{path.as_posix()}' ☕️")

    except ValueError as e:
        Console.warn(e)


if __name__ == "__main__":
    main()
