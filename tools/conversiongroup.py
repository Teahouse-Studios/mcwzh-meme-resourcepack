from json import load, dump
from re import match


def generate_conversion(json1, json2, json3, regex) -> list:
    print(*(f'\033[33mWarning: "{k}" does not exist in the Traditional Chinese json, skipping.\033[0m' for k in json1 if match(
        regex, k) and k not in json2), sep='\n')
    print(*(f'\033[33mWarning: "{k}" does not exist in the Original json, skipping.\033[0m' for k in json1 if match(
        regex, k) and k not in json3), sep='\n')
    return '\n'.join(f"{{type = 'item', original = '{json3[k]}', rule = 'zh:{json1[k]};zh-cn:{json1[k]};zh-tw:{json2[k]};', description = '{k}'}}," for k in json1 if match(regex, k) and k in json2 and k in json3)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType
    from sys import stdout

    def generate_parser() -> ArgumentParser:
        parser = ArgumentParser(
            description="Do S/T conversion group modules by reading from three language files.")
        parser.add_argument("json1", type=FileType(mode='r', encoding='utf8'),
                            help="path to the Simplified Chinese json. Would be the S part in the output.")
        parser.add_argument("json2", type=FileType(mode='r', encoding='utf8'),
                            help="path to the Traditional Chinese json. Would be the T part in the output.")
        parser.add_argument("json3", type=FileType(mode='r', encoding='utf8'),
                            help="path to the Original json. Would be the original part in the output.")
        parser.add_argument("regex", help="specify the regex.")
        parser.add_argument("--outfile", "-o", nargs='?', default=stdout, type=FileType(mode='w', encoding='utf8'),
                            help="specify the name of output json. If omitted, will output the json to stdout.")
        return parser
    args = generate_parser().parse_args()
    out = generate_conversion(load(args.json1), load(
        args.json2), load(args.json3), args.regex)
    dump(out, args.outfile, ensure_ascii=False, indent=4, sort_keys=True)
