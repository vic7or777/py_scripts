import sys, os, io, struct, glob

from collections import namedtuple
from typing import NamedTuple
from pathlib import Path

# ===========================================================================
# pip install pillow
# ---------------------------------------------------------------------------
# https://stackoverflow.com/a/63096701
import subprocess, pkg_resources
required = {'pillow',}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])
# ===========================================================================

from PIL import Image, TgaImagePlugin, PcxImagePlugin, WalImageFile, ImageEnhance, ImageColor

script_path = os.path.abspath(os.path.dirname(sys.argv[0]))
script_name = os.path.abspath(sys.argv[0])
os.chdir(script_path)
os.system('cls')


pak_name = script_name.replace('.py', '.pak')
# pak_name = fr'c:\quake2\baseq2\{pak_name}'

model_t = namedtuple('model_t', 'dir, model, skins, masks')
mask_t = namedtuple('mask_t', 'file, color, blend')

models = (
    model_t( r'models\weapons\g_shotg' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_barrel.png'    , '#ff6600', 1.00),
        mask_t('mask_butt.png'      , '#000000', 1.00),
        mask_t('mask_handle.png'    , '#000000', 1.00),
        mask_t('mask_mag.png'       , '#000000', 1.00),
        mask_t('mask_pivot.png'     , '#000000', 1.00),
    )),
    model_t( r'models\weapons\g_shotg2' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_bandage.png'   , '#ff6600', 1.00),
        mask_t('mask_barrel.png'    , '#000000', 1.00),
        mask_t('mask_butt1.png'     , '#ff6600', 1.00),
        mask_t('mask_butt2.png'     , '#000000', 1.00),
        mask_t('mask_handle1.png'   , '#ff6600', 1.00),
        mask_t('mask_handle2.png'   , '#ff6600', 1.00),
        mask_t('mask_pivot.png'     , '#ff6600', 1.00),
    )),
    model_t( r'models\items\ammo\shells\medium' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t( None                , '#883300', 1.00),
    )),
    model_t( r'models\weapons\g_machn' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_body.png'      , '#ffdd00', 1.00),
        mask_t('mask_butt.png'      , '#000000', 1.00),
        mask_t('mask_handle.png'    , '#000000', 1.00),
        mask_t('mask_pivot.png'     , '#000000', 1.00),
        mask_t('mask_sight.png'     , '#000000', 1.00),
    )),
    model_t( r'models\weapons\g_chain' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_bandage.png'   , '#ffdd00', 1.00),
        mask_t('mask_barrel.png'    , '#000000', 1.00),
        mask_t('mask_body.png'      , '#ffdd00', 1.00),
        mask_t('mask_handle.png'    , '#ffdd00', 1.00),
        mask_t('mask_pivot.png'     , '#ffdd00', 1.00),
    )),
    model_t( r'models\items\ammo\bullets\medium' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t( None                , '#886600', 1.00),
    )),
    model_t( r'models\weapons\g_launch' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_barrel.png'    , '#880011', 1.00),
        mask_t('mask_body.png'      , '#000000', 1.00),
        mask_t('mask_gren.png'      , '#000000', 1.00),
        mask_t('mask_handle.png'    , '#880011', 1.00),
        mask_t('mask_pivot.png'     , '#000000', 1.00),
        mask_t('mask_trigger.png'   , '#880011', 1.00),
    )),
    model_t( r'models\items\ammo\grenades\medium' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_body.png'      , '#880011', 1.00),
        mask_t('mask_cap.png'       , '#000000', 1.00),
    )),
    model_t( r'models\objects\grenade' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_body.png'      , '#ff0022', 1.00),
        mask_t('mask_stripe.png'    , '#ff0000', 1.00),
    )),
    model_t( r'models\objects\grenade2' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_body.png'      , '#ff0022', 1.00),
        mask_t('mask_middle.png'    , '#ff0000', 1.00),
    )),
    model_t( r'models\weapons\g_rocket' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_barrel.png'    , '#ff0000', 1.00),
        mask_t('mask_barrel_hi.png' , '#ff0000', 1.00),
        mask_t('mask_barrel_low.png', '#ff0000', 1.00),
        mask_t('mask_body_low.png'  , '#000000', 1.00),
        mask_t('mask_body.png'      , '#ff0000', 1.00),
        mask_t('mask_body_hi.png'   , '#000000', 1.00),
        mask_t('mask_handle.png'    , '#000000', 1.00),
        mask_t('mask_mag.png'       , '#ff0000', 1.00),
        mask_t('mask_rockets.png'   , '#000000', 1.00),
    )),
    model_t( r'models\items\ammo\rockets\medium' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t( None                , '#880000', 1.00),
    )),
    model_t( r'models\objects\rocket' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_body.png'      , '#ff0000', 1.00),
        mask_t('mask_fire.png'      , '#ff8800', 1.00),
        mask_t('mask_stripe.png'    , '#000000', 1.00),
        mask_t('mask_tail.png'      , '#880000', 1.00),
    )),
    model_t( r'models\weapons\g_rail' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_barrel.png'    , '#00ff00', 1.00),
        mask_t('mask_barrel_l.png'  , '#00ff00', 1.00),
        mask_t('mask_barrel_r.png'  , '#00ff00', 1.00),
        mask_t('mask_body.png'      , '#000000', 1.00),
        mask_t('mask_butt1.png'     , '#00ff00', 1.00),
        mask_t('mask_butt2.png'     , '#000000', 1.00),
        mask_t('mask_handle.png'    , '#000000', 1.00),
        mask_t('mask_pipe.png'      , '#000000', 1.00),
    )),
    model_t( r'models\items\ammo\slugs\medium' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t( None                , '#008800', 1.00),
    )),
    model_t( r'models\weapons\g_hyperb' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_barrel.png'    , '#0088ff', 1.00),
        mask_t('mask_body.png'      , '#0088ff', 1.00),
        mask_t('mask_butt.png'      , '#000000', 1.00),
        mask_t('mask_handle1.png'   , '#000000', 1.00),
        mask_t('mask_handle2.png'   , '#000000', 1.00),
        mask_t('mask_mag.png'       , '#000000', 1.00),
        mask_t('mask_pivot.png'     , '#000000', 1.00),
    )),
    model_t( r'models\weapons\g_bfg' , 'tris.md2' , ('skin.pcx', ) ,
    (
        mask_t('mask_barrel.png'    , '#0000ff', 1.00),
        mask_t('mask_body.png'      , '#0000ff', 1.00),
        mask_t('mask_butt1.png'     , '#000000', 1.00),
        mask_t('mask_butt2.png'     , '#0000ff', 1.00),
        mask_t('mask_handl1.png'    , '#000000', 1.00),
        mask_t('mask_handl2.png'    , '#0000ff', 1.00),
        mask_t('mask_pipe.png'      , '#000000', 1.00),
        mask_t('mask_pivot.png'     , '#0000ff', 1.00),
    )),
    model_t( r'models\items\ammo\cells\medium' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t( None                , '#004488', 1.00),
    )),

    model_t( r'models\items\mega_h' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_body.png'      , '#dddddd', 1.00),
        mask_t('mask_cr.png'        , '#880000', 1.00),
        mask_t('mask_num.png'       , '#444444', 1.00),

    )),
    model_t( r'models\items\adrenal' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_body.png'      , '#444444', 1.00),
        mask_t('mask_num.png'       , '#ffffff', 1.00),
        mask_t('mask_print.png'     , '#0000ff', 1.00),

    )),
    model_t( r'models\items\healing\large' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_body.png'      , '#444444', 1.00),
        mask_t('mask_num.png'       , '#660000', 1.00),
        mask_t('mask_num_sh.png'    , '#000000', 1.00),

    )),
    model_t( r'models\items\healing\medium' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_body.png'      , '#444444', 1.00),
        mask_t('mask_num.png'       , '#660000', 1.00),
        mask_t('mask_num_sh.png'    , '#000000', 1.00),

    )),
    model_t( r'models\items\healing\stimpack' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_body.png'      , '#444444', 1.00),
        mask_t('mask_num.png'       , '#ffffff', 1.00),
        mask_t('mask_print.png'     , '#0000ff', 1.00),

    )),
    model_t( r'models\items\armor\body' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_top.png'       , '#880000', 1.00),
        mask_t('mask_mid.png'       , '#770000', 1.00),
        mask_t('mask_bot.png'       , '#880000', 1.00),
        mask_t('mask_shldr.png'     , '#ff0000', 1.00),
        mask_t('mask_num.png'       , '#888888', 1.00),

    )),
    model_t( r'models\items\armor\combat' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_top.png'       , '#ffdd00', 1.00),
        mask_t('mask_mid.png'       , '#ddff00', 1.00),
        mask_t('mask_bot.png'       , '#ffdd00', 1.00),
        mask_t('mask_num.png'       , '#888888', 1.00),
    )),
    model_t( r'models\items\armor\jacket' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_body.png'      , '#666633', 1.00),
        mask_t('mask_num.png'       , '#888888', 1.00),

    )),
    model_t( r'models\items\armor\shard' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_back.png'      , '#444444', 1.00),
        mask_t('mask_front.png'     , '#882020', 1.00),
        mask_t('mask_num.png'       , '#888888', 1.00),

    )),
    model_t( r'models\items\armor\screen' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_body.png'      , '#008800', 1.00),
        mask_t('mask_l1.png'        , '#000088', 1.00),
        mask_t('mask_l2.png'        , '#880000', 1.00),

    )),
    model_t( r'models\items\armor\shield' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_body.png'      , '#008800', 1.00),
        mask_t('mask_l1.png'        , '#000088', 1.00),
        mask_t('mask_l2.png'        , '#880000', 1.00),

    )),
    model_t( r'models\items\quaddama' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_body.png'      , '#0088ff', 1.00),
        mask_t('mask_nail1.png'     , '#0000ff', 1.00),
        mask_t('mask_nail2.png'     , '#0000ff', 1.00),
    )),
    model_t( r'models\items\invulner' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_skul.png'      , '#000000', 1.00),
        mask_t('mask_wings.png'     , '#ff0000', 1.00),

    )),
    model_t( r'models\items\pack' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_front.png'     , '#666633', 1.00),
        mask_t('mask_bak.png'       , '#000000', 1.00),
        mask_t('mask_chassis.png'   , '#000000', 1.00),
        mask_t('mask_sling.png'     , '#666633', 1.00),
    )),
    model_t( r'models\items\band' , 'tris.md2' , ('skin.pcx', ) , (
        mask_t('mask_body.png'      , '#666633', 1.00),
        mask_t('mask_l1.png'        , '#880000', 1.00),
        mask_t('mask_l2.png'        , '#000088', 1.00),

    )),

    model_t( r'players\male' , 'tris.md2' , (
                                            'cipher.pcx'  ,
                                            'claymore.pcx',
                                            'flak.pcx'    ,
                                            'grunt.pcx'   ,
                                            'howitzer.pcx',
                                            'major.pcx'   ,
                                            'nightops.pcx',
                                            'pointman.pcx',
                                            'psycho.pcx'  ,
                                            'rampage.pcx' ,
                                            'razor.pcx'   ,
                                            'recon.pcx'   ,
                                            'scout.pcx'   ,
                                            'sniper.pcx'  ,
                                            'viper.pcx'   ,
        ) , (
        mask_t('mask_head.png'      , '#ffff00', 1.00),
        mask_t('mask_hand.png'      , '#ffff00', 1.00),
        mask_t('mask_body_hi.png'   , '#ff6600', 1.00),
        mask_t('mask_body_low.png'  , '#ff8800', 1.00),
        mask_t('mask_leg1.png'      , '#ff6600', 1.00),
        mask_t('mask_leg2.png'      , '#ff8800', 1.00),
        mask_t('mask_leg3.png'      , '#ff6600', 1.00),
        mask_t('mask_leg4.png'      , '#ffff00', 1.00),
    )),
    model_t( r'players\female' , 'tris.md2' , (
                                            'athena.pcx'  ,
                                            'brianna.pcx' ,
                                            'cobalt.pcx'  ,
                                            'ensign.pcx'  ,
                                            'jezebel.pcx' ,
                                            'jungle.pcx'  ,
                                            'lotus.pcx'   ,
                                            'stiletto.pcx',
                                            'venus.pcx'   ,
                                            'voodoo.pcx'  ,
        ) , (
        mask_t('mask_head.png'      , '#88ff00', 1.00),
        mask_t('mask_hair.png'      , '#88ff00', 1.00),
        mask_t('mask_hand.png'      , '#88ff00', 1.00),
        mask_t('mask_body_back.png' , '#88ff00', 1.00),
        mask_t('mask_body_hi.png'   , '#ff0022', 1.00),
        mask_t('mask_leg1.png'      , '#0088ff', 1.00),
        mask_t('mask_leg2.png'      , '#ff0022', 1.00),
        mask_t('mask_leg3.png'      , '#88ff00', 1.00),
    )),
)

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
            fn = e.filename.encode('ascii')
            self.pak_file.write(struct.Struct('<56s').pack(fn))
            self.pak_file.write(struct.Struct('<l'  ).pack(e.offset))
            self.pak_file.write(struct.Struct('<l'  ).pack(e.length))
            self.table_size += 64
        self.pak_file.seek(0)
        self.pak_file.write(struct.Struct('<4s2l').pack(b'PACK', self.pointer, self.table_size))
        self.pak_file.close()

    def add_file_from_disk(self, fn):
        if os.path.exists(fn):
            with open(fn, 'rb') as f:
                self.add_file(fn, f)

    def add_file_from_disk1(self, fn, pn):
        if os.path.exists(fn):
            with open(fn, 'rb') as f:
                self.add_file(pn, f)


