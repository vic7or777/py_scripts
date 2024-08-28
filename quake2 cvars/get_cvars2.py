if __name__ != '__main__': exit()
# ----------------------------------------------------------------------------
req_libs = {
    'regex': 'regex',
}
# ----------------------------------------------------------------------------
def install_req_libs(req_libs):
    import subprocess, sys, os
    upgr = True
    run_pip = '-Xfrozen_modules=off -m pip'
    fix_ssl = 'config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org" \
--trusted-host=pypi.python.org --trusted-host=pypi.org --trusted-host=files.pythonhosted.org'

    for imp, inst in req_libs.items():
        try:
            __import__(imp)
        except (ModuleNotFoundError, ImportError):
            try:
                if upgr:
                    subprocess.check_call([sys.executable, f'{run_pip} {fix_ssl}'])
                    subprocess.check_call([sys.executable, f'{run_pip} install --upgrade pip'])
                    upgr = False
                subprocess.check_call([sys.executable, f'{run_pip} install {inst}'])
            except:
                print(f'Need to install librarys: {req_libs.keys()}')
                os.system('pause')
                exit()

install_req_libs(req_libs)
# ----------------------------------------------------------------------------

import sys, os, os.path as op
# import re
import regex as re
from glob import glob
from zipfile import ZipFile


option = '0'
match sys.argv:
    case script_path, option:
        pass
    case script_path, *_:
        pass

script_name = op.basename(script_path)
script_path = op.abspath(script_path)
run_path = op.dirname(script_path)

os.system('cls')
print(sys.version)

print(f'''
This script make things:
- Scan sources in src/*.zip
- Generate a default config for each source archive

Run options:
    "{script_name}"         - list of cvars
    "{script_name} 1"       - list of cvars (with attributes)
    "{script_name} 2"       - list of cvars (no commented and no set)
    "{script_name} 3"       - flat list of cvars
    "{script_name} 4"       - flat list of cvars (no commented and no set)
''')

print(' go')
os.chdir(run_path)

consts = {
# quake2
    'DF_INSTANT_ITEMS': '16',
    'MAXSTACKSURFACES': 'x',
# aprq2
    'GL_DRIVERNAME': 'opengl32',
    'AL_DRIVERNAME': 'openal32',
    'PORT_CLIENT': '27901',
# q2pro r179
    'DEFAULT_INPUT_DRIVER': '""',
    'COM_LOGFILE_NAME': 'console.log',
    'PORT_SERVER': '27910',
    'PORT_ANY': '-1',
    'port': '-1',
    'NUMSTACKEDGES': '3000',
    'NUMSTACKSURFACES': '1000',
    'DEFAULT_REFRESH_DRIVER': 'gl',
# q2pro r364
    'PORT_SERVER_STRING': '27910',
    'PORT_ANY_STRING': '-1',
    'UF_LOCALFOV': '4',
    'VID_GEOMETRY': '640x480',
    'VID_MODELIST': '640x480 800x600 1024x768',
# q2pro r1504
    'MAX_PACKETLEN_WRITABLE_DEFAULT': '1390',
    'modelist': 'desktop 640x480 800x600 1024x768',
    'LIBGL': 'opengl32',
    'LIBAL': 'openal32',
    'NET_EnableIP6': '1',
# q2pro r2765
    'MAX_PACKET_ENTITIES': '128',
# q2pro r3290
    'HISTORY_SIZE': '128',
    'R_TEXTURE_FORMATS': 'png jpg tga',
# q2pro r3470
    'DEFGLPROFILE': '""',
# yamagi-8.20
    'DEFAULT_OPENGL_DRIVER': 'opengl32',
    'DEFAULT_OPENAL_DRIVER': 'openal32.dll',
}

vals = {
    'allow_download': '0',          # quake2
    'm_fixaccel': '1',              # r1q2
    # 'gl_alphabits': '8',
    # 'gl_colorbits': '24',
    # 'gl_depthbits': '24',
    # 'gl_stencilbits': '8',
    'com_time_format': '%H.%M',     # q2pro
    'net_enable_ipv6': '1',         # q2pro r1504
    'gl_shaders': '1',              # q2pro r2765
    'sv_allow_map': '0',            # q2pro r3470
    's_sdldriver': 'directsound',   # yamagi-8.20
}

