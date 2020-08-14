import os
import json
import sys

with open("1.12.lang", 'r', encoding='utf8') as f:
    legacy_lang_data = dict(line.strip().split(
        "=", 1) for line in f if line.strip() != '' and not line.startswith('#'))
mappings = json.load(open(os.path.join(
    "mappings", "all_mappings"), 'r', encoding='utf8'))['mappings']
for item in mappings:
    mapping_file = item + ".json"
    if mapping_file not in os.listdir("mappings"):
        print(
            f"\033[33mWarning: Missing mapping '{mapping_file}', skipping.\033[0m", file=sys.stderr)
    else:
        mapping = json.load(
            open(os.path.join("mappings", mapping_file), 'r', encoding='utf8'))
        mapping_data = {k: v for k, v in mapping.items()}
print(*[k for k in legacy_lang_data if k not in mapping_data], sep='\n')
