#!/usr/bin/env python

from io import open
from setuptools import find_packages, setup


with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(name="Package-Builder",
      version="0.7.0",
      description="Policy Simulation Library (PSL) package management",
      url="https://github.com/open-source-economics/Package-Builder",
      author="Joseph Crail",
      author_email="jbcrail@gmail.com",
      keywords='PSL',
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
      """)
