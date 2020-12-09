# -*- coding: utf-8 -*-
import shutil
from contextlib import contextmanager

from . import helpers

import os
import sys
import tempfile

from doit.task import clean_targets

from .helpers import default_style, reduce_deps, ShouldWrap, isWin, W
from .tasks import TAG


def GuessName(cmdline):
    parts = cmdline.split()
    if parts[0] == 'node' or ('python' in parts[0]):
        return parts[1].split('.')[0]
    return parts[0]


class Config:
    def __init__(self, source, verbose=False, debug=False, css=None, page=None,
                 title=None, output_filename=None, autoopen=False):
        self.temp = tempfile.mkdtemp(prefix='md2pdf-')
        self.debug = debug
        self.verbose = verbose
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
            raise Exception("shouldn't happend")
        return fullname

    @property
    def Initial(self):
        source = self.source
        if ShouldWrap(source):
            handle, fullname = tempfile.mkstemp(prefix='src-md',
                                                dir=self.TempDirName)
            with open(source, 'rb') as src:
                data = src.read(4096)
                while data:
                    os.write(handle, data)
                    data = src.read(4096)
            os.close(handle)
            source = fullname
        return {'targets': [source]}

    @property
    def Verbosity(self):
        return 2 if self.verbose else 0

    @property
    def TempDirName(self):
        return self.temp

    def _setup_env(self):
        os.environ['TMP'] = os.environ['TEMP'] = self.TempDirName
        for key, value in self.params.items():
            os.environ[key.upper()] = value if value else self.defaults.get(key)

    def link_tasks(self, task_gen):
        prev = self.Initial
        for task in task_gen:
            if (not 'file_dep' in task) or (0 == len(task['file_dep'])):
                task['file_dep'] = reduce_deps([prev])
            yield task
            prev = task

    @contextmanager
    def prepare(self, taskgen):
        self._setup_env()
        if self.debug:
            print("Temporary files at:", self.TempDirName)
        try:
            def task_md2pdf():
                for x in self.link_tasks(taskgen(self)):
                    yield x

            DOIT_CONFIG = {
                'action_string_formatting': 'both',
                'dep_file': os.path.join(self.TempDirName, 'doit-db.json'),
            }
            yield locals()
        finally:
            if not self.debug:
                shutil.rmtree(self.TempDirName)

    def TaskGen(self, *args, **kw):
        c = MyTask(*args, **kw)
        return c.get(self)


TypeCmd = lambda: 'type' if isWin else 'cat'


class MyTask:
    def __init__(self, cmdline, outputName=None, deps=None, taskname=None,
                 ignorExecErrors=False, verbosity=False, stdout=True, stdin=None,
                 ext='html'):
        self.stdin = stdin
        self.stdout = stdout
        self.ext = ext
        self._verbosity = verbosity
        self.ignorExecErrors = ignorExecErrors
        self.taskname = taskname if taskname else GuessName(cmdline)
        self.deps = deps if deps else []
        self.cmdline = cmdline
        self.outputName = outputName if outputName else self.taskname+'.'+ext

    @property
    def fullcmd(self):
        cmdline = self.cmdline
        if cmdline.startswith('python '):
            cmdline = W(sys.executable) + cmdline[len("python"):]
        fullcmd = [TypeCmd(),
                   self.stdin['targets'][0] if self.stdin else '{dependencies}',
                   '|', cmdline]
        if self.stdout:
            fullcmd.append('> %(targets)s')
        if self.ignorExecErrors:
            fullcmd.append('||echo errors ignored')
        return ' '.join(fullcmd)

    @property
    def actions(self):
        actions = []
        cmd = self.fullcmd
        if self._verbosity:
            actions.append( lambda:print('> '+cmd, file=sys.stderr) )
        actions.append(cmd)
        return actions

    def get(self, cfg):
        self._verbosity = self._verbosity or cfg.Verbosity

        if not os.path.isabs(self.outputName):
            self.outputName = os.path.join(cfg.TempDirName, self.outputName)

        return {'actions': self.actions,
                'targets': [W(self.outputName)],
                'file_dep': reduce_deps(self.deps),
                'verbosity': self._verbosity,
                'clean': [clean_targets],
                'name': self.taskname}


def gen_html2pdf():
    op_esc = lambda x: '"%s"' % x if x[0] != '"' else x

    defaults = {
        ('header', 'left'): 'Made with amd2pdf',
        ('footer', 'left'): 'https://github.com/tenuki/amd2pdf',
        ('header', 'right'): '(sample)',
        ('header', 'center'): '[title]',
        ('footer', 'center'): "[page] of [topage]",
    }

    opts = ['wkhtmltopdf',
            '--page-size %s' % os.environ.get('PAGE', 'A4')]
    for hf in ['header', 'footer']:
        for lcr in ['left', 'center', 'right']:
            h = os.environ.get(('%s_%s' % (hf, lcr)).upper(),
                               defaults.get((hf, lcr)))
            if h is None:
                continue
            opts.append('--%s-%s %s' % (hf, lcr, op_esc(h)))
    return ' '.join(opts + ['- -'])


def task_md2pdf(cfg):
    yield cfg.TaskGen(
        "node -e \"require('remark-toc-stdin').main(()=>'" + TAG + "')\"",
        taskname='toc')
    yield (wraphtml := cfg.TaskGen('python -c "import amd2pdf;amd2pdf.wrap()"',
                                   taskname='wrap'))
    yield cfg.TaskGen(gen_html2pdf(), ext='pdf', ignorExecErrors=True)
    yield cfg.TaskGen('pdftohtml -stdout -xml -enc UTF-8 -i - image',
                      ext='xml')
    yield (
        xml2idx := cfg.TaskGen('python -c "import amd2pdf;amd2pdf.gettoc()" -',
                               taskname="xml2idx", ext='idx'))
    yield cfg.TaskGen('python -c "import amd2pdf;amd2pdf.htmlpatch()" ' +
                      xml2idx['targets'][0], taskname="htmlpatch",
                      stdin=wraphtml)  # deps+=[wraphtml]
    yield cfg.TaskGen(gen_html2pdf(), cfg.Final, taskname='html2pdf2',
                      ext='pdf',
                      ignorExecErrors=True)

    if cfg.autoopen:
        yield cfg.TaskGen('python -c "import webbrowser;webbrowser.open(%r)"'
                          % cfg.Final, taskname="openresult")
