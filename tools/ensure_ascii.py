import json
with open('zh_meme.json') as f:
    d = json.load(f)
with open('zh_meme.json', 'w', encoding='utf8') as b:
    json.dump(d, b, ensure_ascii=False, indent=4)