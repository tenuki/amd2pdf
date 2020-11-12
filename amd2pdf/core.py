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
                 title=None, output_filename=None):
        self.temp = tempfile.mkdtemp(prefix='md2pdf-')
        self.debug = debug
        self.verbose = verbose
        self.source = source
        self.output_filename = output_filename
        self.params = {'css': css, 'page': page, 'title': title}
        self.defaults = {'css': default_style, 'page': 'A4',
                         'title':os.environ.get('TITLE', '')}

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

    def TaskGen(self, cmdline, outputName=None, deps=None, taskname=None,
                ignorExecErrors=False, verbosity=None, stdout=True, stdin=None,
                ext='html'):
        if deps is None: deps = []
        if taskname is None:
            taskname = GuessName(cmdline)

        if cmdline.startswith('python '):
            cmdline = W(sys.executable) + cmdline[len("python"):]

        _type = 'type' if isWin else 'cat'
        if stdin is None:
            fullcmd = _type + ' {dependencies} | ' + cmdline
        else:
            fullcmd = _type + ' ' + stdin['targets'][0] + ' | ' + cmdline
        if stdout:
            fullcmd += ' > %(targets)s'
        fullcmd += '' if not ignorExecErrors else '||echo errors ignored'

        if outputName is None:
            outputName = taskname + '.' + ext
        if not os.path.isabs(outputName):
            outputName = os.path.join(self.TempDirName, outputName)

        return {'actions': [fullcmd],
                'targets': [W(outputName)],
                'file_dep': reduce_deps(deps),
                'verbosity': verbosity if verbosity else self.Verbosity,
                'clean': [clean_targets],
                'name': taskname}

    def _setup_env(self):
        os.environ['TMP'] = os.environ['TEMP'] = self.TempDirName
        for key, value in self.params.items():
            os.environ[key.upper()] = value if value else self.defaults.get(key)

    def link_tasks(self, task_gen):
        prev = self.Initial
        for task in task_gen:
            if (not 'file_dep' in task) or (0==len(task['file_dep'])):
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
                # for x in self.)taskgen(self):
                for x in self.link_tasks(taskgen(self)):
                    yield x

            DOIT_CONFIG = {'action_string_formatting': 'both'}
            yield locals()
        finally:
            if not self.debug:
                shutil.rmtree(self.TempDirName)


def gen_html2pdf():
    op_esc = lambda x: '"%s"'%x if x[0]!='"' else x

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
    yield cfg.TaskGen("node -e \"require('remark-toc-stdin').main(()=>'"+TAG+"')\"",
                      taskname='toc')
    yield (wraphtml := cfg.TaskGen('python -c "import amd2pdf;amd2pdf.wrap()"',
                           taskname='wrap'))
    yield cfg.TaskGen(gen_html2pdf(), ext='pdf', ignorExecErrors=True)
    yield cfg.TaskGen('pdftohtml -stdout -xml -enc UTF-8 -i - image',
                      ext='xml')
    yield (xml2idx := cfg.TaskGen('python -c "import amd2pdf;amd2pdf.gettoc()" -',
                          taskname="xml2idx", ext='idx'))
    yield cfg.TaskGen('python -c "import amd2pdf;amd2pdf.htmlpatch()" ' +
                      xml2idx['targets'][0], taskname="htmlpatch",
                      stdin=wraphtml)  # deps=[xml2idx, wraphtml]
    yield cfg.TaskGen(gen_html2pdf(), cfg.Final, taskname='html2pdf2',
                      ext='pdf',
                      ignorExecErrors=True)
