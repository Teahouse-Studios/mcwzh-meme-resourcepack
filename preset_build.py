from json import load
from os import listdir, mkdir, remove, rename
from os.path import exists, isdir, join
from sys import exit
from memepack_builder.wrapper import main as _main

PACK_VERSION = '1.3.0'


def check_version_consistency():
    mcmeta_desc = (load(open("meme_resourcepack/pack.mcmeta",
                             'r', encoding='utf8')))['pack']['description']
    return PACK_VERSION in mcmeta_desc


def main():
    if check_version_consistency():
        preset_args = [
            {'platform': 'je', 'type': 'normal', 'modules': {'resource': [], 'collection': [
                'version_1.16.5', 'choice_modules_1']}, 'mod': [], 'hash': False, 'output': 'builds', 'format': 6},
            {'platform': 'je', 'type': 'normal', 'modules': {'resource': ['lang_sfw'], 'collection': [
                'version_1.16.5', 'choice_modules_1']}, 'mod': ['all'], 'hash': False, 'output': 'builds', 'format': 6},
            {'platform': 'je', 'type': 'normal', 'modules': {'resource': ['lang_sfw'], 'collection': [
                'version_1.16.5']}, 'mod': [],  'hash': False, 'output': 'builds', 'format': 6},
            {'platform': 'je', 'type': 'normal', 'modules': {'resource': ['lang_sfw'], 'collection': [
                'version_1.16.5']}, 'mod': [], 'hash': False, 'output': 'builds', 'format': 6},
            {'platform': 'je', 'type': 'compat', 'modules': {'resource': ['lang_sfw'], 'collection': [
                'version_1.16.5', 'choice_modules_1']}, 'mod': ['all'], 'hash': False, 'output': 'builds', 'format': 6},
            {'platform': 'je', 'type': 'compat', 'modules': {'resource': ['lang_sfw'], 'collection': [
                'version_1.16.5', 'choice_modules_1']}, 'mod': [], 'hash': False, 'output': 'builds', 'format': 6},
            {'platform': 'je', 'type': 'compat', 'modules': {'resource': ['lang_sfw'], 'collection': [
                'version_1.16.5']}, 'mod': [], 'hash': False, 'output': 'builds', 'format': 6},
            {'platform': 'je', 'type': 'legacy', 'modules': {'resource': ['lang_sfw'], 'collection': [
                'version_1.12.2-1.15.2']}, 'mod': [], 'hash': False, 'output': 'builds', 'format': 3}
        ]
        preset_name = [
            f"mcwzh-meme_v{PACK_VERSION}.zip",
            f"mcwzh-meme_sfw_v{PACK_VERSION}.zip",
            f"mcwzh-meme_nomod_sfw_v{PACK_VERSION}.zip",
            f"mcwzh-meme_nomod_noresource_sfw_v{PACK_VERSION}.zip",
            f"mcwzh-meme_compatible_sfw_v{PACK_VERSION}.zip",
            f"mcwzh-meme_compatible_nomod_sfw_v{PACK_VERSION}.zip",
            f"mcwzh-meme_compatible_nomod_noresource_sfw_v{PACK_VERSION}.zip",
            f"mcwzh-meme_legacy_nomod_noresource_sfw_v{PACK_VERSION}.zip"
        ]
        pack_counter = 0
        perfect_pack_counter = 0
        base_folder = "builds"
        build_unsuccessful = 0
        if exists(base_folder) and not isdir(base_folder):
            remove(base_folder)
        if not exists(base_folder):
            mkdir(base_folder)
        for file in listdir(base_folder):
            remove(join(base_folder, file))
        for args, name in zip(preset_args, preset_name):
            result = _main(args, True)
            if result['error_code'] == 0:
                pack_counter += 1
                if result['warning_count'] == 0:
                    perfect_pack_counter += 1
                if name != result['file_name']:
                    rename(join(base_folder, result['file_name']),
                           join(base_folder, name))
                    print(f"Renamed pack to {name}.")
            else:
                print(f"Failed to build pack {name}.")
                build_unsuccessful = 1
        print(
            f"Built {pack_counter} packs with {perfect_pack_counter} pack(s) no warning.")
        exit(build_unsuccessful)
    else:
        exit(
            f'\033[1;31mError: Pack version "{PACK_VERSION}" does not match the number in pack.mcmeta.\033[0m')


if __name__ == '__main__':
    main()
