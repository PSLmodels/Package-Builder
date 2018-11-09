#!/usr/bin/env python

from io import open
from setuptools import find_packages, setup


with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(name="Package-Builder",
      version="0.8.0",
      description="Policy Simulation Library (PSL) models package management",
      url="https://github.com/open-source-economics/Package-Builder",
      author="Martin Holmer (based on original work by Joseph Crail)",
      author_email="martin.holmer@gmail.com",
      keywords='PSLmodels',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
      ],
      packages=find_packages(),
      package_dir={'pb': 'pb'},
      install_requires=['click'],
      zip_safe=False,
      long_description=readme,
      entry_points="""
        [console_scripts]
        pb=pb.cli.main:start
      """)
