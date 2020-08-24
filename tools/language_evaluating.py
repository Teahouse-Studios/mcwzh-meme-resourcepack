from json import load
# It's a garbage
# And somehow it's countable

with open("zh_cn.json", 'r', encoding='utf8') as f:
    official_lang_data = load(f)

with open("assets/minecraft/lang/zh_meme.json", 'r', encoding='utf8') as f:
    meme_lang_data = load(f)

print(*(k for k in official_lang_data if k in meme_lang_data), sep='\n')
