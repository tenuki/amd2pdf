import sys

import doit

from .core import Config, task_md2pdf
from .helpers import check_versions
from .tasks import wrap, gettoc, htmlpatch


def run(filename, **kw):
    check_versions(kw.get('verbose', False))
    cfg = Config(filename, **kw)
    with cfg.prepare(task_md2pdf) as locals:
        sys.argv = [sys.argv[0]]
        doit.run(locals)


def usage():
    print("%s [-v] [-d] [-c/--css filename.css] [-p/--page PAGE-TYPE] [-t/--title title] input_filename.md" % sys.argv[0])
    print(" -v: set verbose mode on")
    print(" -d: set debug mode on")
    print(" -t: set document title")
    print(" filename.css: stylesheet to use, default: style.css")
    print(" PAGE-TYPE: Default A4")
    print("")
    print("Output will be: input_filename.pdf")


def check_param(short, long, param):
    def f(idx, args, params):
        arg = args[idx]
        if arg.lower() in (short, long):
            try:
                value = args[idx + 1]
                params[param] = value
                return True
            except:
                raise Exception("%s/%s requires a value."%(short, long))
        return False
    return f


def main():
    debug = False
    verbose = False
    if len(sys.argv) >= 2:
        params = {}
        args = [arg for arg in sys.argv[1:]]
        unmatched = []
        skip = False
        for idx, arg in enumerate(args):
            if skip:
                skip = False
                continue
            if arg == "-v":
                verbose = True
                continue
            if arg == "-d":
                debug = True
                continue

            for f in [
                check_param('-c', '--css', 'css'),
                check_param('-p', '--page', 'page'),
                check_param('-t', '--title', 'title'),
            ]:
                if f(idx, args, params):
                    skip = True
                    break
            if skip:
                continue
            unmatched.append(arg)

        if len(unmatched) < 1:
            usage()
            print("No input filename specified!")
        elif len(unmatched) > 1:
            usage()
            print("Unknown parameters:", unmatched[1:])
        else:
            run(unmatched[0], verbose=verbose, debug=debug, **params)
    else:
        usage()

