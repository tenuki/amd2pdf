# -*- coding: utf-8 -*-
import os
import shutil
import sys
import tempfile
import types
from contextlib import contextmanager

from doit.task import clean_targets

from .helpers import default_style, reduce_deps, ShouldWrap, isWin, W

TARGET_REF = '%(targets)s'
op_esc = lambda x: ('"%s"' % x) if not x.startswith('"') else x


class Amd2pdfException(Exception):
    pass


class ExecError(Amd2pdfException):
    pass


def GuessName(cmdline):
    parts = cmdline.split()
    if parts[0] == 'node' or ('python' in parts[0]):
        return parts[1].split('.')[0]
    return parts[0]


class Config:
    def __init__(self, source, verbose=False, debug=False, css=None, page=None,
                 title=None, output_filename=None, autoopen=False):
        self.temp_dir = tempfile.mkdtemp(prefix='md2pdf-')
        self.debug = debug
        self.verbosity_level = 2 if verbose else 0
        self.source = source
        self.autoopen = autoopen
        self.output_filename = output_filename
        self.params = {'css': css, 'page': page, 'title': title}
        self.defaults = {'css': default_style, 'page': 'A4',
                         'title': os.environ.get('TITLE', '')}

    @property
    def Final(self):
        if self.output_filename is None:
            fname = self.source.split('.')[0] + '.pdf'
        else:
            fname = self.output_filename
        fullname = os.path.join(os.getcwd(), fname)
        if not os.path.isabs(fullname):
            raise ExecError("shouldn't happen")
        return fullname

    @property
    def Initial(self):
        source = self.source
        if ShouldWrap(source):
            handle, fullname = tempfile.mkstemp(prefix='src-md',
                                                suffix='.md',
                                                dir=self.temp_dir)
            with open(source, 'rb') as src:
                data = src.read(4096)
                while data:
                    os.write(handle, data)
                    data = src.read(4096)
            os.close(handle)
            source = fullname
        return {'targets': [source]}

    def _setup_env(self):
        os.environ['TMP'] = os.environ['TEMP'] = self.temp_dir
        for key, value in self.params.items():
            os.environ[key.upper()] = value if value else self.defaults.get(key)

    def link_tasks(self, task_gen):
        prev = self.Initial
        for task in task_gen:
            if ('file_dep' not in task) or ([] == task['file_dep']):
                task['file_dep'] = reduce_deps([prev])
            yield task
            prev = task

    @contextmanager
    def prepare(self, taskgen):
        self._setup_env()
        if self.debug:
            print("Temporary files at:", self.temp_dir)
        try:
            # noinspection PyShadowingNames
            def task_md2pdf():
                for x in self.link_tasks(taskgen(self)):
                    yield x

            DOIT_CONFIG = {'action_string_formatting': 'both',
                           'dep_file': os.path.join(self.temp_dir,
                                                    'amd2pdf-db.json'), }
            yield locals()
        finally:
            if not self.debug:
                shutil.rmtree(self.temp_dir)

    def TaskGen(self, *args, **kw):
        if self.verbosity_level>0:
            kw['verbosity'] = True
        c = MyTask(*args, **kw)
        return c.get(self)


TypeCmd = lambda: 'type' if isWin else 'cat'
NUL = lambda: '/dev/null' if not isWin else 'NUL$'


class MyTask:
    def __init__(self, cmdline, output_name=None, deps=None, taskname=None,
                 ignore_exec_errors=False, verbosity=False, stdout=True,
                 stdin='{dependencies}', ext='html'):
        self.stdin = stdin
        self.stdout = stdout
        self.ext = ext
        self.verbose = verbosity
        self.ignore_exec_errors = ignore_exec_errors
        self.taskname = taskname if taskname else GuessName(cmdline)
        self.deps = deps if deps else []
        self.cmdline = cmdline
        self.output_name = output_name if output_name else self.taskname + '.' + ext

    def get_input(self):
        # prepare input:
        if isinstance(self.stdin, dict):
            input = self.stdin['targets'][0]
        elif isinstance(self.stdin, (types.FunctionType, types.MethodType)):
            input = self.stdin()
        elif isinstance(self.stdin, str):
            input = self.stdin
        else:
            raise Amd2pdfException("Unknown type for stdin: '%r'"%self.stdin)
        return input

    @property
    def fullcmd(self):
        cmdline = self.cmdline
        if cmdline.startswith('python '):
            cmdline = W(sys.executable) + cmdline[len("python"):]

        fullcmd = [TypeCmd(),
                   self.get_input(), #self.stdin['targets'][0] if self.stdin else '{dependencies}',
                   '|', cmdline]
        if self.stdout:
            fullcmd.append('> '+TARGET_REF)
        else:
            if TARGET_REF not in cmdline:
                raise ExecError("When using no stdout, targets must be in cmd!")
        if self.ignore_exec_errors:
            fullcmd.append('||echo errors ignored')
        fullcmd = ' '.join(fullcmd)
        if ' ' in self.output_name:
            fullcmd = fullcmd.replace(TARGET_REF, '"'+TARGET_REF+'"')
        return fullcmd

    @property
    def actions(self):
        actions = []
        cmd = self.fullcmd
        if self.verbose:
            actions.append(lambda: print("------------------------------"))
            actions.append(lambda: print('> cmd: ' + cmd, file=sys.stderr))
        actions.append(cmd)
        return actions

    def get(self, cfg):
        if not os.path.isabs(self.output_name):
            self.output_name = os.path.join(cfg.temp_dir, self.output_name)
        return {'actions': self.actions, 'targets': [self.output_name],
                'file_dep': reduce_deps(self.deps),
                'verbosity': 2 if self.verbose else 0,
                'clean': [clean_targets],
                'name': self.taskname}


