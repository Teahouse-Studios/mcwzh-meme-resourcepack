import argparse
import json
import sys


def sort(origin): return {k: origin[k] for k in sorted(list(origin))}


def generate_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sort a json by key.")
    parser.add_argument("json", help="path to the json.")
    parser.add_argument(
        "--outfile", "-o", help="specify the name of sorted json. If omitted, will output the json to stdout.")
    return parser


if __name__ == '__main__':
    args = generate_parser().parse_args()
    after = sort(json.load(open(args.json, "r", encoding="utf-8")))
    if args.outfile:
        json.dump(after, open(args.outfile, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=4)
    else:
        json.dump(after, sys.stdout, ensure_ascii=False)
