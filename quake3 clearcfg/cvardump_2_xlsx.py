# ----------------------------------------------------------------------------
required_libs = {
    # import: install,
    'xlsxwriter': 'xlsxwriter',
}
# ----------------------------------------------------------------------------
def install_req_libs(req_libs):
    import subprocess, sys, os
    upgr = True
    pipcmd = '-m pip install --trusted-host=pypi.org --trusted-host=pypi.python.org --trusted-host=files.pythonhosted.org'
    for imp, inst in req_libs.items():
        try:
            __import__(imp)
        except (ModuleNotFoundError, ImportError):
            try:
                if upgr:
                    subprocess.check_call([sys.executable,  f'{pipcmd} --upgrade pip'])
                    upgr = False
                subprocess.check_call([sys.executable, f'{pipcmd} {inst}'])
            except:
                print(f'Need to install librarys: {req_libs.keys()}')
                os.system('pause')
                exit()

install_req_libs(required_libs)
# ----------------------------------------------------------------------------

import sys, os
import xlsxwriter
from xlsxwriter.utility import xl_col_to_name

PATH_HOME = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(PATH_HOME)

for fname in ('defaults_q3', 'defaults_ql'):

    with open(f'{fname}.txt') as f:
        con_dump = f.readlines()

    with xlsxwriter.Workbook(f'{fname}.xlsx') as wb:
        sh = wb.add_worksheet('Sheet1')
        sh.freeze_panes(1, 0)

        hdr = {
            'S'     : ( 5, None, None, None, ''           ),
            'U'     : ( 5, None, None, None, ''           ),
            'R'     : ( 5, None, None, None, 'x == Blanks'),
            'I'     : ( 5, None, None, None, 'x == Blanks'),
            'A'     : ( 5, None, None, None, ''           ),
            'L'     : ( 5, None, None, None, ''           ),
            'C'     : ( 5, None, None, None, 'x == Blanks'),
            'T'     : ( 5, None, None, None, ''           ),
            'pfx'   : (10, None, None, None, ''           ),
            'var'   : (25, None, None, None, ''           ),
            'val'   : (50, None, None, None, ''           ),
        }
        leters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        if fname == 'defaults_q3':
            hdr.pop('T')

        c = xl_col_to_name(len(hdr)-1)
        w = len(con_dump)+1
        sh.autofilter(f'A1:{c}{w}')

        row = 0
        for col, txt in enumerate(hdr):
            c = xl_col_to_name(col)
            colwidth, celfmt, colfmt, colopt, filt = hdr[txt]
            sh.set_column(f'{c}:{c}', colwidth, colfmt, colopt)
            sh.write(row, col, txt, celfmt)
            if filt:
                sh.filter_column(c, filt)

        i = len(hdr)-3

        for ln in con_dump:
            row += 1

            flags = list(ln[0:i])
            name, value = ln[i+1:].strip().split(' ', 1)

            pfx = f"{name.split('_', 1)[0]}_" if '_' in name else ''

            if not ' ' in value and value != '""':
                value = value.strip('"')

            value = f' {value}'

            cvar = flags + [pfx, name, value]

            for col, val in enumerate(cvar):
                sh.write(row, col, val, None)
