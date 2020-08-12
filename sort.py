import argparse
import json
import sys


def sort(origin: dict) -> dict:
    return {k: origin[k] for k in sorted(list(origin))}


def generate_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sort a json by key.")
    parser.add_argument("json", help="path to the json.")
    parser.add_argument(
        "--outfile", "-o", help="specify the name of sorted json. If omitted, will output the json to stdout.")
    return parser


if __name__ == '__main__':
    args = generate_parser().parse_args()
    before = json.load(open(args.json, "r", encoding="utf-8"))
    after = sort(before)
    if args.outfile:
        json.dump(fp=open(args.outfile, "w", encoding="utf-8"), obj=after, ensure_ascii=False, indent=4)
    else:
        json.dump(after, sys.stdout, ensure_ascii=False)
