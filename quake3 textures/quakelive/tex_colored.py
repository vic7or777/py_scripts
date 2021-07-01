import sys, os, io, glob, struct, shutil

# pip install pillow
# https://stackoverflow.com/a/63096701
import subprocess, pkg_resources
required = {'pillow',} 
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])
from PIL import Image, ImageFile, TgaImagePlugin, ImageEnhance, ImageColor

# https://stackoverflow.com/a/47958486
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.LOAD_TRUNCATED_IMAGES = True

script_path = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(script_path)
os.system('cls')

# https://stackoverflow.com/a/61730849
def get_dominant_color(src_img, palette_size=16):
    img = src_img.copy()
    # img.thumbnail((100, 100))
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=palette_size)
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]
    dominant_color = palette[palette_index*3:palette_index*3+3]
    r,g,b = dominant_color
    if len(color_counts)>1 and (r<20 and g<20 and b<20):
        palette_index = color_counts[1][1]
        dominant_color = palette[palette_index*3:palette_index*3+3]
    return tuple(dominant_color)

def mono_color_blend(im, val, col):
    mono = Image.new(im.mode, (im.width, im.height), col)
    return Image.blend(im, mono, val)

def change_intens(im, val, col):
    if val == '1.00':
        return im
    else:
        if im.format == 'WAL':
            br = ImageEnhance.Brightness(im.convert('RGBA') )
        else:
            br = ImageEnhance.Brightness(im)
        return br.enhance(float(val))

# Load all textures from disk
# Detect dominant color of each texture
# Save new texture

for tex in glob.iglob(f'{script_path}\\in\\textures\\**\\*.*', recursive=True):

    ext = tex.split('.')[1].lower()
    if not ext in ('wal', 'png', 'tga', 'jpg', 'jpeg'):
        continue

    path = tex.replace('\\in\\', '\\out\\')
    if os.path.exists(path):
        continue

    pathd = os.path.dirname(path)
    if not os.path.exists(pathd):
        os.makedirs(pathd)

    if ext == 'png':
        im = Image.open(tex)
        fmt = 'PNG'

    elif ext == 'tga':
        im = Image.open(tex, formats = ('TGA',))
        im.format == 'TGA'
        fmt = 'TGA'

    elif ext == 'jpg' or ext == 'jpeg':
        im = Image.open(tex)
        fmt = 'JPEG'

    if im.mode == 'L':
        im = im.convert("RGBA")
    col = get_dominant_color(im)
    im1 = mono_color_blend(im, 0.85, col)
    im1.save(fp=path, format=fmt)

ql_dir = r'c:\Program Files (x86)\Steam\steamapps\common\Quake Live\baseq3'
# https://stackoverflow.com/a/25650295
shutil.make_archive(fr'{ql_dir}\textures', 'zip', r'out')

os.rename(fr'{ql_dir}\textures.zip', fr'{ql_dir}\textures.pk3')

print(f'Ready !')
