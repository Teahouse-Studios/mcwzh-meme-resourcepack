from os.path import join, dirname, basename

if __name__ == f'{basename(dirname(__file__))}.build':
    from .packaging.pack_builder import pack_builder
    from .packaging.module_checker import module_checker
else:
    from packaging.pack_builder import pack_builder
    from packaging.module_checker import module_checker


def check_module(module_path=None):
    module_path = module_path or join(dirname(__file__), "modules")
    checker = module_checker(module_path)
    checker.check_module()
    return checker.module_info, checker.check_info_list


def build(args: dict):
    current_dir = dirname(__file__)
    module_info, _ = check_module()
    builder = pack_builder(
        join(current_dir, "meme_resourcepack"), module_info, join(current_dir, "mods"), join(current_dir, "mappings"))
    builder.args = args
    builder.build()
    return builder.filename, builder.warning_count, builder.error


if __name__ == "__main__":
    from argparse import ArgumentParser
    from os import remove, listdir
    from os.path import exists, isdir, curdir

    def generate_parser() -> ArgumentParser:
        parser = ArgumentParser(
            description="Automatically build resourcepacks")
        parser.add_argument('type', default='normal', choices=[
            'normal', 'compat', 'legacy', 'clean'], help="Build type. Should be 'normal', 'compat', 'legacy' or 'clean'. If it's 'clean', all packs in 'builds/' directory will be deleted. Implies '--format 3' when it's 'legacy'.")
        parser.add_argument('-r', '--resource', nargs='*', default='all',
                            help="(Experimental) Include resource modules. Should be module names, 'all' or 'none'. Defaults to 'all'.")
        parser.add_argument('-l', '--language', nargs='*', default='none',
                            help="(Experimental) Include language modules. Should be module names, 'all' or 'none'. Defaults to 'none'.")
        parser.add_argument('-x', '--mixed', nargs='*', default='none',
                            help="(Experimental) Include mixed modules. Should be module names, 'all' or 'none'. Defaults to 'none'.")
        parser.add_argument('-s', '--sfw', action='store_true',
                            help="Use 'suitable for work' strings, equals to '--language sfw'.")
        parser.add_argument('-c', '--collection', nargs='*', default='none',
                            help="(Experimental) Include module collections. Should be module names, 'all' or 'none'. Defaults to 'none'.")
        parser.add_argument('-m', '--mod', nargs='*', default='none',
                            help="(Experimental) Include mod string files. Should be file names in 'mods/' folder, 'all' or 'none'. Defaults to 'none'. Pseudoly accepts a path, but only files in 'mods/' work.")
        parser.add_argument('-f', '--format', type=int,
                            help='Specify "pack_format". when omitted, will default to 3 if build type is "legacy" and 6 if build type is "normal" or "compat". A wrong value will cause the build to fail.')
        parser.add_argument('-o', '--output', nargs='?', default='builds',
                            help="Specify the location to output packs. Default location is 'builds/' folder.")
        parser.add_argument('--hash', action='store_true',
                            help="Add a hash into file name.")
        return parser

    def handle_args(args: dict):
        module_types = 'resource', 'language', 'mixed', 'collection'
        args['modules'] = {key: args.pop(key) for key in module_types}
        if args['sfw'] and 'sfw' not in args['modules']['language']:
            args['modules']['language'].append('sfw')
        return args

    args = handle_args(vars(generate_parser().parse_args()))
    if args['type'] == 'clean':
        target = join(curdir, args['output'])
        if exists(target) and isdir(target):
            for i in listdir(target):
                remove(join(target, i))
            print(f'Cleaned up "{target}".')
        else:
            print(f'\033[1;31mError: "{target}" is not valid.\033[0m')
    else:
        build(args)
