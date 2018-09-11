"""
NOTE: this Python script was developed by Hank Doupe as an alternative
to the pb CLI tool documented in the policybrain-builder/README.md file.
If you have questions about or problems with this builder.py script,
please direct your questions to Hank, @hdoupe, on GitHub.

Build and upload a conda package with the following commands:

export TOKEN=yourtoken
python builder.py repo-name package-name package-version

EXAMPLE: python builder.py OG-USA ogusa 0.5.11

GLOBAL VARIABLES:
- GITHUB_ORGANIZATION: set to either GitHub username or organization
- DEP_CONDA_CHANNEL: list of non-default conda channels (if target package
                     depends on packages that are in non-default channels,
                     this is where those non-default channels should be
                     specified)
- CONDA_USER: the username for the package upload
- PYTHON_VERSIONS: versions of Python for which the package should be built
- OPERATING_SYSTEMS: operating systems for which the package should be built

NOTES:

(1) This script expects modern versions of conda and conda-build:
    conda >= 4.5 and conda-build >= 3.5

(2) To build/upload a conda package that is outside of the
    open-source-economics GitHub organization, change `GITHUB_ORGANIZATION`
    to the desired GitHub username or organization name
"""

import os
import sys
import re
import subprocess as sp
import platform


GITHUB_ORGANIZATION = 'open-source-economics'
DEP_CONDA_CHANNELS = ['ospc']
CONDA_USER = 'ospc'
PYTHON_VERSIONS = ['2.7', '3.6']
OPERATING_SYSTEMS = ['linux-64', 'win-32', 'win-64', 'osx-64']


def get_current_os():
    """
    Get the system corresponding to OPERATING_SYSTEMS
    """
    system_ = platform.system()
    if system_ == 'Darwin':
        conda_name = 'osx'
    elif system_ == 'Linux':
        conda_name = 'linux'
    elif system_ == 'Windows':
        conda_name = 'win'
    else:
        msg = ("The user is using an unexpected operating system: {}.\n"
               "Expected operating systems are windows, linux, or osx.")
        raise OSError(msg.format(system_))
    # see link:
    # https://docs.python.org/3.6/library/platform.html#platform.architecture
    is_64bit = sys.maxsize > 2 ** 32
    n_bits = '64' if is_64bit else '32'
    return conda_name + '-' + n_bits


def run(cmd):
    """
    Run shell commands, make sure they return with status '0'
    """
    print('running', cmd)
    proc = sp.Popen([cmd], shell=True)
    proc.wait()
    assert proc.poll() == 0


def build_and_upload(python_version, package, vers):
    """
    Build package for each os and upload to conda
    """
    vspl = python_version.split('.')
    python_string = vspl[0] + vspl[1]
    current_os = get_current_os()
    cmd = ('conda build --old-build-string conda.recipe '
           '--output-folder artifacts '
           '--no-anaconda-upload --python {python_version}')
    run(cmd.format(python_version=python_version))
    cmd = ('conda convert '
           'artifacts/{os}/{package}-{vers}-py{python_string}_0.tar.bz2 '
           '-p all -o artifacts/')
    run(cmd.format(os=current_os, package=package, vers=vers,
                   python_string=python_string))

    # check that we have the operating systems we want
    assert len(set(OPERATING_SYSTEMS) - set(os.listdir('artifacts'))) == 0

    for os_ in OPERATING_SYSTEMS:
        cmd = ('anaconda --token $TOKEN  upload --force --user {CONDA_USER} '
               'artifacts/{os_}/{package}-{vers}-py{python_string}_0.tar.bz2')
        run(cmd.format(CONDA_USER=CONDA_USER, os_=os_, package=package,
                       vers=vers, python_string=python_string))


def replace_version(version):
    """
    Replace version in `meta.yaml` file so that it doesn't need to be updated
    for each release
    """
    filename = 'conda.recipe/meta.yaml'
    pattern = r'version: .*'
    replacement = 'version: {version}'.format(version=version)
    lines = []
    with open(filename) as meta_file:
        for line in meta_file.readlines():
            lines.append(re.sub(pattern, replacement, line))
    with open(filename, 'w') as meta_file:
        for line in lines:
            meta_file.write(line)


if __name__ == '__main__':
    repo, package, vers = sys.argv[1:]
    print('repo name', repo)
    print('package name', package)
    print('package version', vers)
    cmd = 'git clone https://github.com/{GITHUB_ORGANIZATION}/{repo}/'
    run(cmd.format(GITHUB_ORGANIZATION=GITHUB_ORGANIZATION, repo=repo))
    os.chdir(repo)
    run('git checkout -b v{vers} {vers}'.format(vers=vers))
    replace_version(vers)
    # add depenedent channels if specified
    for channel in DEP_CONDA_CHANNELS:
        run('conda config --add channels {channel}'.format(channel=channel))

    if not os.path.isdir('artifacts'):
        os.mkdir('artifacts')

    for python_version in PYTHON_VERSIONS:
        build_and_upload(python_version, package, vers)

    os.chdir('..')
    run('rm -rf {repo}'.format(repo=repo))

    print('build and upload complete...')
