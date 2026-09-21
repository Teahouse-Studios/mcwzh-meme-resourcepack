#!/usr/bin/env python3
'''
Derive credits.json and credits.txt from mod_credits.json and the vanilla credits.

mod_credits.json follows the format of End Poem Extension Mod (https://modrinth.com/mod/end-poem-extension).
This indicates that when EPX is loaded, mod_credits.json is loaded instead, to avoid potential cross-mod conflicts.
'''
import json
import os
import sys
import tempfile
import zipfile

import requests

MODULES_DIR = os.path.join(os.path.dirname(sys.argv[0]), '..', '..', 'modules')
MOD_CREDITS_JSON = os.path.join(MODULES_DIR, 'meme_resourcepack', 'assets', 'minecraft', 'texts', 'mod_credits.json')
CREDITS_JSON_V3 = os.path.join(MODULES_DIR, 'meme_resourcepack', 'assets', 'minecraft', 'texts', 'credits.json')
CREDITS_JSON_V2 = os.path.join(MODULES_DIR, 'text_credits_1.17-1.19.4', 'assets', 'minecraft', 'texts', 'credits.json')
CREDITS_TXT_V1 = os.path.join(MODULES_DIR, 'text_credits_1.12-1.16.5', 'assets', 'minecraft', 'texts', 'credits.txt')

VERSION_MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"


def _assert_is_list(data, name):
    if not isinstance(data, list):
        raise ValueError(f"{name} is not an array, got: {type(data).__name__}")


def _get_client_resource(version: str, resource: str, func, check):
    manifest_resp = requests.get(VERSION_MANIFEST_URL)
    manifest_resp.raise_for_status()
    manifest = manifest_resp.json()
    if version is None:
        target_version = manifest['versions'][0]
    else:
        target_version = next(filter(lambda x: x.get('id') == version, manifest['versions']))

    meta_resp = requests.get(target_version["url"])
    meta_resp.raise_for_status()
    meta = meta_resp.json()
    jar_url = meta["downloads"]["client"]["url"]

    with tempfile.NamedTemporaryFile(suffix=".jar", delete=True) as tmp_file:
        jar_resp = requests.get(jar_url, stream=True)
        jar_resp.raise_for_status()
        for chunk in jar_resp.iter_content(chunk_size=8192):
            tmp_file.write(chunk)
        tmp_file.flush()

        with zipfile.ZipFile(tmp_file.name, "r") as jar:
            with jar.open(resource) as f:
                data = func(f)

    check(data)
    return data


def download_credits(version: str | None = None) -> list:
    return _get_client_resource(
        version, "assets/minecraft/texts/credits.json",
        func=json.load, check=lambda x: _assert_is_list(x, 'credits.json')
    )


def download_credits_txt(version: str) -> str:
    return _get_client_resource(
        version, 'assets/minecraft/texts/credits.txt',
        func=lambda x: x.read().decode('utf-8'), check=lambda _: None
    )


def read_json_list(path: str) -> list:
    with open(path, encoding='utf8') as f:
        data = json.load(f)
    _assert_is_list(data, path)
    return data


def dump_json_or_text(path: str, data: str | dict | list):
    with open(path, 'w', encoding='utf8') as f:
        if isinstance(data, str):
            f.write(data)
        else:
            json.dump(data, f, indent=2, ensure_ascii=False)


def convert_to_text(data_list: list) -> str:
    lines = []
    for section in data_list:
        lines.append("[C]§f============")
        lines.append(f"[C]§e{section['section']}")
        lines.append("[C]§f============")
        
        for title_item in section["titles"]:
            title = title_item["title"]
            names = title_item["names"]
            lines.append(f"§7{title}")
            if not names:
                continue
            for name in names:
                lines.append(f"§f          {name}")
            lines.append('')
            lines.append('')
    
    return "\n".join(lines)


def v3_to_v2(disciplines_v3: list) -> list:
    disciplines_v3 = json.loads(json.dumps(disciplines_v3))
    ret = []
    for discipline in disciplines_v3:
        section_name = discipline['discipline']
        del discipline['discipline']
        ret.append({'section': section_name, **discipline})
    return ret

def main():
    mod_credits = read_json_list(MOD_CREDITS_JSON)
    if len(mod_credits) != 1 or (not isinstance(mod_credits[0], dict)):
        raise ValueError('Invalid mod credits')
    mod_credits_disciplines = mod_credits[0].get('disciplines')
    _assert_is_list(mod_credits_disciplines, 'disciplines')
    mod_credits_disciplines = v3_to_v2(mod_credits_disciplines)
    
    print('Downloading credits from latest, 1.19.4, 1.16.5')
    credits_latest = download_credits()
    credits_v2 = download_credits(version='1.19.4')
    credits_v1 = download_credits_txt(version='1.16.5')
    print('Merging credits')

    merged_credits_v3 = mod_credits + credits_latest
    merged_credits_v2 = mod_credits_disciplines + credits_v2
    merged_credits_v1 = convert_to_text(mod_credits_disciplines) + '\n' + credits_v1

    print('Dumping credits')
    dump_json_or_text(CREDITS_JSON_V3, merged_credits_v3)
    dump_json_or_text(CREDITS_JSON_V2, merged_credits_v2)
    dump_json_or_text(CREDITS_TXT_V1, merged_credits_v1)


if __name__ == '__main__':
    main()
