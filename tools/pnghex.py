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
    img = Image.open(png_file)
    width, height = img.size
    data = list(img.getdata())
    hex_string = ''
    for y in range(height):
        row = data[y*width:(y+1)*width]
        byte = ''
        for x in range(width):
            byte += '1' if row[x] == (255, 255, 255, 255) else '0'
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

# create_hk_patch_from_tw_hex(r'D:\farstar\glyph_82',r'C:\Users\Lakeus\Downloads\unifont-16.0.01\unifont-16.0.01\font\precompiled\unifont_all-16.0.01.hex',r'D:\farstar\glyph_82\hk=#tw.txt',r'D:\farstar\glyph_82_tw.hex',r'D:\farstar\glyph_82_hk.hex',0x8200)
def create_hk_patch_from_tw_hex(path, unifont_hex_file, hk_ref_tw_list, tw_hex_file, final_hex_file, cp_start=0x4E00):
    unifont_glyphs = read_hex_file_glyphs(unifont_hex_file)
    tw_glyphs = read_hex_file_glyphs(tw_hex_file)
    with open(hk_ref_tw_list,'r',encoding='utf-8') as f:
        hk_ref_tw_str = f.read()
    glyphs = {}
    for i in range(256):
        cp = cp_start + i
        cp_str = hex(cp)[2:].upper()
        if chr(cp) in hk_ref_tw_str:
            glyphs[cp_str] = tw_glyphs[cp_str]
        else:
            glyphs[cp_str] = unifont_glyphs[cp_str]

    for filename in os.listdir(path):
        if filename.endswith("-hk.png"):
            png_file = os.path.join(path, filename)
            unicode_value = filename.split('u')[1].split('-hk.')[0]
            glyphs[unicode_value.upper()] = png_to_hex_mc(png_file)
    with open(final_hex_file,'w',newline='\n') as final_hex_file:
        for k in glyphs:
            final_hex_file.write(k+':'+glyphs[k]+'\n')

def print_256_chr_in_batch(cp_start=0x4E00):
    for i in range(256):
        print(chr(cp_start + i),end='')
    print()

# unihex_to_unicode_page(r'C:\Users\Lakeus\Downloads\unifont-16.0.01\unifont-16.0.01\font\precompiled\unifont_all-16.0.01.hex',r'D:\farstar\glyph_82.png',cp_start=0x8200)
def unihex_to_unicode_page(hex_file, output_image_file, cp_start=0x4E00, img_size=256, sub_img_size=16, glyph_size=(16, 16)):
    # 创建256x256的图像，背景为白色
    img = Image.new('1', (img_size, img_size), color=1)
    
    # 读取hex文件中的字形数据
    glyphs = read_hex_file_glyphs(hex_file)
    
    # 初始化图块位置
    x = 0
    y = 0
    
    # 从指定的码位开始处理
    glyph_items = list(glyphs.items())
    for unicode_val, hex_string in glyph_items:
        # 如果当前码位小于开始码位，跳过
        if int(unicode_val, 16) < cp_start:
            continue

        # 将hex字形转换为像素数据
        glyph_data = []
        for i in range(0, len(hex_string), 2):
            byte = format(int(hex_string[i:i+2], 16), '08b')
            glyph_data.extend([0 if b == '0' else 255 for b in byte])
        
        # 创建一个16x16的图块
        glyph_img = Image.new('1', glyph_size)
        glyph_img.putdata(glyph_data)
        
        # 将图块粘贴到大图上
        img.paste(glyph_img, (x, y))
        
        # 更新图块位置，每16个图块换一行
        x += sub_img_size
        if x >= img_size:
            x = 0
            y += sub_img_size
            if y >= img_size:
                break
    
    # 保存为PNG文件
    img.save(output_image_file)

"""js
// 在 shs-cid 工具内输入所有所需文字并加载后执行
// 获取所有 .cid 元素
const cidElements = document.querySelectorAll('.cid');

// 存储符合条件的 .cid-char 文本
const charTexts = [];

// 遍历每个 .cid 元素
cidElements.forEach(cid => {
    // 获取 .cid-locale 的内容
    const localeElement = cid.querySelector('.cid-locale');
    const langElement = localeElement.querySelector('.cid-lang');
    const equivElement = localeElement.querySelector('.cid-equiv');
    
    // 检查是否符合条件
    if ( (langElement && langElement.innerText === 'HK' && 
        equivElement && equivElement.innerText === '=TW#' ) || 
        (langElement && langElement.innerText === 'TW' && 
        equivElement && equivElement.innerText === '=HK#' ) ) {
        
        // 获取 .cid-char 的内容
        const charElement = cid.querySelector('.cid-char');
        
        if (charElement) {
            // 提取 innerText 并添加到数组
            charTexts.push(charElement.innerText);
        }
    }
});

// 输出结果
console.log(charTexts.toString().replaceAll(',',''));
"""