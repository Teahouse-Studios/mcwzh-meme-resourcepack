if __name__ == '__main__':
    import build
    from json import load
    from os import listdir, mkdir, remove, rename
    from os.path import exists, isdir, join
    from sys import exit

    pack_version = '1.0.5'
    build_unsuccessful = 0

    def check_version_consistency():
        mcmeta_desc = (load(open("meme_resourcepack/pack.mcmeta",
                                 'r', encoding='utf8')))['pack']['description']
        return pack_version in mcmeta_desc

    if check_version_consistency():
        preset_args = [
            {'type': 'normal', 'modules': {'language': ['all'], 'resource': [
                'all'], 'mixed': []}, 'mod': [], 'hash': False, 'output': 'builds', 'format': 6},
            {'type': 'normal', 'modules': {'language': ['sfw'], 'resource': ['all'], 'mixed': [
            ]}, 'mod': ['all'], 'hash': False, 'output': 'builds', 'format': 6},
            {'type': 'normal', 'modules': {'language': ['sfw'], 'resource': [
                'all'], 'mixed': []}, 'mod': [],  'hash': False, 'output': 'builds', 'format': 6},
            {'type': 'normal', 'modules': {'language': ['sfw'], 'resource': [
            ], 'mixed': []}, 'mod': [], 'hash': False, 'output': 'builds', 'format': 6},
            {'type': 'compat', 'modules': {'language': ['sfw'], 'resource': [
                'all'], 'mixed': []}, 'mod': ['all'], 'hash': False, 'output': 'builds', 'format': 6},
            {'type': 'compat', 'modules': {'language': ['sfw'], 'resource': [
                'all'], 'mixed': []}, 'mod': [], 'hash': False, 'output': 'builds', 'format': 6},
            {'type': 'compat', 'modules': {'language': ['sfw'], 'resource': [], 'mixed': [
            ]}, 'mod': [], 'hash': False, 'output': 'builds', 'format': 6},
            {'type': 'legacy', 'modules': {'language': ['sfw', 'attributes', 'old_strings', 'diamond_hoe', 'extra_strings', 'multiplayer_version'], 'resource': [
            ], 'mixed': []}, 'mod': [], 'hash': False, 'output': 'builds', 'format': 3}
        ]
        preset_name = [
            f"mcwzh-meme_v{pack_version}.zip",
            f"mcwzh-meme_sfw_v{pack_version}.zip",
            f"mcwzh-meme_nomod_sfw_v{pack_version}.zip",
            f"mcwzh-meme_nomod_noresource_sfw_v{pack_version}.zip",
            f"mcwzh-meme_compatible_sfw_v{pack_version}.zip",
            f"mcwzh-meme_compatible_nomod_sfw_v{pack_version}.zip",
            f"mcwzh-meme_compatible_nomod_noresource_sfw_v{pack_version}.zip",
            f"mcwzh-meme_legacy_nomod_noresource_sfw_v{pack_version}.zip"
        ]
        pack_counter = 0
        perfect_pack_counter = 0
        base_folder = "builds"
        if exists(base_folder) and not isdir(base_folder):
            remove(base_folder)
        if not exists(base_folder):
            mkdir(base_folder)
        for file in listdir(base_folder):
            remove(join(base_folder, file))
        for args, name in zip(preset_args, preset_name):
            pack_name, warning_count, error, _ = build.build(args)
            if not error:
                pack_counter += 1
                if warning_count == 0:
                    perfect_pack_counter += 1
                if name != pack_name:
                    rename(join(base_folder, pack_name),
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
            f'\033[1;31mError: Pack version "{pack_version}" does not match the number in pack.mcmeta.\033[0m')
