from collections import namedtuple
import sys, os

PATH_HOME = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(PATH_HOME)
os.system('cls')

cvars_console_dump = 'defaults.ql'

cvar = namedtuple('cvar', 'S,U,R,I,A,L,C,T, name, value')

with open(f'{PATH_HOME}\\{cvars_console_dump}') as f:
   con_dump = f.readlines()

cvars = []
for ln in con_dump:
    flags = ln[0:7]
    name_value = ln[8:].strip(' \n').split(' ', 1)
    name = name_value[0].strip()
    value = name_value[1].strip()
    if value.strip('"').startswith('0x'):
        value  = value.lower()

    c = cvar(
        S = 'S' in flags,
        U = 'U' in flags,
        R = 'R' in flags,
        I = 'I' in flags,
        A = 'A' in flags,
        L = 'L' in flags,
        C = 'C' in flags,
        T = 'T' in flags,
        name  = name,
        value = value
    )
    cvars.append(c)

def remve_default_values_from_cfg(cvars, cfg, cfg_out):
    with open(f'{PATH_HOME}\\{cfg}') as f:
        cfg_lines = f.readlines()
    
    cfg_cvars = []
    cvar_max_len = 0
    cfg_binds = []
    bind_max_len = 0
    with open(f'{PATH_HOME}\\{cfg_out}', 'w') as f:   
        for ln in cfg_lines:
            ln = ln.strip(' \n')
            if ln.startswith('seta '):
                name_value = ln[5:].strip().split(' ', 1)
                name = name_value[0].strip()
                value = name_value[1].strip()
                if value.strip('"').startswith('0x'):
                    value  = value.lower()
                skip = False
                deflt = False
                found = False
                for v in cvars:
                    if v.name == name:
                        found = True
                        if v.R or v.I or v.C or name.startswith('ui_'):
                            skip = True
                            break
                        if v.value == value:
                            deflt = True
                            break
                if skip or deflt:
                    continue
                elif found:
                    cfg_cvars.append((name, value))
                    if cvar_max_len < len(name):
                        cvar_max_len = len(name)
                    continue
            if ln.startswith('bind '):
                name_value = ln[5:].strip().split(' ', 1)
                name = name_value[0].strip()
                value = name_value[1].strip()
                cfg_binds.append((name, value))
                if bind_max_len < len(name):
                    bind_max_len = len(name)
                continue
            f.write(ln + '\n')

        for n, v in sorted(cfg_binds, key=lambda x: x[1].strip('"')):
            sp = bind_max_len - len(n)
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
            f.write(f'bind {n}{sp} {v}\n')

        for n, v in sorted(cfg_cvars, key=lambda x: x[0].strip('"')):
            sp = ' ' * (cvar_max_len - len(n))
            if not ' ' in v and v != '""':
                v = ' ' + v.strip('"')
            f.write(f'seta {n} {sp}{v}\n')

        
        f.close()

remve_default_values_from_cfg(cvars, 'qzconfig.cfg', 'qzconfig.cfg')
remve_default_values_from_cfg(cvars, 'repconfig.cfg', 'repconfig.cfg')