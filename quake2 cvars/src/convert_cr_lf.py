import sys, os
import os.path as op
from glob import glob

skip_ext = (
    '.aps',
    '.bce',
    '.bcp',
    '.gif',
    '.jpg',
    '.ico',
    '.iconheader',
    '.o',
    '.opt',
    '.ssv',
    '.tiff',
)

script_path = op.abspath(sys.argv[0])
script_name = op.basename(script_path)
run_path = op.dirname(script_path)

print(' go')
os.chdir(run_path)

files = glob(f'{run_path}/**/*', recursive=True)

LINEBREAK = '\n' # \r\n

for file in files:

    if op.isdir(file):
        continue

    if any(map(file.endswith, skip_ext)):
        continue

    with open(file) as f:
        s = f.read()

    with open(file, 'w') as f:
        f.write(LINEBREAK.join(s.splitlines()) + LINEBREAK)

print(' ok')
