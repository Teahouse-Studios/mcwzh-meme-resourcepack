import zipfile
import sys
import json

def build_pack(type='normal'):
    with open("assets/minecraft/lang/zh_meme.json", 'r', encoding='utf8') as f:
        lang_data = json.load(f)
    if type == 'normal':
        # Normal build
        zipped_pack = zipfile.ZipFile("mcwzh-meme.zip", 'w')
        zipped_pack.writestr("assets/minecraft/lang/zh_meme.json", json.dumps(lang_data, indent=4, ensure_ascii=True))
        zipped_pack.write("pack.mcmeta")
    elif type == 'compat':
        # Compatible build
        zipped_pack = zipfile.ZipFile("mcwzh-meme_compatible.zip", 'w')
        zipped_pack.writestr("assets/minecraft/lang/zh_cn.json", json.dumps(lang_data, indent=4, ensure_ascii=True))
        # Processing mcmeta
        with open("pack.mcmeta", 'r', encoding='utf8') as meta:
            metadata = json.load(meta)
        del metadata['language']
        zipped_pack.writestr("pack.mcmeta", json.dumps(metadata, indent=4, ensure_ascii=False))
    zipped_pack.write("pack.png")
    zipped_pack.close()

if len(sys.argv) > 1:
    if sys.argv[1] == "compat":
        build_pack("compat")
    elif sys.argv[1] == "all":
        build_pack()
        build_pack("compat")
    elif sys.argv[1] == "normal":
        build_pack()
else:
    print("Needs 1 argument")
    exit(code=-1)
print("Build succeeded!")
exit(code=0)
