import sys, os, io, glob, struct

# pip install pillow
# https://stackoverflow.com/a/63096701
import subprocess, pkg_resources
required = {'pillow',} 
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])
from PIL import Image, TgaImagePlugin, PcxImagePlugin, WalImageFile, ImageEnhance, ImageColor

script_path = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(script_path)
os.system('cls')

class File_Entry:
    pass

# https://tomeofpreach.wordpress.com/2013/06/22/makepak-py/
class Pak_Make:
    def __init__(self, pak_name, src_dir):
        self.pak_file = open(pak_name,'wb')
        self.pak_file.write(struct.Struct('<4s2l').pack(b'PACK',0,0))
        self.src_dir = src_dir
        self.pointer = 12
        self.table_size = 0
        self.fileentries = []

    def add_file(self, file_path, f):
        f.seek(0)
        self.pak_file.write(f.read())
        e = File_Entry()
        e.filename = os.path.relpath(file_path, self.src_dir).replace('\\','/')
        e.offset = self.pointer
        e.length = f.tell()
        self.fileentries.append(e)
        self.pointer += e.length

    def finalize(self):
        for e in self.fileentries:
            self.pak_file.write(struct.Struct('<56s').pack(e.filename.encode('ascii')))
            self.pak_file.write(struct.Struct('<l'  ).pack(e.offset))
            self.pak_file.write(struct.Struct('<l'  ).pack(e.length))
            self.table_size += 64
        self.pak_file.seek(0)
        self.pak_file.write(struct.Struct('<4s2l').pack(b'PACK', self.pointer, self.table_size))
        self.pak_file.close()

def pak_images(images_list, pak_name, apply_func, val=0):

    print(f'Making... : {pak_name}')

    if os.path.exists(pak_name):
        print(f'Exist')
        return

    if images_list == []:
        return

    pak = Pak_Make(pak_name, 'out')

    for im, path, im_type, col in images_list:
        # print(path)
        im1 = apply_func(im, val, col)
        if not im1: continue
        with io.BytesIO() as f:
            im1.save(f, im_type)
            pak.add_file(path, f)

    pak.finalize()
    print(f'Ok !')

# https://stackoverflow.com/a/61730849
def get_dominant_color(src_img, palette_size=16):
    img = src_img.copy()
    # img = img.convert("RGBA")
    # img.thumbnail((100, 100))
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=palette_size)
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]
    dominant_color = palette[palette_index*3:palette_index*3+3]
    r,g,b = dominant_color
    if len(color_counts)>1 and (r<10 and g<10 and b<10):
        palette_index = color_counts[1][1]
        dominant_color = palette[palette_index*3:palette_index*3+3]
    return tuple(dominant_color)

def mono_color_blend(im, val, col):
    if val == '1.00':
        return Image.new(im.mode, (im.width, im.height), col)
    if im.format == 'WAL':
        mono = Image.new('RGBA', (im.width, im.height), col)
        return Image.blend(im.convert('RGBA'), mono, val)
    else:
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

def dim_lamp(im, val, col):
    im1 = im.resize((20,20), Image.LANCZOS)
    im1 = im1.convert('L')
    count = 0
    for y in range(im1.height):
        for x in range(im1.width):
            pixel = im1.getpixel((x, y))
            if pixel >= 35:
                count += 1
    if count>25:
        if im.format == 'WAL': br = ImageEnhance.Brightness(im.convert('RGBA'))
        else: br = ImageEnhance.Brightness(im)
        return br.enhance(float(val))
    return None

# Load all textures from disk
# Apply propper colormap to textures in WAL format
# Detect dominant color of each texture
# Save all data to memory (to "images_list")

colormap = Image.open(f'{script_path}\\in\\pics\\colormap.pcx', formats = ('PCX',))
colormap.format == 'PCX'
images_list = []
for tex in glob.iglob(f'{script_path}\\in\\textures\\**\\*.*', recursive=True):

    ext = tex.split('.')[1].lower()
    if not ext in ('wal', 'png', 'tga', 'jpg', 'jpeg'):
        continue

    path = tex.replace('\\in\\', '\\out\\')

    if ext == 'wal':
        path = f'{path.split(".")[0]}.png'
        im = WalImageFile.open(tex)
        im.putpalette(colormap.palette)
        col = get_dominant_color(im)
        images_list.append((im, path, 'PNG', col))

    elif ext == 'png':
        im = Image.open(tex)
        col = get_dominant_color(im)
        images_list.append((im, path, 'PNG', col))

    elif ext == 'tga':
        im = Image.open(tex, formats = ('TGA',))
        im.format == 'TGA'
        col = get_dominant_color(im)
        images_list.append((im, path, 'TGA', col))

    elif ext == 'jpg' or ext == 'jpeg':
        im = Image.open(tex)
        col = get_dominant_color(im)
        images_list.append((im, path, 'JPEG', col))

Blends = (
    '0.50',
    '0.75',
    '0.85',
    '0.90',
    '1.00',
)

Intensities = (
    '0.33',
    '0.50',
    '0.66',
    '0.75',
    '1.00',
    '1.25',
    '1.50',
    '1.75',
    '2.00',
)

# Apply function "mono_color_blend" to all textures in "images_list" and save to PAK file
for i in Blends:
    pak_images(images_list, f'pak9_monocolor_blend_{i}.pak', mono_color_blend, float(i))

# Apply function "change_intens" to all textures in "images_list" and save to PAK file
for i in Intensities:
    pak_images(images_list, f'pak9_intensity_{i}.pak', change_intens, i)

# Apply function "dim_lamp" to all textures in "images_list" and save to PAK file
pak_images(images_list, f'pak9_lamp_0.75.pak', dim_lamp, 0.75)

print(f'Ready !')
