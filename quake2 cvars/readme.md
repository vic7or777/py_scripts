# Get default cvars from zipped source code

## quake2 / r1q2 / aprq2 / q2pro / opentdm / openffa


This script make things:
- Scan sources in src/*.zip
- Generate a default configuration for each source archive.
```
    Run options:
        get_cvars2.py       - list of cvars
        get_cvars2.py 1     - list of cvars with attributes
        get_cvars2.py 2     - list of cvars (no commented and no set)
        get_cvars2.py 3     - flat list of cvars
        get_cvars2.py 4     - flat list of cvars (no commented and no set)
```