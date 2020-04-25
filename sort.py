import argparse
import json
import sys


def sort(origin: dict) -> dict:
    out = {}
    keylist = [i for i in origin.keys()]
    keylist.sort()
    for k in keylist:
        out.update({k: origin[k]})
    return out


def generate_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sort a json by key.")
    parser.add_argument("json", help="path to the json.")
    parser.add_argument(
        "--outfile", "-o", help="specify the name of sorted json. If omitted, will output the json to stdout.")
    return parser


if __name__ == '__main__':
    parser = generate_parser()
    args = vars(parser.parse_args())
    with open(args['json'], 'r', encoding='utf8') as d:
        indata = dict(json.load(d))
    out = sort(indata)
    if args['outfile']:
        filename = args['outfile']
        with open(filename, 'w', encoding='utf8') as f:
            json.dump(out, f, ensure_ascii=False, indent=4)
    else:
        json.dump(out, sys.stdout, ensure_ascii=False)
