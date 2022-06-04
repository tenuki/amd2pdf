# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()


setup(
    name='amd2pdf',
    version='0.1.3',
    description='Another markdown to pdf with TOC and page index support',
    long_description='This is another markdown to pdf conversion tool. '
                     'This includes TOC markdown tag support and the generated '
                     'output is page indexed.',
    author='david weil',
    author_email='david.weil@endlesstruction.com.ar',
    license="GNU General Public License v3.0",
    url='https://github.com/tenuki/amd2pdf',
    packages=find_packages(exclude=('tests', 'docs')),
        package_data={
            # If any package contains *.txt files, include them:
            #"": ["*.txt"],
            # And include any *.dat files found in the "data" subdirectory
            # of the "mypkg" package, also:
            "amd2pdf": ["rsrc/*.css", "*.js"],
        },
    install_requires=['doit', 'jinja2', 'Markdown'],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            "amd2pdf=amd2pdf:main"
        ]
    }
)

