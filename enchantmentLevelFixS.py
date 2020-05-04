import json

# WIP

lang = {}

i = 11

while i <= 32767:
    lang['enchantment.level.' + str(i)] = str(i)
    print(i)
    i += 1

with open("enchlevelfixS.json", 'w', encoding='utf8') as lang_file:
    lang_file.write(json.dumps(lang, indent=4, ensure_ascii=False))