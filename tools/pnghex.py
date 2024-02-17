from PIL import Image
import os
def png_to_hex(png_file):
    img =  Image.open(png_file).convert('1')
    width, height = img.size
    data = list(img.getdata())
    hex_string = ''
    for y in range(height):
        row = data[y*width:(y+1)*width]
        byte = ''
        for x in range(width):
            byte += '1' if row[x] == 0 else '0'
            if (x+1) % 8 == 0:
                hex_string += f'{int(byte, 2):02X}'
                byte = ''
    return hex_string

def png_to_hex_mc(png_file):
    img =  Image.open(png_file)
    width, height = img.size
    data = list(img.getdata())
    hex_string = ''
    for y in range(height):
        row = data[y*width:(y+1)*width]
        byte = ''
        for x in range(width):
            byte += '1' if row[x] == (255,255,255,255) else '0'
            if (x+1) % 8 == 0:
                hex_string += f'{int(byte, 2):02X}'
                byte = ''
    return hex_string

def hex_to_png(hex_string, png_file):
    width = 8 if len(hex_string) == 32 else 16
    height = 16
    data = []
    for i in range(0, len(hex_string), 2):
        byte = format(int(hex_string[i:i+2], 16), '08b')
        data.extend([0 if b == '0' else 255 for b in byte])
    img =  Image.new ('1', (width, height))
    img.putdata(data)
    img.save (png_file)

def cesi_pngs_to_hex():
    png_folder=r"C:\Users\Lakeus\Downloads\CESI\cjk-{}"
    ext="bcdef"

    for i in ext:
        hex_filename="cjk-{}.hex".format(i)
        hex_file = os.path.join(r"C:\Users\Lakeus\Downloads\CESI", hex_filename)
        with open(hex_file, "w", encoding="utf-8") as f:
            for filename in os.listdir(png_folder.format(i)):
                if filename.endswith(".png"):
                    png_file=os.path.join(png_folder.format(i), filename)
                    unicode_value = filename.split('u')[1].split(".")[0]
                    f.write(unicode_value.upper()+":"+png_to_hex(png_file)+"\n")

def split_mc_unicode_page(png_file, cp_start, path):
    original_image = Image.open(png_file)
    width, height = original_image.size
    num_images = (width // 16) * (height // 16)

    for i in range(num_images):
        start_x = (i % (width // 16)) * 16
        start_y = (i // (width // 16)) * 16

        new_image = Image.new("RGBA", (16, 16))
        new_image.paste(original_image.crop((start_x, start_y, start_x + 16, start_y + 16)))
        unicode_code = i + cp_start
        file_name = f"u{hex(unicode_code)[2:]}.png"
        new_image.save(path+file_name)

def pngs_to_hex(path, hex_file):
    with open(hex_file,'w',newline='\n') as hex_file:
        for filename in os.listdir(path):
            if filename.endswith(".png"):
                png_file = os.path.join(path,filename)
                unicode_value=filename.split('u')[1].split('.')[0]
                hex_file.write(unicode_value.upper()+":"+png_to_hex(png_file)+"\n")

def pngs_to_hex_mc(path, hex_file):
    with open(hex_file,'w',newline='\n') as hex_file:
        for filename in os.listdir(path):
            if filename.endswith(".png"):
                png_file = os.path.join(path,filename)
                unicode_value=filename.split('u')[1].split('.')[0]
                hex_file.write(unicode_value.upper()+":"+png_to_hex_mc(png_file)+"\n")

def read_hex_file_glyphs(hex_file):
    glyphs={}
    with open(hex_file) as hex_file:
        for ln in hex_file:
            cp=ln.split(":")[0]
            glyph_data=ln.split(":")[1].rstrip("\n")
            glyphs[cp]=glyph_data
    return glyphs

def remove_identical_glyphs(partial_hex_file, unifont_hex_file, final_hex_file):
    partial_hex_file_glyphs = read_hex_file_glyphs(partial_hex_file)
    unifont_hex_file_glyphs = read_hex_file_glyphs(unifont_hex_file)
    with open(final_hex_file, "w", newline="\n") as final_hex_file:
        for k in partial_hex_file_glyphs:
            if partial_hex_file_glyphs[k] != unifont_hex_file_glyphs.get(k):
                final_hex_file.write(k+":"+partial_hex_file_glyphs[k]+"\n")

