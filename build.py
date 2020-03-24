import zipfile
import json
import argparse
import os

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
    parser = argparse.ArgumentParser(description="Automatically build resourcepacks")
    parser.add_argument('type', default='normal',help="Build type. This should be 'all', 'normal' or 'compat'.", choices=['all', 'normal', 'compat'])
    parser.add_argument('-n', '--without-figure', action='store_true', help="Do not add figures when building resource packs. If build type is 'all', this argument will be ignored.")
    parser.add_argument('-l', '--legacy', action='store_true', help="(Not fully implemented) Use legacy format (.lang) when building resource packs. If build type is 'all', this argument will be ignored.")
    args = vars(parser.parse_args())
    if args['type'] == 'all':
        build_all()
    else:
        build(args)
    print("\n[INFO] Built %d pack(s) with %d pack(s) no warning" % (pack_counter, successful_pack_counter))

def build(args):
    global pack_counter
    global successful_pack_counter
    global warning_pack_counter
    with open("assets/minecraft/lang/zh_meme.json", 'r', encoding='utf8') as f:
        lang_data = json.load(f)
    pack_name = get_packname(args)
    print("[INFO] Building " + pack_name)
    warning_counter = 0
    # all builds have these files
    pack = zipfile.ZipFile(pack_name, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=5)
    pack.write("pack.png")
    pack.write("LICENSE")
    # build with figures
    if not args['without_figure']:
        for file in os.listdir("assets/minecraft/models/item"):
            pack.write("assets/minecraft/models/item/" + file)
        for file in os.listdir("assets/minecraft/textures/entity"):
            pack.write("assets/minecraft/textures/entity/" + file)
        for file in os.listdir("assets/minecraft/textures/block"):
            pack.write("assets/minecraft/textures/block/" + file)   
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
        pack.writestr("assets/minecraft/lang/" + lang_name + lang_extension, json.dumps(lang_data, indent=4, ensure_ascii=True))
    else:
        # legacy build
        lang_extension = ".lang"
        legacy_lang_data = {}
        for file in mappings:
            file_name = file + ".json"
            if file_name not in os.listdir("mappings"):
                print("\033[33m[WARN] Missing mapping: %s, skipping\033[0m" % (file_name))
                warning_counter += 1
                pass
            else:
                location = "mappings/" + file_name
                with open(location, encoding='utf8') as f:
                    mapping = json.load(f)
                for k, v in mapping.items():
                    if v not in lang_data.keys():
                        print('\033[33m[WARN] Corrupted key-value pair in file %s: {"%s": "%s"}\033[0m' % (file_name, k, v))
                        warning_counter += 1
                        pass
                    else:
                        legacy_lang_data.update({k:lang_data[v]})
        legacy_lang_file = ""
        for k, v in legacy_lang_data.items():
            legacy_lang_file += "%s=%s\n" % (k, v)
        pack.writestr("assets/minecraft/lang/" + lang_name + lang_extension, legacy_lang_file)
        # change pack format
        metadata['pack'].update({"pack_format": 3})
    pack.writestr("pack.mcmeta", json.dumps(metadata, indent=4, ensure_ascii=False))
    pack.close()
    print("[INFO] Built pack %s with %d warning(s)" % (pack_name, warning_counter))
    if warning_counter == 0:
        successful_pack_counter += 1
    else:
        warning_pack_counter += 1
    pack_counter += 1

def build_all():
    build({'type': 'normal', 'without_figure': False, 'legacy': False})
    build({'type': 'normal', 'without_figure': True, 'legacy': False})
    build({'type': 'compat', 'without_figure': False, 'legacy': False})
    build({'type': 'compat', 'without_figure': True, 'legacy': False})
#    build({'type': 'normal', 'without_figure': False, 'legacy': True})
#    build({'type': 'normal', 'without_figure': True, 'legacy': True})
#    build({'type': 'compat', 'without_figure': False, 'legacy': True})
    build({'type': 'compat', 'without_figure': True, 'legacy': True})

def get_packname(args):
    base_name = "mcwzh-meme"
    if args['type'] == 'normal':
        pass
    elif args['type'] == 'compat':
        base_name = base_name + "_compatible"
    if args['without_figure']:
        base_name = base_name + "_nofigure"
    if args['legacy']:
        base_name = base_name + '_legacy'
    return base_name + ".zip"

if __name__ == '__main__':
    main()
