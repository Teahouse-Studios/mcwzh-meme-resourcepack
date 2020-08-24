from argparse import ArgumentParser
from json import load, dump
from sys import stdout


def sort(origin): return {k: origin[k] for k in sorted(list(origin))}


def generate_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Sort a json by key.")
    parser.add_argument("json", help="path to the json.")
    parser.add_argument(
        "--outfile", "-o", help="specify the name of sorted json. If omitted, will output the json to stdout.")
    return parser


if __name__ == '__main__':
    args = generate_parser().parse_args()
    file = load(open(args.json, "r", encoding="utf-8"))
    if args.outfile:
        dump(file, open(args.outfile, "w", encoding="utf-8"),
             ensure_ascii=False, indent=4, sort_keys=True)
    else:
        dump(file, stdout, ensure_ascii=False, sort_keys=True)
