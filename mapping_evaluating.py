import os
import json

legacy_lang_data = {}

with open("1.12.lang", 'r', encoding='utf8') as f:
    items = [i for i in f.read().splitlines() if (i != '' and not i.startswith('#'))]

legacy_lang_data.update((i.split("=", 1) for i in items))

with open(os.path.join("mappings", "all_mappings"), 'r', encoding='utf8') as f:
        mappings = json.load(f)['mappings']

mapping_data = {}

for item in mappings:
    mapping_file = item + ".json"
    if mapping_file not in os.listdir("mappings"):
        warning = f"Warning: Missing mapping '{mapping_file}', skipping."
        print(f"\033[33m{warning}\033[0m", file=sys.stderr)
    else:
        with open(os.path.join("mappings", mapping_file), 'r', encoding='utf8') as f:
            mapping = json.load(f)
        for k, v in mapping:
            mapping_data.update({k: v})

for k in mapping_data.keys():
    if k not in legacy_lang_data.keys():
        print(k) 