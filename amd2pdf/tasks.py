import fileinput
import functools
import json
import os
import re
import sys
import traceback
from bisect import bisect
from io import StringIO

import jinja2
import markdown
from jinja2 import DictLoader

from .toc_handler import proc_toc


__PATH = os.path.dirname(__file__)
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
    _input = ''.join(fileinput.input(files=('-',)))
    ret = wrap_int({'wrap_input':_input, 'CSS_FILENAME': ['rsrc', 'style.css']})
    print(ret)


def wrap_int(input_dict):
    _css_fname = input_dict['CSS_FILENAME']
    if isinstance(_css_fname, list):
        _css_fname = [__PATH] + _css_fname
        _css_fname = os.path.join(*_css_fname)

    data = {
        'CSS': fixcss(fileread(_css_fname)),
        'title': os.environ.get('TITLE', ''),
        'head': os.environ.get('HEAD', ''),
        'body': input_dict['wrap_input'],
    }
    output = render_template('template.html', **data)
    return output



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
    _input = os.linesep.join(fileinput.input(files=(sys.argv[1],)))
    ret = gettoc_int(_input)
    print(repr(ret))


def gettoc_int(_input):
    found = []
    linecnt = 1
    for line in _input.splitlines():
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
        #print('found:', found[-1], file=sys.stderr)

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
    #print('-->', repr(found), file=sys.stderr)
    found = [y for x, y in found]
    #print('-->', repr(found), file=sys.stderr)
    return found


def htmlpatch():
    replacements = os.linesep.join(fileinput.input(files=(sys.argv[1],)))
    _input = os.linesep.join(fileinput.input(files=('-',)))
    ret = htmlpatch_int(_input, replacements)
    print(ret)


def htmlpatch_int(_input, _replacements_json):
    replacements = json.loads(_replacements_json)
    lines = 0
    output = StringIO()
    for line in _input.splitlines():
        while replacements and (TAG in line):
            line_left, line_right = line.split(TAG, 1)
            line = line_left + str(replacements.pop(0)) + line_right
        try:
            output.write(line)
        except:
            print('line: %r'%line, file=sys.stderr)
            print(len(line), file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            raise
        lines += 1
    _output = output.getvalue()
    return _output


def toc_to_dummy():
    _input = ''.join(fileinput.input(files=('-',)))
    ret = toc_to_dummy_int(_input)
    print(ret)


def toc_to_dummy_int(input):
    output = proc_toc(input).decode('utf-8')
    return output


def md2html():
    _input = ''.join(fileinput.input(files=('-',)))
    ret = md2htmlint(_input)
    print(ret)


def md2htmlint(input):
    output = markdown.markdown(input, extensions=['toc'])
    return output


if __name__ == "__main__":
    pass
