import os
import json
# It's a garbage
# And somehow it's countable

with open("zh_cn.json", 'r', encoding='utf8') as f:
    official_lang_data = json.load(f)

with open("assets/minecraft/lang/zh_meme.json", 'r', encoding='utf8') as f:
    meme_lang_data = json.load(f)

print(*(set(official_lang_data) ^ set(meme_lang_data)), sep='\n')