skip_vars = {
# quake2
    'game',
    'gamename',
    'gamedate',
    'qport',
# r1q2
    'sys_fpu_bits',
    'cl_player_updates',
    'dbg_framesleep',
# q2pro r179
    'in_device',
    'snddevice',
# q2pro r364
    'sv_features',
    'net_tcp_ip',
    'net_tcp_port',
    's_device',
# yamagi-8.20
    'cl_libcurl',
# *_test*
    'cl_test',
    'cl_test2',
    'cl_test3',
    'cl_testblend',
    'cl_testentities',
    'cl_testlights',
    'cl_testparticles',
    'gl_r1gl_test',
    'gl_test',
    's_testsound',
}

skip_vars_prefix = {
    'cl_stereo',
    'joy_',
    'dbg_',
}

skip_folders = (
    # 'ctf',
    'unix',
    'linux',
    'irix',
    'solaris',
    'video',
)

order = (
    'game', 'baseq2', 'savegame', 'ctf',
    'server', 'net', 'mvd',
    'client', 'input',
    'vid', 'refresh',
    'ref_gl', 'gl', 'sdl', 'gl1', 'gl3',
    'ref_soft', 'soft', 'sw',
    'sound', 'qal',
    'win32', 'windows',
    'unix', 'linux', 'solaris', 'irix',
    'qcommon', 'common',
    'video',
    'menu', 'ui',
)

# '... /* comment */ ...'
re_com1 = re.compile( r'(?:\/\*)[\s\S]*?(?:\*\/)' ) 

# # '... // comment   \n   ...'
# re_com2 = re.compile( r'(\s*\/\/.*?\n\s*)'      )

# https://stackoverflow.com/questions/70064025/regex-pattern-to-match-comments-but-not-urls
# https://stackoverflow.com/questions/20089922/python-regex-engine-look-behind-requires-fixed-width-pattern-error
# '... // comment   \n   ...' but not '...http://...'
re_com2 = re.compile( r'(?<=^|[^\S])\/\/.*\n\s*'  )

# '# text \n...'
re_com3 = re.compile( r'\n(#.*)'                  )

re_sep1 = re.compile(  r'\s*,\s*'    )  # ' , '
re_sep2 = re.compile(  r'"\s*\n\s*"' )  # '" \n "'
re_ltsp = re.compile(  r'\n\s+'      )  # '\n    '

# va("...",text) -> text
re_unmacro1 = re.compile( r'va\s*\(\s*".*?"\s*,(.*?)\)' )

# STRINGIFY(text) -> text
# STRINGER(text) -> text
re_unmacro2 = re.compile( r'(?:STRINGIFY|STRINGER)\((.*?)\)'         )

# 'NET_EnableIP6()' -> 'NET_EnableIP6'
re_unmacro3 = re.compile( r'\(\)'                       )

# Cvar_Get(text) -> text
re_cvar = re.compile( r'(?:cvar.get|gi.cvar)\s*\(\s*("[\s\S]*?)\)+\s*[;,-]', flags=re.IGNORECASE)

# Cvar_Get(va("adr%i",i) ...) -> adr0 .. adr15
re_q2pro_adr = re.compile( r'Cvar_Get\(\s*va\(\s*"adr%i", i\s*\)' )
re_yq2_adr = re.compile( r'Cvar_Get\(buffer, "", CVAR_ARCHIVE\);' )

# find table of cheat cvars (quake2 / r1q2 / yamagi)
# cheatvars[] = {text};
re_cheat_table = re.compile(r'cheatvars\[\] = \{([\s\S]+?)\};', flags=re.IGNORECASE)
# {"text", 0, 0, NULL},
re_cheat_vars = re.compile(r'\{\s*"(.+?)"\s*,.*?\}', flags=re.IGNORECASE)

def Cheat_Cvars_Get(zip_arch):
    with ZipFile(zip_arch) as zf:
        for file in zf.namelist():

            src_file = op.basename(file)
            if not src_file.endswith('.c'):
                continue
            
            with zf.open(file, 'r') as f:
                txt = f.read().decode('cp1252')
                tab = re_cheat_table.findall(txt)
                for t in tab:
                    for c in re_cheat_vars.findall(t):
                        yield c

