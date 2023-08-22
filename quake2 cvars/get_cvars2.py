if __name__ != '__main__': exit()
# ----------------------------------------------------------------------------
required_libs = {
    'regex',
}
# ----------------------------------------------------------------------------
def install_lib(required):
    import sys, os
    from subprocess import check_call
    from pkg_resources import working_set
    installed = {pkg.key for pkg in working_set}
    missing = required - installed
    if missing:
        try:
            check_call([sys.executable, '-m', 'pip', 'install', *missing])
        except:
            print(f'Need to install library: {list(missing)}')
            os.system('pause')
            exit()
install_lib(required_libs)
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

script_path = op.abspath(script_path)
run_path = op.dirname(script_path)

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
# yamagi-8.20
    'DEFAULT_OPENGL_DRIVER': 'opengl32',
    'DEFAULT_OPENAL_DRIVER': 'openal32.dll',
}

vals = {
    'allow_download': '1',          # quake2
    'm_fixaccel': '1',              # r1q2
    # 'gl_alphabits': '8',
    # 'gl_colorbits': '24',
    # 'gl_depthbits': '24',
    # 'gl_stencilbits': '8',
    'com_time_format': '%H.%M',     # q2pro
    'net_enable_ipv6': '1',         # q2pro r1504
    'gl_shaders': '1',              # q2pro r2765
    's_sdldriver': 'directsound',   # yamagi-8.20
}

skip_vals = {
# quake2
    'game',
    'gamename',
    'gamedate',
    'qport',
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
}

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
re_cvar = re.compile( r'(?:cvar.get|gi.cvar|ri.cvar)\s*\(\s*("[\s\S]*?)\)+\s*[;,-]', flags=re.IGNORECASE)

# Cvar_Get(va("adr%i",i) ...) -> adr0 .. adr15
re_q2pro_adr = re.compile( r'Cvar_Get\(\s*va\(\s*"adr%i", i\s*\)' )

def Cvar_Get(zip_arch):
    with ZipFile(zip_arch) as zf:
        for file in zf.namelist():

            if not file.endswith('.c'):
                continue

            if op.basename(file) in ('cvar.c',):
                continue

            folder = op.basename(op.dirname(file))
            if folder in ('irix','linux','solaris', 'unix', 'video'):
                continue

            with zf.open(file, 'r') as f:
                txt = f.read().decode('cp1252')

                txt = re_ltsp.sub(r'\n', txt)

                txt = re_com1.sub(r''  , txt)
                txt = re_com2.sub(r'\n', txt)
                txt = re_com3.sub(r''  , txt)

                if re_q2pro_adr.search(txt):
                    for i in range(15):
                        yield folder, f'adr{i}, "", CVAR_ARCHIVE'

                txt = re_unmacro1.sub(r'\1', txt)
                txt = re_unmacro2.sub(r'\1', txt)
                txt = re_unmacro3.sub(r''  , txt)

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


zip_list = glob(f'src/*.zip')

for src_arch in (zip_list):

    src_name = src_arch.rsplit('.', 1)[0].replace('-src','').rsplit('\\', 1)[1]

    cvars = {}
    for folder, cvar in Cvar_Get(src_arch):

        v1, v2, v3 = str2cvar(cvar)

        if v1 in skip_vals:
            continue

        if v1 in vals:
            v2 = vals[v1]

        if v2 in consts:
            v2 = consts[v2]

        if not folder in cvars:
            cvars[folder] = dict()
        cvars[folder][v1] = (v2,v3)

        max_cv, max_vl = get_max_ln(cvars)

        for k in cvars:
            cvars[k] = dict(sorted(cvars[k].items(), key=lambda x: x[0]))


    with open(f'{src_name}.txt', 'w') as f:
        for K, V in cvars.items():
            f.write(f'\n// {K}\n\n')
            for k, v in V.items():
                v1, v2, v3 = k, v[0], v[1]

                v1 = f'{v1:{max_cv}s}'

                if v3 == '0':
                    f.write(f'  set {v1} {v2}\n')
                else:
                    v3 = list(map(str.strip, v3.split('|')))
                    v3 = sorted(v3)
                    skip = cheat = False
                    for atr in v3:
                        match atr:
                            case 'NOSET' | 'ROM' | 'USER_CREATED':
                                skip = True
                            case 'CHEAT':
                                cheat = True
                    if skip:
                        continue

                    match option:
                        case '1':
                            v2 = f'{v2:{max_vl}s}'
                            v3 = ' | '.join(v3)
                            f.write(f'{"//" if cheat else "  "}set {v1} {v2} // {v3}\n')
                        case _:
                            f.write(f'{"//" if cheat else "  "}set {v1} {v2}\n')
print(' ok')
