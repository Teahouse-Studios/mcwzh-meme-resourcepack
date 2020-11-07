from argparse import ArgumentParser, FileType
from json import load


def generate_parser():
    parser = ArgumentParser(
        description='Print keys in the first json but not in the second one.')
    parser.add_argument("json1", type=FileType(
        'r', encoding='utf8'), help='First json')
    parser.add_argument("json2", type=FileType(
        'r', encoding='utf8'), help='Second json')
    return parser


if __name__ == '__main__':
    args = generate_parser().parse_args()
    d = load(args.json2)
    print(*(k for k in load(args.json1) if k not in d), sep='\n')
