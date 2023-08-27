from collections import namedtuple
import sys, os
import re

PATH_HOME = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(PATH_HOME)
os.system('cls')

cvars_console_dump = 'defaults.q3'

skip_vars_pfx = {
    'ui_',
}
skip_flags = {'R', 'I', 'C', }

def split(s, n, c = ' '):
    return tuple(map(str.strip, s.strip().split(c, n)))

cvar = namedtuple('cvar', 'value, flags')
nocvar = cvar('', set())
cvars = {}
with open(f'{PATH_HOME}\\{cvars_console_dump}') as f:
    con_dump = f.readlines()
    for ln in con_dump:
        flags = set(ln[:7].split())
        name, value = split(ln[8:], 1)
        if value.strip('"').startswith('0x'):
            value  = value.lower()
        name = name.lower()
        cvars[name] = cvar(value, flags)

wsp = re.compile(r'\s+')

def remve_default_values_from_cfg(cvars, cfg, cfg_out):
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
            sp = bind_maxln - len(k)
            if sp % 2:
                sr = sp // 2
                sl = sp - sr
            else:
                sl = sp // 2
                sr = sp - sl
            sp *= ' '
            sl *= ' '
            sr *= ' '
            if not ';' in v:
                v = ' ' + v.strip('"')
            f.write(f'bind {k}{sp} {v}\n')

        for n, v in cfg_cvars.items():
            sp = ' ' * (cvar_maxln - len(n))
            if not ' ' in v and v != '""':
                v = ' ' + v.strip('"')
            f.write(f'seta {n} {sp}{v}\n')

        f.close()

remve_default_values_from_cfg(cvars, 'q3config.cfg', 'q3config.cfg')

print('ok')