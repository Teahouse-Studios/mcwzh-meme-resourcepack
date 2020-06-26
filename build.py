import zipfile
import json
import argparse
import os
import warnings
import hashlib

# Apache 2.0

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
    parser = generate_parser()
    args = vars(parser.parse_args())
    if args['type'] == 'clean':
        for i in os.listdir('builds/'):
            os.remove('builds/' + i)
        print("\n[INFO] Deleted all packs built.")
    else:
        if args['type'] == 'all':
            build_all()
        else:
            build(args)
        print(
            f"\n[INFO] Built {pack_counter} pack(s) with {successful_pack_counter} pack(s) no warning")


def build(args: dict) -> (str, str):
    global pack_counter
    global successful_pack_counter
    global warning_pack_counter
    warning_counter = 0
    counter = 0
    logs = ""
    info = ""
    # get figure list
    (figlist, counter, info) = get_figure_list(args['figure'])
    warning_counter += counter
    logs += info
    counter = 0
    info = ""
    # get mod list
    (modlist, counter, info) = get_mod_list(args['include'])
    warning_counter += counter
    logs += info
    counter = 0
    # suitable for work
    if args['sfw']:
        modlist.add('optional/sfw.json')
    # debug mode
    if not args['debug']:
        warnings.filterwarnings("ignore")
    # load basic strings
    with open("assets/minecraft/lang/zh_meme.json", 'r', encoding='utf8') as f:
        lang_data = json.load(f)
    with open("assets/realms/lang/zh_meme.json", 'r', encoding='utf8') as r:
        realms_data = json.load(r)
    pack_name = "builds/" + get_packname(args)
    info = f"[INFO] Building {pack_name}"
    print(info)
    logs += f"{info}\n"
    # check build path
    if os.path.exists("builds"):
        if not os.path.isdir("builds"):
            os.remove("builds")
            os.mkdir("builds")
    else:
        os.mkdir("builds")
    # all builds have these files
    pack = zipfile.ZipFile(
        pack_name, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=5)
    pack.write("pack.png")
    pack.write("LICENSE")
    # add figures
    if figlist:
        for file in figlist:
            pack.write(file, arcname=file[file.find("assets"):])
    # add mods
    if modlist:
        info = ""
        (mod_content, counter, info) = get_mod_content(modlist)
        logs += info
        lang_data.update(mod_content)
        warning_counter += counter
        counter = 0
    # processing mcmeta
    with open("pack.mcmeta", 'r', encoding='utf8') as meta:
        metadata = json.load(meta)
    if args['type'] == 'normal':
        lang_name = "zh_meme"
    elif args['type'] == 'compat':
        del metadata['language']
        lang_name = "zh_cn"
    if not args['legacy']:
        # normal/compatible build
        lang_extension = ".json"
        pack.writestr("assets/minecraft/lang/" + lang_name + lang_extension,
                      json.dumps(lang_data, indent=4, ensure_ascii=True))
        pack.writestr("assets/realms/lang/" + lang_name + lang_extension,
                      json.dumps(realms_data, indent=4, ensure_ascii=True))
        if args['debug']:
            with open(lang_name + lang_extension, 'w', encoding='utf8') as debug_file:
                debug_file.write(json.dumps(
                    lang_data, indent=4, ensure_ascii=False))
    else:
        # legacy(1.12.2) build
        lang_extension = ".lang"
        # change pack format
        metadata['pack'].update({"pack_format": 3})
        lang_data.update(realms_data)
        info = ""
        (legacy_lang_content, counter, info) = generate_legacy_content(
            lang_data, mappings)
        logs += info
        pack.writestr("assets/minecraft/lang/" + lang_name +
                      lang_extension, legacy_lang_content)
        warning_counter += counter
        counter = 0
        if args['debug']:
            with open(lang_name + lang_extension, 'w', encoding='utf8') as debug_file:
                debug_file.write(legacy_lang_content)
    pack.writestr("pack.mcmeta", json.dumps(
        metadata, indent=4, ensure_ascii=False))
    pack.close()
    # add hash to pack name
    if args['hash']:
        sha256 = hashlib.sha256(json.dumps(args).encode('utf8')).hexdigest()
        new_name = pack_name[:pack_name.find(
            ".zip")] + "." + sha256[:7] + ".zip"
        if os.path.exists(new_name):
            os.remove(new_name)
        os.rename(pack_name, new_name)
        pack_name = new_name
    info = f"[INFO] Built pack {pack_name} with {warning_counter} warning(s)"
    print(info)
    logs += f"{info}\n"
    if warning_counter == 0:
        successful_pack_counter += 1
    else:
        warning_pack_counter += 1
    pack_counter += 1
    return pack_name, logs


def build_all() -> None:
    build({'type': 'normal', 'figure': ['all'], 'legacy': False, 'include': [
          'all'], 'debug': False, 'sfw': False, 'hash': False})
    build({'type': 'normal', 'figure': ['all'], 'legacy': False, 'include': [
          'all'], 'debug': False, 'sfw': True, 'hash': False})
    build({'type': 'normal', 'figure': [], 'legacy': False, 'include': [
          'all'], 'debug': False, 'sfw': True, 'hash': False})
    build({'type': 'compat', 'figure': ['all'], 'legacy': False, 'include': [
          'all'], 'debug': False, 'sfw': True, 'hash': False})
    build({'type': 'compat', 'figure': [], 'legacy': False, 'include': [
          'all'], 'debug': False, 'sfw': True, 'hash': False})
    build({'type': 'compat', 'figure': [], 'legacy': False,
           'include': [], 'debug': False, 'sfw': True, 'hash': False})
    build({'type': 'compat', 'figure': [], 'legacy': True, 'include': [
          'all'], 'debug': False, 'sfw': True, 'hash': False})


