import fileinput
import functools
import json
import os
import re
import sys
from bisect import bisect

import jinja2
import markdown
from jinja2 import DictLoader

from .toc_handler import proc_toc

TEMPLATE_DATA = """<!DOCTYPE html><html>
<head>
<meta charset="utf-8" />
<title>{{title}}</title>
{{head}}
<style>{{CSS}}</style>
</head>
<body>
{{body}}
</body>
</html>"""


def render_template(file_name, **context):
    env = jinja2.Environment(loader=DictLoader({'template.html':
                                                TEMPLATE_DATA}))
    template = env.get_template(file_name)
    result = template.render(context)
    return result


def fileread(filename):
    with open(filename, 'r') as f:
        return f.read()


def fixcss(data):
    data = data.replace('.markdown-', '')
    data = data.replace('margin:auto;', '')
    return data


def wrap():
    print('parsing...', file=sys.stderr)
    linecnt = 0
    lines = []
    for line in fileinput.input(files=('-',)):
        lines.append(line)
        linecnt += 1
    print('checking.....', file=sys.stderr)
    print('keys:' + repr(list(os.environ.keys())), file=sys.stderr)
    data = {
        'CSS': fixcss(fileread(os.environ.get('CSS', 'style.css'))),
        'title': os.environ.get('TITLE', ''),
        'head': os.environ.get('HEAD', ''),
        'body': ''.join(lines),
    }
    sys.stdout.write(render_template('template.html', **data))
    sys.stdout.flush()
    print("CSS:"+os.environ.get('CSS', 'style.css'), file=sys.stderr)



TAG = 'iiiii'
f = lambda x: ' ?'.join(x.split())

text_left = r'<text top="([0-9]+)" left="[0-9]+" width="[0-9]+" height="[0-9]+" font="[0-9]+">'
text_right = r'</text>'

fullRE = re.compile(text_left + (r'<a href="([^"]*)">%s</a>'%f(TAG)) + text_right)
currentRE = re.compile(text_left+f(TAG)+text_right)
hash_link_to_idx = lambda link: int(link.split('#',1)[1])


def _cmp(x, y):
    return y - x


def gettoc():
    #print('type: %s  (%d)' % (type(data), len(data)), file=sys.stderr)
    # root = ET.fromstring(data)
    # for x in root.findall(".//a"):
    #     link = x.attrib.get('href')
    #     if x.text==TAG and '#' in link:
    #         #print(link, file=sys.stderr)
    #         found.append(hash_link_to_idx(link))
    found = []
    linecnt = 1
    for line in fileinput.input(files=(sys.argv[1],)):
        linecnt += 1
        line = line.strip()
        if not TAG in line: continue
        m = fullRE.search(line)
        if m:
            if '#' not in m.groups()[1]:
                continue
            idx_nr, page_nr = int(m.groups()[0]), hash_link_to_idx(m.groups()[1])  # index
        else:
            # try get a link in the same page
            m = currentRE.search(line)
            if m:
                idx_nr, page_nr = int(m.groups()[0]), None
            else:
                continue
        found.append( (idx_nr, page_nr) )
        print('found:', found[-1], file=sys.stderr)

    # fix Nones
    Nones = False
    idx_page_d = {}
    for idx_nr, page_nr in found:
        if page_nr is not None:
            idx_page_d[idx_nr] = page_nr
        else:
            Nones = True
    if Nones:  # we need to fix them..
        newfound = []
        idx_sorted = list(idx_page_d.keys())
        idx_sorted.sort()
        for idx_nr, page_nr in found:
            if page_nr is None:
                _idx = bisect(idx_sorted, idx_nr)
                if _idx>0:
                    page_nr = idx_page_d[idx_sorted[_idx-1]]
                else:
                    page_nr = 1
            newfound.append((idx_nr, page_nr))
        found = newfound

    # now sort them
    cmpfunc = lambda x, y: _cmp(x[0],y[0]) if x[0]!=y[0] else _cmp(x[1],y[1])
    found.sort(reverse=True, key=functools.cmp_to_key(cmpfunc))
    print('-->', repr(found), file=sys.stderr)
    found = [y for x, y in found]
    print('-->', repr(found), file=sys.stderr)
    print(repr(found))
    return found


def htmlpatch():
    print('opening: %s..' % sys.argv[1], file=sys.stderr)
    with open(sys.argv[1], 'r') as f:
        data = f.read()
        print('parsing: %s' % repr(data), file=sys.stderr)
        replacements = json.loads(data)
        # replacements = json.load(f)

    print('parsing...', file=sys.stderr)
    lines = 0
    for line in fileinput.input(files=('-',)):
        #print('stdin>' + line.rstrip(), file=sys.stderr)
        while replacements and (TAG in line):
            line_left, line_right = line.split(TAG, 1)
            line = line_left + str(replacements.pop(0)) + line_right
        sys.stdout.write(line)
        lines += 1

    print('parse done. repl: %r, lines: %d' % (replacements, lines),
          file=sys.stderr)


def toc_to_dummy():
    print('parsing...', file=sys.stderr)
    _lines = []
    for line in fileinput.input(files=('-',)):
        _lines.append(line)

    data = ''.join(_lines)
    result = proc_toc(data)
    sys.stdout.write(result.decode('utf-8'))
    print('parse done. repl: %r, lines: %d' % (len(data), len(result)),
          file=sys.stderr)


def md2html():
    print('parsing...', file=sys.stderr)
    _lines = []
    for line in fileinput.input(files=('-',)):
        _lines.append(line)

    data = ''.join(_lines)
    result = markdown.markdown(data, extensions=['toc'])
    sys.stdout.write(result)
    print('parse done. repl: %r, lines: %d' % (len(data), len(result)),
          file=sys.stderr)


if __name__ == "__main__":
    pass
