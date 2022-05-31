import os
import sys
import time
from functools import reduce
from subprocess import run


mods_path = os.path.dirname(os.path.abspath(__file__))
rsrc_path = os.path.join(mods_path, 'rsrc')

default_style = os.path.join(rsrc_path, 'style.css')


isWin = sys.platform == "win32"
ShouldWrap = lambda filename: isWin and (' ' in filename)
W = lambda filename: '"%s"' % filename if ShouldWrap(filename) else filename


def reduce_deps(deps):
    def R(value, element):
        return value + list(element['targets'])
    return reduce(R, deps, [])


def check_version_wkhtmltopdf(output):
    URL = 'https://github.com/wkhtmltopdf/wkhtmltopdf/releases'
    print(repr(output))
    if b'(with patched qt)' not in output:
        for _ in range(5):
            print("WARNING: WKHTMLTOPDF with PATCHED QT is required! Try: "+URL,
                  file=sys.stderr)
            time.sleep(1)


def check_versions(verbose=False):
    cmds = {
        'wkhtmltopdf': 'wkhtmltopdf -V',
        'pdftohtml': 'pdftohtml -v',
        # 'node': 'node -v',
        'python': sys.executable +' --version'
    }
    checks = {'wkhtmltopdf': check_version_wkhtmltopdf}
    for k, v in cmds.items():
        p = run(v, shell=True, capture_output=True)
        output = p.stdout+os.linesep.encode('ascii')+p.stderr
        out = [line for line in output.splitlines() if len(line.strip()) ]
        if verbose:
            print('Using %s version: "%s"' % (k, out[0].decode('utf-8')),
                  file=sys.stderr)
        if k in checks:
            checks[k](b'\n'.join(out))
        if p.returncode != 0:
            raise Exception("Tool not found: %s (%s)" % (k, v))
