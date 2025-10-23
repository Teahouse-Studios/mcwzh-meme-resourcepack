import json
import argparse
from typing import Dict
from os import path
import requests



MEME_JSON_PATH = path.join(
    path.dirname(__file__),
    *'../../modules/meme_resourcepack/assets/minecraft/lang/zh_meme.json'.split('/')
)
VERSION_MANIFEST_URL = 'https://piston-meta.mojang.com/mc/game/version_manifest_v2.json'
OUTPUT_PENDING = path.join(path.dirname(__file__), 'pending.json')
OUTPUT_FILTERS = path.join(path.dirname(__file__), 'filters.json')



def whats_new(legacy: Dict[str, str], new_unlocalized: Dict[str, str]) -> Dict[str, str]:
    new_unlocalized = dict(new_unlocalized) # edit on its copy
    for existing_key in legacy:
        if existing_key in new_unlocalized: # keys in `legacy` can be absent in `new_unlocalized` due to compatibility consideration
            del new_unlocalized[existing_key]
    return new_unlocalized


def load_chinese_translations(version: str | None):
    manifest = requests.get(VERSION_MANIFEST_URL).json()

    # 查找版本元数据
    if version:
        version_meta_url = next((v['url'] for v in manifest['versions'] if v['id'] == version), None)
    else:
        version_meta_url = manifest['versions'][0]['url']
    if not version_meta_url:
        raise Exception(f"Version not found: {version}")

    version_meta = requests.get(version_meta_url).json()
    asset_index_url = version_meta['assetIndex']['url']
    asset_index = requests.get(asset_index_url).json()
    zh_cn_hash = asset_index['objects']['minecraft/lang/zh_cn.json']['hash']
    zh_cn_url = f"https://resources.download.minecraft.net/{zh_cn_hash[:2]}/{zh_cn_hash}"
    return requests.get(zh_cn_url).json()


def gen_diff(version: str):
    with open(MEME_JSON_PATH, encoding='utf8') as f:
        old_meme = json.load(f)
    new_cn = load_chinese_translations(version if version != 'latest' else None)
    diff = whats_new(old_meme, new_cn)
    with open(OUTPUT_PENDING, 'w', encoding='utf8') as f:
        json.dump(diff, f, indent=4, ensure_ascii=False, sort_keys=True)


def init_filters():
    filters = {}
    if path.exists(OUTPUT_FILTERS):
        with open(OUTPUT_FILTERS, encoding='utf8') as f:
            filters = json.load(f)
    for key in ('sfc', 'sfw'):
        if key not in filters:
            filters[key] = {}

    with open(OUTPUT_FILTERS, 'w', encoding='utf8') as f:
        json.dump(filters, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Generate diff from current zh_meme.json to target version')
    parser.add_argument('version', type=str, help='Target version id or "latest"')
    args = parser.parse_args()

    print('Generating diff...')
    gen_diff(args.version)
    print(f"Check out diff at {OUTPUT_PENDING}")

    init_filters()
    print(f'\nAlso check out filters at {OUTPUT_FILTERS}\n'
          'If suitable-for-children or suitable-for-work mappings need to be set, '
          'add "BEFORE": "AFTER" to the respective object.')

if __name__ == '__main__':
    main()
