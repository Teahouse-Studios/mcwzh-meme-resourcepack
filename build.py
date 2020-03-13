import zipfile
import json
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Automatically build resourcepacks")
    parser.add_argument('type', default='normal',help="Build type. This should be 'all', 'normal' or 'compat'.", choices=['all', 'normal', 'compat'])
    parser.add_argument('-n', '--without-figure', action='store_true', help="Do not add figures when building resource packs. If build type is 'all', this argument will be ignored.")
    parser.add_argument('-l', '--legacy', action='store_true', help="(Not implemented) Use legacy format (.lang) when building resource packs. If build type is 'all', this argument will be ignored.")
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
        # if not args['legacy']:
            # normal build
            # pack.writestr("assets/minecraft/lang/zh_meme.json", json.dumps(lang_data, indent=4, ensure_ascii=True))
            # pack.write("pack.mcmeta")
        # else
            # legacy build
            # legacy_lang_data = ""
            # for k, v in lang_data.items():
            #     legacy_lang_data += "%s=%s\n" %(key,val)
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
    build({'type': 'normal', 'without_figure': False, 'legacy': False})
    build({'type': 'normal', 'without_figure': True, 'legacy': False})
    build({'type': 'compat', 'without_figure': False, 'legacy': False})
    build({'type': 'compat', 'without_figure': True, 'legacy': False})
#    build({'type': 'normal', 'without_figure': False, 'legacy': True})
#    build({'type': 'normal', 'without_figure': True, 'legacy': True})
#    build({'type': 'compat', 'without_figure': False, 'legacy': True})
#    build({'type': 'compat', 'without_figure': True, 'legacy': True})

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