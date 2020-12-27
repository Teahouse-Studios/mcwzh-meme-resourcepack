from io import TextIOWrapper
from json import load, dump
from re import match


def generate_conversion_list(json1, json2, json3, regex) -> list:
    print(*(f'\033[33mWarning: "{k}" does not exist in the second json, skipping.\033[0m' for k in json1 if match(
        regex, k) and k not in json2), sep='\n')
    return list({'zh':json1[k], 'zh-cn':json1[k], 'zh-tw':json2[k], 'original': json3[k], 'description': k} for k in json1 if match(args.regex, k) and k in json2)

def generate_conversion_group(list) -> str:
    a = ''
    for k in list:
        original = k['original']
        zh = k['zh']
        zh_cn = k['zh-cn']
        zh_tw = k['zh-tw']
        description = k['description']
        a += f"{{type = 'item', original = '{original}', rule = 'zh:{zh};zh-cn:{zh_cn};zh-tw:{zh_tw};', description = '{description}'}},\n"
    return a

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType
    from sys import stdout

    def generate_parser() -> ArgumentParser:
        parser = ArgumentParser(
            description="Do S/T conversion group modules by reading from three language files.")
        parser.add_argument("json1", type=FileType(mode='r', encoding='utf8'),
                            help="path to the first json. Would be the S part in the output.")
        parser.add_argument("json2", type=FileType(mode='r', encoding='utf8'),
                            help="path to the second json. Would be the T part in the output.")
        parser.add_argument("json3", type=FileType(mode='r', encoding='utf8'), 
                            help="path to the third json. Would be the original part in the output.")
        parser.add_argument("regex", help="specify the regex.")
        parser.add_argument("--outfile", "-o", nargs='?', type=str,
                            help="specify the name of sorted json. If omitted, will output the json to stdout.")
        return parser
        # default=stdout, type=FileType(mode='w', encoding='utf8'),
    args = generate_parser().parse_args()
    out = generate_conversion_group(generate_conversion_list(load(args.json1), load(args.json2), load(args.json3), args.regex))
    print(out)
    # dump(out, args.outfile, ensure_ascii=False, indent=4, sort_keys=True)
    with open(args.outfile, mode='w', encoding='utf8') as f:
        f.write(out)
