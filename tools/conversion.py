from json import load, dump
from re import match


def generate_conversion(json1, json2, regex) -> dict:
    print(*(f'\033[33mWarning: "{k}" does not exist in the second json, skipping.\033[0m' for k in json1 if match(
        regex, k) and k not in json2), sep='\n')
    return dict((json1[k], json2[k]) for k in json1 if match(args.regex, k) and k in json2)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType
    from sys import stdout

    def generate_parser() -> ArgumentParser:
        parser = ArgumentParser(
            description="Do S/T conversion by reading from two language files.")
        parser.add_argument("json1", type=FileType(mode='r', encoding='utf8'),
                            help="path to the first json. Would be the keys in the output.")
        parser.add_argument("json2", type=FileType(mode='r', encoding='utf8'),
                            help="path to the second json. Would be the values in the output.")
        parser.add_argument("regex", help="specify the regex.")
        parser.add_argument("--outfile", "-o", nargs='?', default=stdout, type=FileType(mode='w', encoding='utf8'),
                            help="specify the name of sorted json. If omitted, will output the json to stdout.")
        return parser
    args = generate_parser().parse_args()
    out = generate_conversion(load(args.json1), load(args.json2), args.regex)
    dump(out, args.outfile, ensure_ascii=False, indent=4, sort_keys=True)
