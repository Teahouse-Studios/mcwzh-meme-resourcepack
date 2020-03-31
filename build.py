import zipfile
import json
import argparse
import os
import warnings
from pathlib import Path

mappings = ['addServer', 'advancements', 'advMode', 'attribute', 'book', 'build', 'chat',
            'commands', 'connect', 'container', 'controls', 'createWorld', 'death',
            'deathScreen', 'debug', 'demo', 'difficulty', 'disconnect', 'effect',
            'enchantment', 'entity', 'filled_map', 'gameMode', 'generator', 'gui', 'inventory',
            'item', 'itemGroup', 'key', 'language', 'lanServer', 'lingering_potion',
            'mcoServer', 'menu', 'merchant', 'mount', 'multiplayer', 'narrator', 'options',
            'potion', 'recipe', 'record', 'resourcePack', 'screenshot', 'selectServer',
            'selectWorld', 'sign', 'soundCategory', 'spectatorMenu', 'splash_potion',
            'stat', 'stats', 'structure_block', 'subtitles', 'tile', 'tipped_arrow',
            'title', 'translation', 'tutorial']

successful_pack_counter = 0
warning_pack_counter = 0
pack_counter = 0


def main():
    parser = argparse.ArgumentParser(
        description="Automatically build resourcepacks")
    parser.add_argument('type', default='normal', help="Build type. This should be 'all', 'normal' or 'compat'.", choices=[
                        'all', 'normal', 'compat'])
    parser.add_argument('-t', '--figure', default='all', choices=['all', 'none'],
                        help="Use or do not use figure textures or models when building resource packs. This should be 'all' or 'none'. For higher customizability, see '--mod-content'. If build type is 'all', this argument will be ignored.")
    parser.add_argument('-s', '--sfw', action='store_true',
                        help="Use 'suitable for work' strings. If build type is 'all', this argument will be ignored.")
    parser.add_argument('-l', '--legacy', action='store_true',
                        help="(Not fully implemented) Use legacy format (.lang) when building resource packs. If build type is 'all', this argument will be ignored.")
    parser.add_argument('-i', '-m', '--include', type=str, nargs='*',
                        help="(Not fully implemented) Include modification strings or folders. Should be path(s) to a file, folder or 'all'. If build type is 'all', this argument will be ignored.")
    parser.add_argument('-d', '--debug', action='store_true',
                        help="Output an individual language file. If build type is 'all', this argument will be ignored.")
    args = vars(parser.parse_args())
    if args['type'] == 'all':
        build_all()
    else:
        build(args)
    print("\n[INFO] Built %d pack(s) with %d pack(s) no warning" %
          (pack_counter, successful_pack_counter))


