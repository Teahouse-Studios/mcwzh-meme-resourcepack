cps=[]
def generate_bitmap_font_provider(cps):
    for cp in cps:
        cp -= 0x10000
        lead = cp >> 10
        trail = cp & 0b00000000001111111111
        lead += 0xd800
        trail += 0xdc00
        print("""
            {{
                "type": "bitmap",
                "file": "minecraft:font/character-{0:x}.png",
                "ascent": 7,
                "chars": ["\\u{1:X}\\u{2:X}"]
            }},""".format(cp+0x10000,lead,trail),end="")