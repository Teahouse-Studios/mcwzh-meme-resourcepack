import json
from argparse import ArgumentParser

# WIP


def dump(max: int):
    with open("enchlevelfixS.json", 'w', encoding='utf8') as e:
        json.dump({f'enchantment.level.{i}': f'{i}' for i in range(11, max + 1)},
                  e, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    def generate_parser():
        parser = ArgumentParser(
            description="Generate enchantment level fix json.")
        parser.add_argument('max', type=int, help='wanted max level.')
        return parser
    args = generate_parser().parse_args()
    dump(args.max)
