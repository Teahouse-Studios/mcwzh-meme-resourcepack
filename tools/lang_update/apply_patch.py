import json
from typing import Dict, Any
from os import path

MEME_JSON_PATH = path.join(
    path.dirname(__file__),
    *'../../modules/meme_resourcepack/assets/minecraft/lang/zh_meme.json'.split('/')
)
SFC_JSON_PATH = path.join(
    path.dirname(__file__),
    *'../../modules/lang_sfc/add.json'.split('/')
)
SFW_JSON_PATH = path.join(
    path.dirname(__file__),
    *'../../modules/lang_sfw/add.json'.split('/')
)
INPUT_PENDING = path.join(path.dirname(__file__), 'pending.json')
INPUT_FILTERS = path.join(path.dirname(__file__), 'filters.json')


def read_json(fn: str) -> dict:
    with open(fn, encoding='utf8') as f:
        return json.load(f)


def write_json(fn: str, obj: Any):
    with open(fn, 'w', encoding='utf8') as f:
        # zh_meme uses an indent of 4
        json.dump(obj, f, ensure_ascii=False, indent=4, sort_keys=True)


def merge_json(*json_files: Dict[str, str]) -> Dict[str, str]:
    ret = {}
    for data in json_files:
        ret.update(data)
    return ret


def map_with_filter(src: Dict[str, str], mapping: Dict[str, str]) -> Dict[str, str]:
    dest = {}
    for key, value in src.items():
        for keyword, replaced_keyword in mapping.items():
            if keyword in value:
                dest[key] = value = value.replace(keyword, replaced_keyword)
    return dest


def main():
    print('1. Applying main patch')
    pending_patch = read_json(INPUT_PENDING)
    write_json(MEME_JSON_PATH, merge_json(read_json(MEME_JSON_PATH), pending_patch))

    print('2. Checking filters')
    filters = read_json(INPUT_FILTERS)
    for key, target_filename in (('sfc', SFC_JSON_PATH), ('sfw', SFW_JSON_PATH)):
        mapped = map_with_filter(pending_patch, filters[key])
        if mapped:
            print(f'Found {len(mapped)} matching {key} items. Applying...')
            write_json(target_filename, merge_json(read_json(target_filename), mapped))
        else:
            print(f'No matching {key} items found.')


if __name__ == '__main__':
    main()
