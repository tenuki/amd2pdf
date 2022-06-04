import sys

import doit

from .cli import check_param, check_bool_param

from .core import Config, task_md2pdf
from .helpers import check_versions
from .tasks import wrap, gettoc, htmlpatch, toc_to_dummy, md2html


def run(filename, **kw):
    check_versions(kw.get('verbose', False))
    cfg = Config(filename, **kw)
    with cfg.prepare(task_md2pdf) as locals:
        sys.argv = [sys.argv[0]]
        doit.run(locals)


def usage():
    print("amd2pdf [-v] [-d] [-O] [-c/--css filename.css] "
          "[-p/--page PAGE-TYPE] [-t/--title title] [-o/--output filename] "
          "input_filename.md")
    print(" -v: set verbose mode on")
    print(" -d: set debug mode on")
    print(" -O: open output in browser")
    print(" -t title: set document title")
    print(" -o filename: set output filename")
    print(" -c/--css filename.css: stylesheet to use, default: style.css")
    print(" -p/--page PAGE-TYPE: Default A4")
    print("")
    print("Output will be: input_filename.pdf")


def main():
    if len(sys.argv) >= 2:
        params = {}
        args = [arg for arg in sys.argv[1:]]
        unmatched = []
        skip = False
        for idx, arg in enumerate(args):
            if skip:
                skip = False
                continue
            for f in [
                check_bool_param('-O', '--autoopen', 'autoopen'),
                check_bool_param('-v', '--verbose', 'verbose'),
                check_bool_param('-d', '--debug', 'debug'),
                check_param('-c', '--css', 'css'),
                check_param('-p', '--page', 'page'),
                check_param('-t', '--title', 'title'),
                check_param('-o', '--output', 'output_filename'),
            ]:
                _break, _skip = f(idx, args, params)
                if _break:
                    skip = _skip
                    break
            if skip or _break:
                continue
            unmatched.append(arg)

        if len(unmatched) < 1:
            usage()
            print("No input filename specified!")
        elif len(unmatched) > 1:
            usage()
            print("Unknown parameters:", unmatched[1:])
        else:
            run(unmatched[0], **params)
    else:
        usage()

