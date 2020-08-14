import json
import argparse

# WIP


def dump(max: int):
    json.dump({f'enchantment.level.{i}': f'{i}' for i in range(11, max + 1)}, open("enchlevelfixS.json", 'w', encoding='utf8'),
              indent=4, ensure_ascii=False)


def generate_parser():
    parser = argparse.ArgumentParser(
        description="Generate enchantment level fix json.")
    parser.add_argument('max', help='wanted max level.')
    return parser


if __name__ == '__main__':
    args = generate_parser().parse_args()
    dump(int(args.max))
