from collections import namedtuple
import sys, os

PATH_HOME = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(PATH_HOME)
os.system('cls')

cfg1  = fr'{PATH_HOME}\qzconfig.cfg'
cfg1_ = fr'{PATH_HOME}\qzconfig.cfg'
cfg2  = fr'{PATH_HOME}\repconfig.cfg'
cfg2_ = fr'{PATH_HOME}\repconfig.cfg'
ql_defaults_cvars_console_dump_file_name = fr'{PATH_HOME}\defaults.ql'

cvar = namedtuple('cvar', 'S,U,R,I,A,L,C,T, name, value')

with open(ql_defaults_cvars_console_dump_file_name) as f:
   con_dump = f.readlines()

cvars = []
for l in con_dump:
    flags = l[0:7]
    name_value = l[8:].strip(' \n').split(' ', 1)
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
    with open(cfg) as f:
        cfg_lines = f.readlines()
    
    cfg_cvars = []
    max_str_len = 0
    with open(cfg_out, 'w') as f:
        
        for ln in cfg_lines:
            l = ln.strip(' \n')
            if not l.startswith('seta '):
                f.write(ln)
            else:
                name_value = l[5:].strip().split(' ', 1)
                name = name_value[0].strip()
                value = name_value[1].strip()
                if name.startswith('ui_'):
                    continue
                if value.strip('"').startswith('0x'):
                    value  = value.lower()
                val_pass = False
                val_def = False
                for v in cvars:
                    if v.name == name:
                        if v.R or v.I or v.C:
                            val_pass = True
                            break
                        if v.value == value:
                            val_def = True
                            break
                if val_pass or val_def:
                    continue
                else:
                    cfg_cvars.append((name, value))
                    if max_str_len < len(name):
                        max_str_len = len(name)
        
        for n, v in sorted(cfg_cvars, key=lambda x: x[0]):
            sp = ' ' * (max_str_len - len(n))
            f.write(f'seta {n} {sp}{v}\n')
        
        f.close()

remve_default_values_from_cfg(cvars, cfg1, cfg1_)
remve_default_values_from_cfg(cvars, cfg2, cfg2_)