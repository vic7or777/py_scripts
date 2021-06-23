import sys, os, io, struct, glob

from collections import namedtuple
from typing import NamedTuple
from pathlib import Path

# pip install pillow
# https://stackoverflow.com/a/63096701
import subprocess, pkg_resources
required = {'pillow',} 
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])
from PIL import Image, TgaImagePlugin, PcxImagePlugin, WalImageFile, ImageEnhance, ImageColor

pak_name = 'mdl_colored.pak'
# pak_name = r'c:\quake2\baseq2\mdl_colored.pak'

models_t = namedtuple('models_t', 'dir, mdl, skin, format, color, blend')
models = (
    models_t( r'in\players\cyborg'  ,  None       , 'oni911.pcx'        , 'png' , '#ffcc00', 0.90 ) ,
    models_t( r'in\players\cyborg'  ,  None       , 'ps9000.pcx'        , 'png' , '#ffcc00', 0.90 ) ,
    models_t( r'in\players\cyborg'  ,  None       , 'tyr574.pcx'        , 'png' , '#ffcc00', 0.90 ) ,

    models_t( r'in\players\male'    ,  None       , 'cipher.pcx'        , 'png' , '#ffff00', 0.90 ) ,
    models_t( r'in\players\male'    ,  None       , 'claymore.pcx'      , 'png' , '#ffff00', 0.90 ) ,
    models_t( r'in\players\male'    ,  None       , 'flak.pcx'          , 'png' , '#ffff00', 0.90 ) ,
    models_t( r'in\players\male'    ,  None       , 'grunt.pcx'         , 'png' , '#ffff00', 0.90 ) ,
    models_t( r'in\players\male'    ,  None       , 'howitzer.pcx'      , 'png' , '#ffff00', 0.90 ) ,
    models_t( r'in\players\male'    ,  None       , 'major.pcx'         , 'png' , '#ffff00', 0.90 ) ,
    models_t( r'in\players\male'    ,  None       , 'nightops.pcx'      , 'png' , '#ffff00', 0.90 ) ,
    models_t( r'in\players\male'    ,  None       , 'pointman.pcx'      , 'png' , '#ffff00', 0.90 ) ,
    models_t( r'in\players\male'    ,  None       , 'psycho.pcx'        , 'png' , '#ffff00', 0.90 ) ,
    models_t( r'in\players\male'    ,  None       , 'rampage.pcx'       , 'png' , '#ffff00', 0.90 ) ,
    models_t( r'in\players\male'    ,  None       , 'razor.pcx'         , 'png' , '#ffff00', 0.90 ) ,
    models_t( r'in\players\male'    ,  None       , 'recon.pcx'         , 'png' , '#ffff00', 0.90 ) ,
    models_t( r'in\players\male'    ,  None       , 'scout.pcx'         , 'png' , '#ffff00', 0.90 ) ,
    models_t( r'in\players\male'    ,  None       , 'sniper.pcx'        , 'png' , '#ffff00', 0.90 ) ,
    models_t( r'in\players\male'    ,  None       , 'viper.pcx'         , 'png' , '#ffff00', 0.90 ) ,

    models_t( r'in\players\female'  ,  None       , 'athena.pcx'        , 'png' , '#88ff00', 0.90 ) ,
    models_t( r'in\players\female'  ,  None       , 'brianna.pcx'       , 'png' , '#88ff00', 0.90 ) ,
    models_t( r'in\players\female'  ,  None       , 'cobalt.pcx'        , 'png' , '#88ff00', 0.90 ) ,
    models_t( r'in\players\female'  ,  None       , 'ensign.pcx'        , 'png' , '#88ff00', 0.90 ) ,
    models_t( r'in\players\female'  ,  None       , 'jezebel.pcx'       , 'png' , '#88ff00', 0.90 ) ,
    models_t( r'in\players\female'  ,  None       , 'jungle.pcx'        , 'png' , '#88ff00', 0.90 ) ,
    models_t( r'in\players\female'  ,  None       , 'lotus.pcx'         , 'png' , '#88ff00', 0.90 ) ,
    models_t( r'in\players\female'  ,  None       , 'stiletto.pcx'      , 'png' , '#88ff00', 0.90 ) ,
    models_t( r'in\players\female'  ,  None       , 'venus.pcx'         , 'png' , '#88ff00', 0.90 ) ,
    models_t( r'in\players\female'  ,  None       , 'voodoo.pcx'        , 'png' , '#88ff00', 0.90 ) ,

    models_t( r'in\models\weapons\g_flareg'             , 'tris.md2' , 'base.pcx'  , 'png' , '#88ff00', 0.66 ) ,
    models_t( r'in\models\weapons\g_blast'              , 'tris.md2' , 'base.pcx'  , 'png' , '#88ff00', 0.66 ) ,

    models_t( r'in\models\weapons\g_shotg'              , 'tris.md2' , 'skin.pcx'  , 'png' , '#ff4400', 0.33 ) ,
    models_t( r'in\models\weapons\g_shotg2'             , 'tris.md2' , 'skin.pcx'  , 'png' , '#ff4400', 0.66 ) ,
    models_t( r'in\models\items\ammo\shells\medium'     , 'tris.md2' , 'skin.pcx'  , 'png' , '#ff4400', 0.33 ) ,

    models_t( r'in\models\weapons\g_machn'              , 'tris.md2' , 'skin.pcx'  , 'png' , '#ffffff', 0.33 ) ,
    models_t( r'in\models\weapons\g_chain'              , 'tris.md2' , 'skin.pcx'  , 'png' , '#ffffff', 0.66 ) ,
    models_t( r'in\models\items\ammo\bullets\medium'    , 'tris.md2' , 'skin.pcx'  , 'png' , '#ffffff', 0.33 ) ,

    models_t( r'in\models\objects\flash'                , 'tris.md2' , 'skin.pcx'  , 'png' , '#000000', 0.95 ) ,
    models_t( r'in\models\objects\smoke'                , 'tris.md2' , 'skin.pcx'  , 'png' , '#ffffff', 0.33 ) ,

    models_t( r'in\models\weapons\g_launch'             , 'tris.md2' , 'skin.pcx'  , 'png' , '#8844cc', 0.66 ) ,
    models_t( r'in\models\items\ammo\grenades\medium'   , 'tris.md2' , 'skin.pcx'  , 'png' , '#8844cc', 0.33 ) ,

    models_t( r'in\models\objects\grenade'              , 'tris.md2' , 'skin.pcx'  , 'png' , '#ff0088', 0.66 ) ,
    models_t( r'in\models\objects\grenade2'             , 'tris.md2' , 'skin.pcx'  , 'png' , '#ff0088', 0.66 ) ,

    models_t( r'in\models\weapons\g_rocket'             , 'tris.md2' , 'skin.pcx'  , 'png' , '#cc0000', 0.75 ) ,
    models_t( r'in\models\items\ammo\rockets\medium'    , 'tris.md2' , 'skin.pcx'  , 'png' , '#cc0000', 0.50 ) ,

    models_t( r'in\models\objects\rocket'               , 'tris.md2' , 'skin.pcx'  , 'png' , '#ff0000', 0.66 ) ,
#   models_t( r'in\models\objects\r_explode'            , 'tris.md2' , 'skin1.pcx' , 'png' , '#000000', 0.66 ) ,
#   models_t( r'in\models\objects\r_explode'            , 'tris.md2' , 'skin2.pcx' , 'png' , '#000000', 0.66 ) ,
#   models_t( r'in\models\objects\r_explode'            , 'tris.md2' , 'skin3.pcx' , 'png' , '#000000', 0.66 ) ,
#   models_t( r'in\models\objects\r_explode'            , 'tris.md2' , 'skin4.pcx' , 'png' , '#000000', 0.66 ) ,
#   models_t( r'in\models\objects\r_explode'            , 'tris.md2' , 'skin5.pcx' , 'png' , '#000000', 0.66 ) ,
#   models_t( r'in\models\objects\r_explode'            , 'tris.md2' , 'skin6.pcx' , 'png' , '#000000', 0.66 ) ,
#   models_t( r'in\models\objects\r_explode'            , 'tris.md2' , 'skin7.pcx' , 'png' , '#000000', 0.66 ) ,

    models_t( r'in\models\weapons\g_rail'               , 'tris.md2' , 'skin.pcx'  , 'png' , '#0000cc', 0.75 ) ,
    models_t( r'in\models\items\ammo\slugs\medium'      , 'tris.md2' , 'skin.pcx'  , 'png' , '#0000cc', 0.50 ) ,

    models_t( r'in\models\weapons\g_hyperb'             , 'tris.md2' , 'skin.pcx'  , 'png' , '#0088ff', 0.66 ) ,
    models_t( r'in\models\weapons\g_bfg'                , 'tris.md2' , 'skin.pcx'  , 'png' , '#0044ff', 0.66 ) ,
    models_t( r'in\models\weapons\g_disint'             , 'tris.md2' , 'skin.pcx'  , 'png' , '#0044ff', 0.66 ) ,
    models_t( r'in\models\items\ammo\cells\medium'      , 'tris.md2' , 'skin.pcx'  , 'png' , '#0044ff', 0.33 ) ,

    models_t( r'in\models\objects\laser'                , 'tris.md2' , 'skin.pcx'  , 'png' , '#0088ff', 0.66 ) ,
    models_t( r'in\models\objects\explode'              , 'tris.md2' , 'skin.pcx'  , 'png' , '#0088ff', 0.33 ) ,

    models_t( r'in\models\items\ammo\nuke'              , 'tris.md2' , 'skin.pcx'  , 'png' , '#000000', 0.33 ) ,
    models_t( r'in\models\items\ammo\mines'             , 'tris.md2' , 'skin.pcx'  , 'png' , '#000000', 0.33 ) ,
    models_t( r'in\models\objects\dmspot'               , 'tris.md2' , 'skin.pcx'  , 'png' , '#00ff00', 0.33 ) ,
    models_t( r'in\models\objects\dmspot'               , 'tris.md2' , 'skin2.pcx' , 'png' , '#00ff00', 0.33 ) ,

#   models_t( r'in\models\objects\banner'               , 'tris.md2' , 'skin.pcx'  , 'png' , '#000000', 0.66 ) ,
#   models_t( r'in\models\objects\barrels'              , 'tris.md2' , 'skin.pcx'  , 'png' , '#000000', 0.66 ) ,
#   models_t( r'in\models\objects\black'                , 'tris.md2' , 'skin.pcx'  , 'png' , '#000000', 0.66 ) ,
#   models_t( r'in\models\objects\satellite'            , 'tris.md2' , 'skin.pcx'  , 'png' , '#000000', 0.66 ) ,
#   models_t( r'in\models\objects\bomb'                 , 'tris.md2' , 'skin.pcx'  , 'png' , '#000000', 0.66 ) ,

    models_t( r'in\models\objects\debris1'              , 'tris.md2' , 'skin.pcx'  , 'png' , '#222222', 1.00 ) ,
    models_t( r'in\models\objects\debris2'              , 'tris.md2' , 'skin.pcx'  , 'png' , '#222222', 1.00 ) ,
    models_t( r'in\models\objects\debris3'              , 'tris.md2' , 'skin.pcx'  , 'png' , '#222222', 1.00 ) ,

    models_t( r'in\models\objects\gibs\arm'             , 'tris.md2' , 'skin.pcx'  , 'png' , '#222222', 1.00 ) ,
    models_t( r'in\models\objects\gibs\bone2'           , 'tris.md2' , 'skin.pcx'  , 'png' , '#222222', 1.00 ) ,
    models_t( r'in\models\objects\gibs\bone'            , 'tris.md2' , 'skin.pcx'  , 'png' , '#222222', 1.00 ) ,
    models_t( r'in\models\objects\gibs\chest'           , 'tris.md2' , 'skin.pcx'  , 'png' , '#222222', 1.00 ) ,
    models_t( r'in\models\objects\gibs\gear'            , 'tris.md2' , 'skin.pcx'  , 'png' , '#222222', 1.00 ) ,
    models_t( r'in\models\objects\gibs\head2'           , 'tris.md2' , 'player.pcx', 'png' , '#222222', 1.00 ) ,
    models_t( r'in\models\objects\gibs\head2'           , 'tris.md2' , 'skin.pcx'  , 'png' , '#222222', 1.00 ) ,
    models_t( r'in\models\objects\gibs\head'            , 'tris.md2' , 'skin.pcx'  , 'png' , '#222222', 1.00 ) ,
    models_t( r'in\models\objects\gibs\leg'             , 'tris.md2' , 'skin.pcx'  , 'png' , '#222222', 1.00 ) ,
    models_t( r'in\models\objects\gibs\skull'           , 'tris.md2' , 'skin.pcx'  , 'png' , '#222222', 1.00 ) ,
    models_t( r'in\models\objects\gibs\sm_meat'         , 'tris.md2' , 'skin.pcx'  , 'png' , '#222222', 1.00 ) ,
    models_t( r'in\models\objects\gibs\sm_metal'        , 'tris.md2' , 'skin.pcx'  , 'png' , '#222222', 1.00 ) ,

    models_t( r'in\models\items\quaddama'               , 'tris.md2' , 'skin.pcx'  , 'png' , '#4488cc', 0.66 ) ,
    models_t( r'in\models\items\invulner'               , 'tris.md2' , 'skin.pcx'  , 'png' , '#8844cc', 0.66 ) ,

    models_t( r'in\models\items\mega_h'                 , 'tris.md2' , 'skin.pcx'  , 'png' , '#ffffff', 0.66 ) ,
    models_t( r'in\models\items\healing\large'          , 'tris.md2' , 'skin.pcx'  , 'png' , '#888888', 0.66 ) ,
    models_t( r'in\models\items\healing\medium'         , 'tris.md2' , 'skin.pcx'  , 'png' , '#444444', 0.66 ) ,
    models_t( r'in\models\items\healing\stimpack'       , 'tris.md2' , 'skin.pcx'  , 'png' , '#444444', 0.33 ) ,
    models_t( r'in\models\items\adrenal'                , 'tris.md2' , 'skin.pcx'  , 'png' , '#444444', 0.33 ) ,

    models_t( r'in\models\items\armor\shard'            , 'tris.md2' , 'skin.pcx'  , 'png' , '#880000', 0.33 ) ,
    models_t( r'in\models\items\armor\jacket'           , 'tris.md2' , 'skin.pcx'  , 'png' , '#008800', 0.33 ) ,
    models_t( r'in\models\items\armor\combat'           , 'tris.md2' , 'skin.pcx'  , 'png' , '#ffff00', 0.33 ) ,
    models_t( r'in\models\items\armor\body'             , 'tris.md2' , 'skin.pcx'  , 'png' , '#ff0000', 0.66 ) ,
    models_t( r'in\models\items\armor\shield'           , 'tris.md2' , 'skin.pcx'  , 'png' , '#008800', 0.33 ) ,
    models_t( r'in\models\items\armor\screen'           , 'tris.md2' , 'skin.pcx'  , 'png' , '#008800', 0.33 ) ,
#   models_t( r'in\models\items\armor\effect'           , 'tris.md2' , 'skin.pcx'  , 'png' , '#008800', 0.33 ) ,

    models_t( r'in\models\items\pack'                   , 'tris.md2' , 'skin.pcx'  , 'png' , '#004400', 0.33 ) ,
    models_t( r'in\models\items\band'                   , 'tris.md2' , 'skin.pcx'  , 'png' , '#004400', 0.33 ) ,
    models_t( r'in\models\items\silencer'               , 'tris.md2' , 'skin.pcx'  , 'png' , '#444444', 0.33 ) ,
    models_t( r'in\models\items\breather'               , 'tris.md2' , 'skin.pcx'  , 'png' , '#444444', 0.33 ) ,
    models_t( r'in\models\items\enviro'                 , 'tris.md2' , 'skin.pcx'  , 'png' , '#444444', 0.33 ) ,
#   models_t( r'in\models\items\c_head'                 , 'tris.md2' , 'skin.pcx'  , 'png' , '#444444', 0.33 ) ,

#   models_t( r'in\models\items\keys\target'            , 'tris.md2' , 'skin.pcx'  , 'png' , '#444444', 1.00 ) ,
#   models_t( r'in\models\items\keys\spinner'           , 'tris.md2' , 'skin.pcx'  , 'png' , '#444444', 1.00 ) ,
#   models_t( r'in\models\items\keys\pyramid'           , 'tris.md2' , 'skin.pcx'  , 'png' , '#444444', 1.00 ) ,
#   models_t( r'in\models\items\keys\power'             , 'tris.md2' , 'skin.pcx'  , 'png' , '#444444', 1.00 ) ,
#   models_t( r'in\models\items\keys\pass'              , 'tris.md2' , 'skin.pcx'  , 'png' , '#444444', 1.00 ) ,
#   models_t( r'in\models\items\keys\key'               , 'tris.md2' , 'skin.pcx'  , 'png' , '#444444', 1.00 ) ,
#   models_t( r'in\models\items\keys\data_cd'           , 'tris.md2' , 'skin.pcx'  , 'png' , '#444444', 1.00 ) ,
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
            self.pak_file.write(struct.Struct('<56s').pack(e.filename.encode('ascii')))
            self.pak_file.write(struct.Struct('<l'  ).pack(e.offset))
            self.pak_file.write(struct.Struct('<l'  ).pack(e.length))
            self.table_size += 64
        self.pak_file.seek(0)
        self.pak_file.write(struct.Struct('<4s2l').pack(b'PACK', self.pointer, self.table_size))
        self.pak_file.close()

def mono_color_blend(im, color, val):
    if val == '1.00':
        return Image.new(im.mode, (im.width, im.height), color)
    if im.format in ('PCX', 'WAL'):
        mono = Image.new('RGBA', (im.width, im.height), color)
        return Image.blend(im.convert('RGBA'), mono, val)
    else:
        mono = Image.new(im.mode, (im.width, im.height), color)
        return Image.blend(im, mono, val)

script_path = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(script_path)
os.system('cls')

colormap = Image.open(f'{script_path}\in\\pics\\colormap.pcx', formats = ('PCX',))
colormap.format == 'PCX'

if os.path.exists(pak_name):
    print(f'Exist')

pak = Pak_Make(pak_name, 'in')
print(f'Making... : {pak_name}')

for m in models:

    im = Image.open(f'{script_path}\\{m.dir}\\{m.skin}', formats = ('PCX',))
    im.format == 'PCX'
    im.putpalette(colormap.palette)
    
    clr = ImageColor.getcolor(m.color, "RGB")
    im1 = mono_color_blend(im, clr, m.blend)

    with io.BytesIO() as f:
        im1.save(f, m.format)
        fn = f'{m.dir}\\{m.skin}'.replace('.pcx', f'.{m.format}')
        pak.add_file(fn, f)

    if not m.mdl == None:
        with open(f'{script_path}\\{m.dir}\\{m.mdl}', 'rb') as f:
            pak.add_file(f'{m.dir}\\{m.mdl}', f)

pak.finalize()

print(f'Ready !')
