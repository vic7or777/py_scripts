# ----------------------------------------------------------------------------
required_libs = {
    'xlsxwriter',
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

from collections import namedtuple
import sys, os
import xlsxwriter

PATH_HOME = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(PATH_HOME)

with open(f'{PATH_HOME}\\defaults.ql') as f:
   con_dump = f.readlines()

with xlsxwriter.Workbook('ql_defaults.xlsx') as wb:
    sh = wb.add_worksheet('Sheet1')
    sh.freeze_panes(1, 0)

    hdr = {
        'S'     : ( 5, None, None, None),
        'U'     : ( 5, None, None, None),
        'R'     : ( 5, None, None, None),
        'I'     : ( 5, None, None, None),
        'A'     : ( 5, None, None, None),
        'L'     : ( 5, None, None, None),
        'C'     : ( 5, None, None, None),
        'T'     : ( 5, None, None, None),
        'pfx'   : (10, None, None, None),
        'var'   : (25, None, None, None),
        'val'   : (50, None, None, None),
    }
    leters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    row = 0
    for col, key in enumerate(hdr, 0):
        c = leters[col]
        cfg = hdr[key]
        sh.set_column(f'{c}:{c}', cfg[0], cfg[2], cfg[3])
        sh.write(row, col, key, cfg[1])
            
    for ln in con_dump:
        row += 1

        flags = list(ln[0:8])

        name, value = ln[9:].strip().split(' ', 1)

        pfx = f"{name.split('_', 1)[0]}_" if '_' in name else ''

        if not ' ' in value and value != '""':
            value = ' ' + value.strip('"')

        cvar = flags + [pfx,] + [name, value]

        for col, val in enumerate(cvar):
            sh.write(row, col, val, None)