def gen_html2pdf(fname):
    page_format = os.environ.get('PAGE', 'A4')
    margins = {'A4': {'T': '1in', 'L': '1in', 'R': '1in', 'B': '1in'}}
    inch_to_mm = lambda x: (float(x) * 25.4) if not x.endswith('in') \
                                                        else inch_to_mm(x[:-2])
    defaults = {('header', 'left'): 'Made with amd2pdf',
                ('footer', 'left'): 'https://github.com/tenuki/amd2pdf',
                ('header', 'right'): '(sample)',
                ('header', 'center'): '[title]',
                ('footer', 'center'): "[page] of [topage]", }
    opts = ['wkhtmltopdf', '--enable-internal-links',
            '--disable-smart-shrinking', ]
    opts = opts + ['-%s %s' % (margin, margins[page_format][margin]) for margin
                   in 'TLRB']
    opts = opts + ['--header-spacing %d' % int(
        ((1.0 * inch_to_mm(margins[page_format]['T'])) / 3) + 0.5)]
    opts = opts + ['--footer-spacing %d' % int(
        ((1.0 * inch_to_mm(margins[page_format]['B'])) / 3) + 0.5)]
    opts = opts + []
    opts = opts + ['--page-size %s' % page_format]

    for hf in ['header', 'footer']:
        for lcr in ['left', 'center', 'right']:
            h = os.environ.get(('%s_%s' % (hf, lcr)).upper(),
                               defaults.get((hf, lcr)))
            if h is None:
                continue
            opts.append('--%s-%s %s' % (hf, lcr, op_esc(h)))
    return ' '.join(opts + ['- ' + fname])


def fast_check_for_toc(cfg):
    with open(cfg.source, 'rb') as src:
        data = src.read()
    return b'[TOC]' in data


def task_md2pdf(cfg):
    TOC = fast_check_for_toc(cfg)
    yield cfg.TaskGen('python -m markdown -x toc', taskname='md2html')
    if TOC:
        yield cfg.TaskGen('python -c "import amd2pdf;amd2pdf.toc_to_dummy()"',
                          taskname='toc_to_dummy')

    yield (wraphtml := cfg.TaskGen('python -c "import amd2pdf;amd2pdf.wrap()"',
                                   taskname='wrap'))

    if TOC:
        yield cfg.TaskGen(gen_html2pdf(TARGET_REF), ext='pdf', stdout=False,
                          ignore_exec_errors=True)
        yield cfg.TaskGen('pdftohtml -stdout -xml -enc UTF-8 -i - image',
                          ext='xml')
        yield (xml2idx := cfg.TaskGen(
            'python -c "import amd2pdf;amd2pdf.gettoc()" -',
            taskname="xml2idx", ext='idx'))
    else:
        # fake xml2idx task
        yield (xml2idx := cfg.TaskGen('python -c "print(\'[]\')"',
                                       taskname="xml2idx", ext='idx'))

    yield cfg.TaskGen('python -c "import amd2pdf;amd2pdf.htmlpatch()" ' +
                      xml2idx['targets'][0], taskname="htmlpatch",
                      stdin=wraphtml)
    yield cfg.TaskGen(gen_html2pdf(TARGET_REF), cfg.Final, stdout=False,
                      taskname='html2pdf2', ext='pdf', ignore_exec_errors=True)

    if cfg.autoopen:
        yield cfg.TaskGen(
            'python -c "import webbrowser;webbrowser.open(%r)"' % cfg.Final,
            stdin=NUL,
            taskname="openresult")
