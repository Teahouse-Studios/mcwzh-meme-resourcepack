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
    print("[INFO] Built " + str(pack_counter) + " pack(s), with " + str(successful_pack_counter) + " pack(s) no warning")

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
    if args['type'] == 'normal':
        if not args['legacy']:
            # normal build
            pack.writestr("assets/minecraft/lang/zh_meme.json", json.dumps(lang_data, indent=4, ensure_ascii=True))
        else:
            # legacy build
            legacy_lang_data = lang_data
            for file in mappings:
                file_name = file + ".json"
                if file_name not in os.listdir("mappings"):
                    print("[WARN] Missing mapping: " + file_name + ", Skipping")
                    warning_counter += 1
                    pass
                else:
                    location = "mappings/" + file_name
                    with open(location, encoding='utf8') as f:
                        mapping = json.load(f)
                    for k,v in mapping.items():
                        legacy_lang_data.update({k:legacy_lang_data.pop(v)})
            legacy_lang_file = ""
            for k, v in legacy_lang_data.items():
                legacy_lang_file += "%s=%s\n" %(k,v)
            pack.writestr("assets/minecraft/lang/zh_meme.json", legacy_lang_file)
        pack.write("pack.mcmeta")
    elif args['type'] == 'compat':
        if not args['legacy']:
            # compatible build
            pack.writestr("assets/minecraft/lang/zh_cn.json", json.dumps(lang_data, indent=4, ensure_ascii=True))
        else:
            # legacy build
            legacy_lang_data = {}
            for file in mappings:
                file_name = file + ".json"
                if file_name not in os.listdir("mappings"):
                    print("[WARN] Missing mapping: " + file_name + ", Skipping")
                    warning_counter += 1
                    pass
                else:
                    location = "mappings/" + file_name
                    with open(location, encoding='utf8') as f:
                        mapping = json.load(f)
                    for k,v in mapping.items():
                        if (k not in mapping.keys()) or (v not in lang_data.keys()):
                            print("[WARN] " + "Corrupted key-value pair in file " + file_name + ": " + "{\"" + k + "\": \"" + v + "\"}" )
                            warning_counter += 1
                            pass
                        else:
                            legacy_lang_data.update({k:lang_data[v]})
            legacy_lang_file = ""
            for k, v in legacy_lang_data.items():
                legacy_lang_file += "%s=%s\n" %(k,v)
            pack.writestr("assets/minecraft/lang/zh_cn.json", legacy_lang_file)
        # Processing mcmeta
        with open("pack.mcmeta", 'r', encoding='utf8') as meta:
            metadata = json.load(meta)
        del metadata['language']
        pack.writestr("pack.mcmeta", json.dumps(metadata, indent=4, ensure_ascii=False))
    pack.close()
    print("[INFO] Built pack " + pack_name + " with " + str(warning_counter) + " warning(s)")
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
