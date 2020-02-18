import zipfile
import json
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Automatically build resourcepacks")
    parser.add_argument('type', default='normal',help="Build type. This should be 'all', 'normal' or 'compat'.", choices=['all', 'normal', 'compat'])
    parser.add_argument('-n', '--without-figure', action='store_true', help="Do not add figures when building resource packs. If build type is 'all', this argument will be ignored.")
    args = vars(parser.parse_args())
    if args['type'] == 'all':
        build_all()
    else:
        build(args)
    print("Build succeeded!")

def build(args):
    with open("assets/minecraft/lang/zh_meme.json", 'r', encoding='utf8') as f:
        lang_data = json.load(f)
    pack_name = get_packname(args)
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
        # normal build
        pack.writestr("assets/minecraft/lang/zh_meme.json", json.dumps(lang_data, indent=4, ensure_ascii=True))
        pack.write("pack.mcmeta")
    elif args['type'] == 'compat':
        # compatible build
        pack.writestr("assets/minecraft/lang/zh_cn.json", json.dumps(lang_data, indent=4, ensure_ascii=True))
        # Processing mcmeta
        with open("pack.mcmeta", 'r', encoding='utf8') as meta:
            metadata = json.load(meta)
        del metadata['language']
        pack.writestr("pack.mcmeta", json.dumps(metadata, indent=4, ensure_ascii=False))
    pack.close()

def build_all():
    build({'type': 'normal', 'without_figure': False})
    build({'type': 'normal', 'without_figure': True})
    build({'type': 'compat', 'without_figure': False})
    build({'type': 'compat', 'without_figure': True})

def get_packname(args):
    base_name = "mcwzh-meme"
    if args['type'] == 'normal':
        if args['without_figure']:
            base_name = base_name + "_nofigure"
    elif args['type'] == 'compat':
        base_name = base_name + "_compatible"
        if args['without_figure']:
            base_name = base_name + "_nofigure"
    return base_name + ".zip"

if __name__ == '__main__':
    main()