import sys, os
import re
from decimal import Decimal as D
from collections import namedtuple

PATH_HOME = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(PATH_HOME)
os.system('cls')

skip_vars_pfx = {
    'ui_',
    'r_lastvalidrenderer'
}
skip_flags = {'R', 'I', 'C', }

isnum = re.compile(r'-?[\d\.]+f?')

def remove_exp(d):
    return d.quantize(D(1)) if d == d.to_integral() else d.normalize()

def str_to_dec(s):
    ss = s.strip('"').strip().lower()
    dot = ss.count('.')
    if (0 <= dot <= 1) and isnum.fullmatch(ss):
        ss = ss.rstrip('f')
        if D(ss) == D('0'):
            ss = '0'
        elif dot == 1:
            ss = ss.lstrip('0').rstrip('0').rstrip('.')
        else:
            ss = ss.lstrip('0')
        return remove_exp(D(ss))
    return s

def split(s, n, c = ' '):
    return tuple(map(str.strip, s.strip().split(c, n)))

cvar = namedtuple('cvar', 'value, flags')

def get_defaults(cvars_console_dump):
    cvars = {}
    with open(f'{PATH_HOME}\\{cvars_console_dump}') as f:
        con_dump = f.readlines()
        for ln in con_dump:
            flags = set(ln[:7].split())
            name, value = split(ln[8:], 1)
            if value.strip('"').startswith('0x'):
                value  = value.lower()
            value = str_to_dec(value)
            name = name.lower()
            cvars[name] = cvar(value, flags)
    return cvars

wsp = re.compile(r'\s+')

def remove_default_values_from_cfg(def_fname, cfg, cfg_out):

    cvars = get_defaults(def_fname)
    with open(f'{PATH_HOME}\\{cfg}') as f:
        cfg_lines = f.readlines()

    cfg_cvars = {}
    cvar_maxln = 0
    cfg_binds = {}
    bind_maxln = 0

    with open(f'{PATH_HOME}\\{cfg_out}', 'w') as f:
        for ln in cfg_lines:

            # ln = wsp.sub(' ', ln.strip())
            ln = ln.strip()

            match tuple(map(str.strip, ln.split(' ', 1))):

                case 'set'|'seta', val:
                    name, value = split(val, 1)
                    name_ = name.lower()

                    if value.strip('"').startswith('0x'):
                        value  = value.lower()

                    value = str_to_dec(value)

                    if any(map(name_.startswith, skip_vars_pfx)):
                        continue

                    if name_ in cvars:
                        default = cvars[name_]

                        if default.flags & skip_flags:
                            continue

                        if default.value == value:
                            continue

                        cfg_cvars[name] = value
                        if cvar_maxln < len(name):
                            cvar_maxln = len(name)

                        continue

                case 'bind', val:
                    key, value = split(val, 1)

                    cfg_binds[value] = key
                    if bind_maxln < len(key):
                        bind_maxln = len(key)

                    continue

                case _ :
                    pass

            f.write(ln + '\n')

        cfg_binds = dict(sorted(cfg_binds.items(), key=lambda x: x[0].strip('"')))
        cfg_cvars = dict(sorted(cfg_cvars.items(), key=lambda x: x[0]))

        for v, k in cfg_binds.items():
            if not ';' in v:
                v = ' ' + v.strip('"')
            f.write(f'bind {k:{bind_maxln}s} {v}\n')

        for n, v in cfg_cvars.items():
            v = str(v)
            if not ' ' in v and v != '""':
                v = ' ' + v.strip('"')
            f.write(f'seta {n:{cvar_maxln}s} {v}\n')


remove_default_values_from_cfg('defaults_q3.txt', 'q3config.cfg', 'q3config.cfg')

remove_default_values_from_cfg('defaults_ql.txt', 'qzconfig.cfg', 'qzconfig.cfg')
remove_default_values_from_cfg('defaults_ql.txt', 'repconfig.cfg', 'repconfig.cfg')

print('ok')