def build(args):
    global pack_counter
    global successful_pack_counter
    global warning_pack_counter
    if not args['debug']:
        warnings.filterwarnings("ignore")
    with open("assets/minecraft/lang/zh_meme.json", 'r', encoding='utf8') as f:
        lang_data = json.load(f)
    pack_name = get_packname(args)
    print("[INFO] Building " + pack_name)
    warning_counter = 0
    # all builds have these files
    pack = zipfile.ZipFile(
        pack_name, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=5)
    pack.write("pack.png")
    pack.write("LICENSE")
    # build without figures
    if args['figure'] == 'none':
        exclude_list = ['optional/brewing_stand_model',
                        'optional/totem_model', 'optional/observer_think']
        for i in exclude_list:
            for i in args['include']:
                args['include'].remove(i)
    # build with figures
    if args['figure'] == 'all':
        include_list = ['optional/brewing_stand_model',
                        'optional/totem_model', 'optional/observer_think']
        for i in include_list:
            if i not in args['include']:
                args['include'].append(i)
    # build with sfw
    if args['sfw']:
        args['include'].append('optional/sfw.json')
    # build with mod content
    moddata = {}
    if args['include']:
        if 'all' in args['include']:
            modlist = ['mods/' + i for i in os.listdir("mods")]
            modlist.extend(args['include'])
            modlist.remove('all')
        else:
            modlist = args['include']
        for file in modlist:
            if os.path.isfile(file):
                if file.endswith(".json"):
                    with open(file, encoding='utf8') as f:
                        moddata.update(json.load(f))
                elif file.endswith(".lang"):
                    with open(file, 'r', encoding='utf8') as f:
                        moddata_item = [i for i in f.read().splitlines() if (
                            i != '' and not i.startswith("#"))]
                    moddata.update(dict(i.split("=", 1) for i in moddata_item))
                else:
                    print(
                        '\033[33m[WARN] File extension "%s" is not supported, skipping\033[0m' % file[file.rfind('.') + 1:])
                    warning_counter += 1
            elif Path(file).is_dir():
                for item in Path(file).rglob('*'):
                    pack.write(item, str(item.relative_to(
                        '.').as_posix()).split(file, 1)[-1])
            else:
                print(
                    '\033[33m[WARN] File or folder "%s" does not exist, skipping\033[0m' % file)
                warning_counter += 1
        lang_data.update(moddata)
    # Processing mcmeta
    with open("pack.mcmeta", 'r', encoding='utf8') as meta:
        metadata = json.load(meta)
    # decide build type
    if args['type'] == 'normal':
        lang_name = "zh_meme"
    elif args['type'] == 'compat':
        del metadata['language']
        lang_name = "zh_cn"
    if not args['legacy']:
        lang_extension = ".json"
        # normal/compatible build
        pack.writestr("assets/minecraft/lang/" + lang_name + lang_extension,
                      json.dumps(lang_data, indent=4, ensure_ascii=True))
        if args['debug']:
            with open(lang_name + lang_extension, 'w') as debug_file:
                debug_file.write(json.dumps(
                    lang_data, indent=4, ensure_ascii=True))
    else:
        # legacy(1.12.2) build
        lang_extension = ".lang"
        legacy_lang_data = {}
        for file in mappings:
            file_name = file + ".json"
            if file_name not in os.listdir("mappings"):
                print(
                    "\033[33m[WARN] Missing mapping %s, skipping\033[0m" % file_name)
                warning_counter += 1
                pass
            else:
                location = "mappings/" + file_name
                with open(location, encoding='utf8') as f:
                    mapping = json.load(f)
                for k, v in mapping.items():
                    if v not in lang_data.keys():
                        print(
                            '\033[33m[WARN] Corrupted key-value pair in file %s: {"%s": "%s"}\033[0m' % (file_name, k, v))
                        warning_counter += 1
                        pass
                    else:
                        legacy_lang_data.update({k: lang_data[v]})
        # build with mod content
        if args["include"]:
            legacy_lang_data.update(moddata)
        legacy_lang_file = ""
        for k, v in legacy_lang_data.items():
            legacy_lang_file += "%s=%s\n" % (k, v)
        pack.writestr("assets/minecraft/lang/" + lang_name +
                      lang_extension, legacy_lang_file)
        if args['debug']:
            with open(lang_name + lang_extension, 'w') as debug_file:
                debug_file.write(legacy_lang_file)
        # change pack format
        metadata['pack'].update({"pack_format": 3})
    pack.writestr("pack.mcmeta", json.dumps(
        metadata, indent=4, ensure_ascii=False))
    pack.close()
    print("[INFO] Built pack %s with %d warning(s)" %
          (pack_name, warning_counter))
    if warning_counter == 0:
        successful_pack_counter += 1
    else:
        warning_pack_counter += 1
    pack_counter += 1


def build_all():
    build({'type': 'normal', 'figure': 'all',
           'legacy': False, 'include': ['all'], 'debug': False, 'sfw': False})
    build({'type': 'normal', 'figure': 'none',
           'legacy': False, 'include': ['all'], 'debug': False, 'sfw': False})
    build({'type': 'compat', 'figure': 'all',
           'legacy': False, 'include': [], 'debug': False, 'sfw': False})
    build({'type': 'compat', 'figure': 'none',
           'legacy': False, 'include': [], 'debug': False, 'sfw': False})
    build({'type': 'compat', 'figure': 'none',
           'legacy': True, 'include': [], 'debug': False, 'sfw': False})


def get_packname(args):
    base_name = "mcwzh-meme"
    if args['type'] == 'normal':
        if not args['include']:
            base_name += "_nomod"
    elif args['type'] == 'compat':
        base_name += "_compatible"
    if args['figure'] == 'none':
        base_name += "_nofigure"
    if args['legacy']:
        base_name += '_legacy'
    if 'optional/sfw.json' in args['include']:
        base_name += '_sfw'
    return base_name + ".zip"


if __name__ == '__main__':
    main()