def get_packname(args: dict) -> str:
    base_name = "mcwzh-meme"
    if args['type'] == 'normal':
        pass
    elif args['type'] == 'compat':
        base_name += "_compatible"
    if not args['figure']:
        base_name += "_nofigure"
    elif 'none' in args['figure']:
        base_name += "_nofigure"
    if not args['include']:
        base_name += "_nomod"
    elif 'none' in args['include']:
        base_name += "_nomod"
    if args['legacy']:
        base_name += '_legacy'
    if args['sfw']:
        base_name += '_sfw'
    return base_name + ".zip"


def generate_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Automatically build resourcepacks")
    parser.add_argument('type', default='normal', help="Build type. Should be 'all', 'normal', 'compat' or 'clean'. If it's 'all', all other arguments will be ignored. If it's 'clean', all packs in 'builds/' directory will be deleted.",
                        choices=['all', 'normal', 'compat', 'clean'])
    parser.add_argument('-t', '--figure', nargs='*', default='all',
                        help="Specify which figures should be added. Should be path(s) to a file, folder, 'all' or 'none'. Defaults to 'all'.")
    parser.add_argument('-s', '--sfw', action='store_true',
                        help="Use 'suitable for work' strings.")
    parser.add_argument('-l', '--legacy', action='store_true',
                        help="(Experimental) Use legacy format (.lang) when building resource packs.")
    parser.add_argument('-i', '--include', nargs='*', default='all',
                        help="(Experimental) Include modification strings or folders. Should be path(s) to a file, folder, 'all' or 'none'. Defaults to 'all'.")
    parser.add_argument('-d', '--debug', action='store_true',
                        help="Output an individual language file.")
    parser.add_argument('--hash', action='store_true',
                        help="Add a hash in the name of the pack.")
    return parser


def get_figure_list(figlist: list) -> (set, int, str):
    figure_list = set()
    pack_pos = set()
    warning = 0
    log = ""
    if figlist:
        if 'none' in figlist:
            # no figures added
            pass
        elif 'all' in figlist:
            # all figures added
            for root, dirs, files in os.walk('optional'):
                if root == 'optional':
                    files.clear()
                for name in files:
                    # prevent duplicates
                    file_pos = os.path.join(root, name)
                    num = len(pack_pos)
                    pack_pos.add(file_pos[file_pos.find("assets"):])
                    if num != len(pack_pos):
                        figure_list.add(file_pos)
        else:
            for path in figlist:
                if os.path.exists(path):
                    if os.path.isfile(path):
                        figure_list.add(path)
                    elif os.path.isdir(path):
                        for root, dirs, files in os.walk(path):
                            figure_list.update(
                                os.path.join(root, name) for name in files)
                else:
                    warn = f'[WARN] "{path}" does not exist, skipping'
                    print(f"\033[33m{warn}\033[0m")
                    log += f"{warn}\n"
                    warning += 1
    return figure_list, warning, log


def get_mod_list(modlist: list) -> (set, int, str):
    mods = set()
    warning = 0
    log = ""
    if modlist:
        if 'none' in modlist:
            # no mods added
            pass
        elif 'all' in modlist:
            # all mods added
            mods.update("mods/" + file for file in os.listdir('mods'))
        else:
            for path in modlist:
                if os.path.exists(path):
                    if os.path.isfile(path):
                        mods.add(path)
                    elif os.path.isdir(path):
                        for root, dirs, files in os.walk(path):
                            mods.update(
                                os.path.join(root, name) for name in files)
                else:
                    warn = f'[WARN] "{path}" does not exist, skipping'
                    print(f"\033[33m{warn}\033[0m")
                    log += f"{warn}\n"
                    warning += 1
    return mods, warning, log


def get_mod_content(modlist: list) -> (dict, int, str):
    mods = {}
    counter = 0
    log = ""
    for file in modlist:
        if file.endswith(".json"):
            with open(file, 'r', encoding='utf8') as f:
                mods.update(json.load(f))
        elif file.endswith(".lang"):
            with open(file, 'r', encoding='utf8') as f:
                items = [i for i in f.read().splitlines() if (
                    i != '' and not i.startswith('#'))]
            mods.update(dict(i.split("=", 1) for i in items))
        else:
            warn = f'[WARN] File type "{file[file.rfind(".") + 1:]}" is not supported, skipping'
            print(f"\033[33m{warn}\033[0m")
            counter += 1
            log += f"{warn}\n"
    return mods, counter, log


def generate_legacy_content(lang_data: dict, mapping_list: list) -> (str, int, str):
    counter = 0
    legacy_lang_data = {}
    log = ""
    for item in mapping_list:
        mapping_file = item + ".json"
        if mapping_file not in os.listdir("mappings"):
            warn = f'[WARN] Missing mapping "{mapping_file}", skipping'
            print(f'\033[33m{warn}\033[0m')
            log += f"{warn}\n"
            counter += 1
        else:
            path = "mappings/" + mapping_file
            with open(path, 'r', encoding='utf8') as f:
                mapping = json.load(f)
            for k, v in mapping.items():
                if v not in lang_data.keys():
                    warn = f'[WARN] Corrupted key-value pair in file {mapping_file}: {{"{k}": "{v}"}}'
                    print(f'\033[33m{warn}\033[0m')
                    log += f"{warn}\n"
                    counter += 1
                else:
                    legacy_lang_data.update({k: lang_data[v]})
    legacy_lang_content = ""
    for k, v in legacy_lang_data.items():
        legacy_lang_content += f"{k}={v}\n"
    return legacy_lang_content, counter, log


if __name__ == '__main__':
    main()
