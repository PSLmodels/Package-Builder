#!/usr/bin/env python

from io import open
from setuptools import find_packages, setup


with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(name="policybrain-builder",
      version="0.6.0",
      description="Open Source Policy Center (OSPC) package management",
      url="https://github.com/open-source-economics/policybrain-builder",
      author="Joseph Crail",
      author_email="jbcrail@gmail.com",
      keywords='ospc',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
      ],
      packages=find_packages(),
      package_dir={'policybrain_builder': 'policybrain_builder'},
      install_requires=['click'],
      zip_safe=False,
      long_description=readme,
      entry_points="""
        [console_scripts]
        pb=policybrain_builder.cli.main:start
        policybrain=policybrain_builder.cli.main:start
      """)
