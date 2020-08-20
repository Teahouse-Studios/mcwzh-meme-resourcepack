import json
import argparse
import re
import sys


def generate_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Do S/T conversion by reading from two language files.")
    parser.add_argument(
        "json1", help="path to the first json. Would be the keys in the output.")
    parser.add_argument(
        "json2", help="path to the second json. Would be the values in the output.")
    parser.add_argument("regex", help="specify the regex.")
    parser.add_argument(
        "--outfile", "-o", help="specify the name of sorted json. If omitted, will output the json to stdout.")
    return parser


def generate_conversion(args) -> dict:
    json1 = json.load(open(args.json1, 'r', encoding='utf8'))
    json2 = json.load(open(args.json2, 'r', encoding='utf8'))
    print(*(f'\033[33mWarning: "{k}" does not exist in the second json, skipping.\033[0m' for k in json1 if re.match(
        args.regex, k) and k not in json2), sep='\n')
    return dict((json1[k], json2[k]) for k in json1 if re.match(args.regex, k) and k in json2)


if __name__ == '__main__':
    args = generate_parser().parse_args()
    out = generate_conversion(args)
    if args.outfile:
        json.dump(out, open(args.outfile, 'w', encoding='utf8'),
                  ensure_ascii=False, indent=4)
    else:
        json.dump(out, sys.stdout, ensure_ascii=False)
