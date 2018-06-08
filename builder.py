import sys
import subprocess as sp
import os
import re
import platform


"""
Release a package with the following commands:
export TOKEN=yourtoken
python builder.py repo-name package-name package-version

e.g. python builder.py OG-USA ogusa 0.5.11

Note: To release a package that is outside of the open-source-economics
GitHub organization, change `GITHUB_ORGANIZATION` to the desired username or
GitHub organization name.

Global variables:
- GITHUB_ORGANIZATION: Set either GH username or organization
- DEP_CONDA_CHANNEL: A list of non-default conda channels. The target package
                     may depend on packages that are in non-default channels.
                     This is where those non-default channels should be
                     specified.
- CONDA_USER: The username for the package upload
- PYTHON_VERSIONS: Versions of Python for which the package should be built
- OPERATING_SYSTEMS: Operating systems for which the package should be built
"""

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
    # see https://docs.python.org/3.6/library/platform.html#platform.architecture
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


def build_and_upload(python_version, repo, package, vers):
    """
    Build package for each os and upload to conda
    """
    vspl = python_version.split('.')
    python_string = vspl[0] + vspl[1]
    current_os = get_current_os()
    run(f'conda build conda.recipe --token $TOKEN --output-folder artifacts --no-anaconda-upload --python {python_version}')
    run(f'conda convert artifacts/{current_os}/{package}-{vers}-py{python_string}_0.tar.bz2 -p all -o artifacts/')

    # check that we have the operating systems we want
    assert len(OPERATING_SYSTEMS - set(os.listdir('artifacts'))) == 0

    for os_ in OPERATING_SYSTEMS:
        run(f'anaconda --token $TOKEN  upload --force --user {CONDA_USER} artifacts/{os_}/{package}-{vers}-py{python_string}_0.tar.bz2')


def replace_version(version):
    """
    Replace version in `meta.yaml` file so that it doesn't need to be updated
    for each release
    """
    filename = 'conda.recipe/meta.yaml'
    pattern = r'version: .*'
    replacement = f'version: {version}'
    lines = []
    with open(filename) as f:
        for line in f.readlines():
            lines.append(re.sub(pattern, replacement, line))
    with open(filename, 'w') as f:
        for line in lines:
            f.write(line)


if __name__ == '__main__':
    repo, package, vers = sys.argv[1:]
    print('repo name', repo)
    print('package name', package
    print('package version', vers)
    run(f'git clone https://github.com/{GITHUB_ORGANIZATION}/{repo}/')
    os.chdir(repo)
    run(f'git checkout -b v{vers} {vers}')
    replace_version(vers)
    # add depenedent channels if specified
    for channel in DEP_CONDA_CHANNELS:
        run(f'conda config --add channels {channel}')

    if not os.path.isdir('artifacts'):
        os.mkdir('artifacts')

    for python_version in PYTHON_VERSIONS:
        build_and_upload(python_version, repo, package, vers)
