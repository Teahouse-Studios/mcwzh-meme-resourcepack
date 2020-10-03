import build
import os


if __name__ == '__main__':
    preset_args = [
        {'type': 'normal', 'language': [], 'resource': [
            'all'], 'mod': ['all'], 'sfw': True, 'hash': False, 'output': 'builds'},
        {'type': 'normal', 'language': [], 'resource': [
            'all'], 'mod': [], 'sfw': True, 'hash': False, 'output': 'builds'},
        {'type': 'normal', 'language': [], 'resource': [
        ], 'mod': [], 'sfw': True, 'hash': False, 'output': 'builds'},
        {'type': 'compat', 'language': [], 'resource': [
            'all'], 'mod': ['all'], 'sfw': True, 'hash': False, 'output': 'builds'},
        {'type': 'compat', 'language': [], 'resource': [
            'all'], 'mod': [], 'sfw': True, 'hash': False, 'output': 'builds'},
        {'type': 'compat', 'language': [], 'resource': [
        ], 'mod': [], 'sfw': True, 'hash': False, 'output': 'builds'},
        {'type': 'legacy', 'language': ['attributes', 'old_strings', 'diamond_hoe'], 'resource': [
        ], 'mod': [], 'sfw': True, 'hash': False, 'output': 'builds'},
        {'type': 'normal', 'language': [], 'resource': [
            'all'], 'mod': ['all'], 'sfw': False, 'hash': False, 'output': 'builds'},
    ]
    preset_name = [
        "mcwzh-meme_sfw.zip",
        "mcwzh-meme_nomod_sfw.zip",
        "mcwzh-meme_nomod_noresource_sfw.zip",
        "mcwzh-meme_compatible_sfw.zip",
        "mcwzh-meme_compatible_nomod_sfw.zip",
        "mcwzh-meme_compatible_nomod_noresource_sfw.zip",
        "mcwzh-meme_legacy_noresource_sfw.zip",
        "mcwzh-meme.zip"
    ]
    pack_counter = 0
    perfect_pack_counter = 0
    base_folder = "builds"
    if os.path.exists(base_folder) and not os.path.isdir(base_folder):
        os.remove(base_folder)
    if not os.path.exists(base_folder):
        os.mkdir(base_folder)
    for file in os.listdir(base_folder):
        os.remove(os.path.join(base_folder, file))
    for args, name in zip(preset_args, preset_name):
        info, warning_count, error_count = build.build(args)
        if error_count == 0:
            pack_counter += 1
            if warning_count == 0:
                perfect_pack_counter += 1
            if name != "mcwzh-meme.zip":
                os.rename("builds/mcwzh-meme.zip",
                          os.path.join(base_folder, name))
                print(f"Renamed pack to {name}.")
        else:
            print(f"Failed to build pack {name}.")
    print(
        f"Built {pack_counter} packs with {perfect_pack_counter} pack(s) no warning.")
