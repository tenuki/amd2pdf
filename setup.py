# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

setup(
    name='amd2pdf',
    version='0.1.0',
    description='Another markdown to pdf conversion tool',
    long_description=readme,
    author='david weil',
    author_email='david.weil@endlesstruction.com.ar',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
        package_data={
            # If any package contains *.txt files, include them:
            #"": ["*.txt"],
            # And include any *.dat files found in the "data" subdirectory
            # of the "mypkg" package, also:
            "amd2pdf": ["rsrc/*.css"],
        },
    data_files=[('', ['amd2pdf/rsrc/style.css'])],
    install_requires=['doit', 'jinja2'],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            "amd2pdf=amd2pdf:main"
        ]
    }
)