if os.path.exists(pak_name):
    print(f'Exist')

pak = Pak_Make(pak_name, '')
print(f'Making... : {pak_name}')

colormap = Image.open(f'in\\pics\\colormap.pcx', formats = ('PCX',))
colormap.format == 'PCX'

for i in models:

    for s in i.skins:

        im1 = Image.open(f'in\\{i.dir}\\{s}', formats = ('PCX',))
        im1.format == 'PCX'
        im1.putpalette(colormap.palette)
        im1 = im1.convert('RGBA')

        for m in i.masks:
            color = ImageColor.getcolor(m.color, "RGB")
            mono = Image.new(im1.mode, (im1.width, im1.height), color)
            im2 = Image.blend(im1, mono, m.blend)
            if m.file:
                im_mask = Image.open(f'in\\mask\\{i.dir}\\{m.file}').convert('L')
                im1 = Image.composite(im2, im1, im_mask)
            else:
                im1 = im2
        # Add colored skin in png format to pak
        with io.BytesIO() as f:
            im1.save(f, 'PNG')
            fn = f'{i.dir}\\{s}'.replace('.pcx', '.png')
            pak.add_file(fn, f)

# Add source files to pak
for i in models:

    # Add model file to pak
    mdl = f'{i.dir}\\{i.model}'
    if os.path.exists(mdl):
        pak.add_file_from_disk(mdl)
    else:
        pak.add_file_from_disk1(f'in\\{mdl}', mdl)

    # Add skin in pcx format to pak
    for s in i.skins:
        skn = f'{i.dir}\\{s}'
        pak.add_file_from_disk(f'in\\{skn}')
        
        if os.path.exists(f'in\\bright\\{skn}'):
            pak.add_file_from_disk1(f'in\\bright\\{skn}', skn)
        elif os.path.exists(skn):
            pak.add_file_from_disk1(f'{skn}', skn)
        else:
            pak.add_file_from_disk1(f'in\\{skn}', skn)

    # Add mask skin in png format to pak
    pak.add_file_from_disk(f'in\\mask\\{i.dir}\\mask.png')
    for m in i.masks:
        if m.file:
            pak.add_file_from_disk(f'in\\mask\\{i.dir}\\{m.file}')

# Add colormap.pcx
pak.add_file_from_disk(f'in\\pics\\colormap.pcx')

# Add self script
pak.add_file_from_disk(script_name)

pak.finalize()

print(f'Ready !')
