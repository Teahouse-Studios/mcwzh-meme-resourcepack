import os
from argparse import ArgumentParser
from sys import stderr
from packaging.pack_builder import pack_builder
from packaging.module_checker import module_checker


def build(args: dict):
    build_info = []
    current_path = os.getcwd()

    def raise_warning(warn: str):
        build_info.append(f'Warning: {warn}')
        print(f'\033[33mWarning: {warn}\033[0m', file=stderr)
    # init module_checker
    checker = module_checker()
    checker.module_path = os.path.join(current_path, "modules")
    # checking module integrity
    checker.check_module()
    if checker.info != "":
        raise_warning(checker.info)
    builder = pack_builder(current_path, os.path.join(
        current_path, "modules"), checker.module_list, os.path.join(current_path, "mods"))
    builder.args = args
    builder.build()
    build_info.append(builder.logs)
    return build_info, builder.warning_count, builder.error_count


if __name__ == "__main__":
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
        parser.add_argument('-m', '--mod', nargs='*', default='none',
                            help="(Experimental) Include mod string files. Should be file names in 'mods/' folder, 'all' or 'none'. Defaults to 'none'. Pseudoly accepts a path, but only files in 'mods/' work.")
        parser.add_argument('-f', '--format', type=int,
                            help='Specify "pack_format". when omitted, will default to 3 if build type is "legacy" and 6 if build type is "normal" or "compat". A wrong value will cause the build to fail.')
        parser.add_argument('-o', '--output', nargs='?', default='builds',
                            help="Specify the location to output packs. Default location is 'builds/' folder.")
        parser.add_argument('--hash', action='store_true',
                            help="Add a hash into file name.")
        return parser
    args = vars(generate_parser().parse_args())
    if args['type'] == 'clean':
        for i in os.listdir('builds/'):
            os.remove(os.path.join('builds', i))
        print("\nDeleted all packs built.")
    else:
        build(args)
