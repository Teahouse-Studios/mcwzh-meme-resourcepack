import json
import argparse
import re
import sys

def main():
    parser = generate_parser()
    args = vars(parser.parse_args())
    out = generate_conversion(args)
    if args['outfile']:
        filename = args['outfile']
        with open(filename, 'w', encoding='utf8') as f:
            json.dump(out, f, ensure_ascii=False, indent=4)
    else:
        json.dump(out, sys.stdout, ensure_ascii=False)

def convert(identifier: str, json1: dict, json2:dict) -> dict:
    if json2[identifier]:
        return {json1[identifier]:json2[identifier]}
    else:
        warn = '[WARN] "%s" does not exist in the second json, skipping' % identifier
        print("\033[33m%s\033[0m" % warn)
        return {}

def generate_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Do S/T conversion by reading from two language files.")
    parser.add_argument("json1", help="path to the first json. Would be the keys in the output.")
    parser.add_argument("json2", help="path to the second json. Would be the values in the output.")
    parser.add_argument("regex", help="specify the regex.")
    parser.add_argument(
        "--outfile", "-o", help="specify the name of sorted json. If omitted, will output the json to stdout.")

    return parser

def generate_conversion(args: dict) -> dict:
    with open(args["json1"], 'r', encoding='utf8') as f:
        json1 = json.load(f)
    with open(args["json2"], 'r', encoding='utf8') as s:
        json2 = json.load(s)
    identifiers = list(json1.keys())
    matched_identifiers = []
    for i in identifiers:
        if re.match(args['regex'],i):
            matched_identifiers.append(i)
    conversion = {}
    for i in matched_identifiers:
        conversion.update(convert(i, json1, json2))
    return conversion

if __name__ == '__main__':
    main()