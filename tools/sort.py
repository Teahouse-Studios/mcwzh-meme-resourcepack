def sort(origin):
    return {k: origin[k] for k in sorted(origin)}


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType
    from json import load, dump
    from sys import stdout

    def generate_parser() -> ArgumentParser:
        parser = ArgumentParser(description="Sort a json by key.")
        parser.add_argument("json", type=FileType(
            mode='r', encoding='utf8'), help="path to the json.")
        parser.add_argument("--outfile", "-o", nargs='?', default=stdout, type=FileType(mode='w', encoding='utf8'),
                            help="specify the name of sorted json. If omitted, will output the json to stdout.")
        return parser
    args = generate_parser().parse_args()
    dump(load(args.json), args.outfile,
         ensure_ascii=False, indent=4, sort_keys=True)
