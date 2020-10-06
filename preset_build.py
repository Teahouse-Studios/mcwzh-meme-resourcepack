import build
import os


if __name__ == '__main__':
    preset_args = [
        {'type': 'normal', 'modules': {'language': ['all'], 'resource': [
            'all'], 'mixed': []}, 'mod': [], 'hash': False, 'output': 'builds', 'format': 6},
        {'type': 'normal', 'modules': {'language': ['sfw'], 'resource': [
            'all'], 'mixed': []}, 'mod': ['all'],  'hash': False, 'output': 'builds', 'format': 6},
        {'type': 'normal', 'modules': {'language': ['sfw'], 'resource': [
            'all'], 'mixed': []}, 'mod': [], 'hash': False, 'output': 'builds', 'format': 6},
        {'type': 'normal', 'modules': {'language': ['sfw'], 'resource': [
        ], 'mixed': []}, 'mod': [], 'hash': False, 'output': 'builds', 'format': 6},
        {'type': 'compat', 'modules': {'language': ['sfw'], 'resource': [
            'all'], 'mixed': []}, 'mod': ['all'], 'hash': False, 'output': 'builds', 'format': 6},
        {'type': 'compat', 'modules': {'language': ['sfw'], 'resource': [
            'all'], 'mixed': []}, 'mod': [], 'hash': False, 'output': 'builds', 'format': 6},
        {'type': 'compat', 'modules': {'language': ['sfw'], 'resource': [
        ], 'mixed': []}, 'mod': [], 'hash': False, 'output': 'builds', 'format': 6},
        {'type': 'legacy', 'modules': {'language': ['sfw', 'attributes', 'old_strings', 'diamond_hoe'], 'resource': [
        ], 'mixed': []}, 'mod': [], 'hash': False, 'output': 'builds', 'format': 3},
        {'type': 'normal', 'modules': {'language': ['sfw'], 'resource': ['all'], 'mixed': [
        ]}, 'mod': ['all'], 'hash': False, 'output': 'builds', 'format': 6},
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
        pack_name, warning_count, error, _ = build.build(args)
        if not error:
            pack_counter += 1
            if warning_count == 0:
                perfect_pack_counter += 1
            if name != pack_name:
                os.rename(os.path.join(base_folder, pack_name),
                          os.path.join(base_folder, name))
                print(f"Renamed pack to {name}.")
        else:
            print(f"Failed to build pack {name}.")
    print(
        f"Built {pack_counter} packs with {perfect_pack_counter} pack(s) no warning.")
