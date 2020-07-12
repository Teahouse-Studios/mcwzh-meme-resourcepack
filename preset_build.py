import build
import os


def main():
    preset_args = [
        {'type': 'normal', 'language': [], 'resource': [
            'all'], 'mod': ['all'], 'sfw': True, 'hash': False},
        {'type': 'normal', 'language': [], 'resource': [
            'all'], 'mod': [], 'sfw': True, 'hash': False},
        {'type': 'normal', 'language': [], 'resource': [
        ], 'mod': [], 'sfw': True, 'hash': False},
        {'type': 'compat', 'language': [], 'resource': [
            'all'], 'mod': ['all'], 'sfw': True, 'hash': False},
        {'type': 'compat', 'language': [], 'resource': [
            'all'], 'mod': [], 'sfw': True, 'hash': False},
        {'type': 'compat', 'language': [], 'resource': [
        ], 'mod': [], 'sfw': True, 'hash': False},
        {'type': 'legacy', 'language': ['attributes', 'old_strings', 'diamond_hoe'], 'resource': [
        ], 'mod': [], 'sfw': True, 'hash': False},
        {'type': 'normal', 'language': [], 'resource': [
            'all'], 'mod': ['all'], 'sfw': False, 'hash': False},
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
    pack_builder = build.builder()
    pack_counter = 0
    perfect_pack_counter = 0
    for item, name in zip(preset_args, preset_name):
        pack_builder.set_args(item)
        pack_builder.build()
        pack_counter += 1
        if pack_builder.get_warning_count() == 0:
            perfect_pack_counter += 1
        if name != "mcwzh-meme.zip":
            if os.path.exists("builds/" + name):
                os.remove("builds/" + name)
            os.rename("builds/mcwzh-meme.zip", "builds/" + name)
        print(f"Renamed pack to {name}.")
    print(
        f"Built {pack_counter} packs with {perfect_pack_counter} pack(s) no warning.")


if __name__ == "__main__":
    main()