def Cvars_Get(zip_arch):
    with ZipFile(zip_arch) as zf:
        for file in zf.namelist():

            src_file = op.basename(file)
            if not src_file.endswith('.c'):
                continue
            if src_file in ('cvar.c',):
                continue

            folder = op.basename(op.dirname(file))
            if folder in skip_folders:
                continue

            with zf.open(file, 'r') as f:
                txt = f.read().decode('cp1252')

                txt = re_ltsp.sub(r'\n', txt)

                txt = re_com1.sub(r''  , txt)
                txt = re_com2.sub(r'\n', txt)
                txt = re_com3.sub(r''  , txt)

                adrs = 0
                if re_q2pro_adr.search(txt): adrs = 16
                elif re_yq2_adr.search(txt): adrs = 9
                if adrs:
                    for i in range(adrs):
                        yield folder, f'adr{i}, "", CVAR_ARCHIVE'

                txt = re_unmacro3.sub(r''  , txt)
                txt = re_unmacro1.sub(r'\1', txt)
                txt = re_unmacro2.sub(r'\1', txt)

                cvars = re_cvar.findall(txt)
                for cvar in cvars:
                    cvar = re_sep1.sub(', ', cvar.strip())
                    cvar = re_sep2.sub('', cvar)
                    yield folder, cvar


def str2cvar(c):
    v12, v3 = c.rsplit(',', 1)
    v1, v2 = v12.split(',',1)

    v1 = v1.strip()
    v1 = v1.strip('"')
    v2 = v2.strip()
    if not ' ' in v2 and v2 != '""':
        v2 = v2.strip('"')
    v3 = v3.strip()
    v3 = v3.replace('CVAR_','')
    return v1, v2, v3

def get_max_ln(D):
    max_cv = max_vl = 0
    for d in D.values():
        for k, v in d.items():
            if (l := len(k)) > max_cv: max_cv = l
            if (l := len(v[0])) > max_vl: max_vl = l
    if max_vl > 25: max_vl = 25
    return max_cv, max_vl

def remove_duplicates(cvars):
    for F0 in cvars:
        for c0 in cvars[F0]:
            for F1 in reversed(cvars):
                if F1 == F0:
                    break
                if c0 in cvars[F1]:
                    del cvars[F1][c0]    

def merge_parts(cvars):
    D = {"":{}}
    for v in reversed(cvars.values()):
        D[""] |= v
    return D

zip_list = glob(f'src/*.zip')

for src_arch in (zip_list):

    src_name = src_arch.rsplit('.', 1)[0].replace('-src','').rsplit('\\', 1)[1]

    cfg_path = f'{src_name}.cfg'

    if op.exists(cfg_path):
        continue

    cheat_cvars = tuple(Cheat_Cvars_Get(src_arch))

    cvars = {f:{} for f in order}

    for folder, cvar in Cvars_Get(src_arch):

        v1, v2, v3 = str2cvar(cvar)

        if v1 in skip_vars:
            continue

        if any(map(v1.startswith, skip_vars_prefix)):
            continue

        if v1 in vals:
            v2 = vals[v1]

        if v2 in consts:
            v2 = consts[v2]

        if not folder in cvars:
            cvars[folder] = dict()
        cvars[folder][v1] = (v2,v3)

    match option:
        case '3'|'4':
            cvars = merge_parts(cvars)
        case _ :
            remove_duplicates(cvars)

    max_cv, max_vl = get_max_ln(cvars)
    
    with open(cfg_path, 'w') as f:

        for K, V in cvars.items():

            if not V:
                continue

            first = True

            V = dict(sorted(V.items(), key=lambda x: x[0]))

            for k, v in V.items():
                cv, val, atr = k, v[0], v[1]

                cv_ = f'{cv:{max_cv}s}'
                val_ = f'{val:{max_vl}s}'

                skip = cheat = False

                if cv in cheat_cvars:
                    cheat = True

                if atr == '0':
                    atrs = {'CHEAT'} if cheat else set()
                else:
                    atrs = set(map(str.strip, atr.split('|')))
                    if cheat:
                        atrs.add('CHEAT')

                for a in atrs:
                    match a:
                        case 'NOSET' | 'ROM' | 'USER_CREATED':
                            skip = True
                        case 'CHEAT':
                            cheat = True

                if skip:
                    continue

                if first and K:
                    f.write(f'\n// {K}\n\n')
                    first = False

                match option:
                    case '1': atr = ' | '.join(sorted(atrs))
                    case _  : atr = 'CHEAT' if cheat else ''

                match option:
                    case '2'|'4':
                        if atr: f.write(f'  {cv_} {val_} // {atr}\n')
                        else:   f.write(f'  {cv_} {val}\n')
                    case _ :
                        if atr: f.write(f'// set {cv_} {val_} // {atr}\n')
                        else:   f.write(f'// set {cv_} {val}\n')

print(' ok')
