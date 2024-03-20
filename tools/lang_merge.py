from argparse import ArgumentParser, FileType
from json import load, dump

def generate_parser():
    parser = ArgumentParser(
        description='Merge both json files in output.json file.')
    parser.add_argument("json1", type=FileType(
        'r', encoding='utf8'), help='First json')
    parser.add_argument("json2", type=FileType(
        'r', encoding='utf8'), help='Second json')
    return parser


if __name__ == '__main__':
    args = generate_parser().parse_args()
    dict1 = load(args.json1)
    dict2 = load(args.json2)
    a = dict()
    for i in dict1:
        if i not in dict2:
            a[i] = dict1[i]
    dict2.update(a)
    out= open('output.json','w', encoding='utf8')
    dump(dict2, out, ensure_ascii=False, indent=4, sort_keys=True)