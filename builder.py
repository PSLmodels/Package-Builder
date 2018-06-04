import sys
import subprocess as sp
import os
import re


"""
Release a package with the following commands:
export TOKEN=yourtoken
python builder.py gh-username repo-name package-name package-version

e.g. python builder.py open-source-economics OG-USA ogusa 0.5.11

Note: `CURRENT_DIST` will have to be changed to your computer's operating
system
"""


CURRENT_DIST = 'linux-64'
DISTS = {'linux-32', 'linux-64', 'win-32', 'win-64', 'osx-64'}

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
    Build package for each distribution and upload to conda
    """
    vspl = python_version.split('.')
    python_string = vspl[0] + vspl[1]
    run(f'conda build conda.recipe --token $TOKEN --output-folder artifacts --no-anaconda-upload --python {python_version}')
    run(f'conda convert artifacts/{CURRENT_DIST}/{package}-{vers}-py{python_string}_0.tar.bz2 -p all -o artifacts/')

    # check that we have the platforms we want
    assert len(DISTS - set(os.listdir('artifacts'))) == 0

    for dist in DISTS:
        run(f'anaconda --token $TOKEN  upload --force --user ospc artifacts/{dist}/{package}-{vers}-py{python_string}_0.tar.bz2')


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
    owner, repo, package, vers = sys.argv[1:]
    print('owner', owner)
    print('repo name', repo)
    print('package name', package
    print('package version', vers)
    run(f'git clone https://github.com/{owner}/{repo}/')
    os.chdir(repo)
    run(f'git checkout -b v{vers} {vers}')
    replace_version(vers)
    run(f'conda config --add channels ospc')

    if not os.path.isdir('artifacts'):
        os.mkdir('artifacts')

    for python_version in ('2.7', '3.6'):
        build_and_upload(python_version, repo, package, vers)
