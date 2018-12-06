"""
Command-line interface (CLI) to Package-Builder response function,
which can be accessed as 'pbrelease' from an installed pkgbld conda package.
"""
# CODING-STYLE CHECKS:
# pycodestyle cli.py
# pylint --disable=locally-disabled cli.py

import argparse
import re
import os
import pkgbld


def main():
    """
    Contains command-line interface (CLI) to Package-Builder response function.
    """
    # parse command-line arguments:
    usage_str = ('pbrelease  REPOSITORY_NAME  PACKAGE_NAME  MODEL_VERSION\n'
                 '                  [--help]  [--version]')
    parser = argparse.ArgumentParser(
        prog='',
        usage=usage_str,
        description=('Creates conda packages named PACKAGE_NAME for the PSL '
                     'model in REPOSITORY_NAME that has a MODEL_VERSION '
                     'release.  The packages are build locally in a '
                     'temporary workspace and then uploaded to the '
                     'Anaconda Cloud PSLmodels channel for public '
                     'distribution.')
    )
    parser.add_argument('REPOSITORY_NAME', nargs='?',
                        help=('Name of repository in the GitHub organization '
                              'called PSLmodels. Example: Tax-Calculator'),
                        default=None)
    parser.add_argument('PACKAGE_NAME', nargs='?',
                        help=('Name of packages to build and upload. '
                              'Example: taxcalc'),
                        default=None)
    parser.add_argument('MODEL_VERSION', nargs='?',
                        help=('Model release string that has X.Y.Z '
                              'semantic-versioning pattern. '
                              'Example: 0.23.2'),
                        default=None)
    parser.add_argument('--version',
                        help=('optional flag that writes Package-Builder '
                              'release version to stdout and quits'),
                        default=False,
                        action="store_true")
    args = parser.parse_args()
    # show Package-Builder version and quit if --version option specified
    if args.version:
        print('Package-Builder {}'.format(pkgbld.__version__))
        return 0
    # check command-line arguments
    repo_name = args.REPOSITORY_NAME
    pkg_name = args.PACKAGE_NAME
    version = args.MODEL_VERSION
    emsg = ''
    if not isinstance(repo_name, str):
        emsg += 'ERROR: REPOSITORY_NAME is not specified\n'
    if not isinstance(pkg_name, str):
        emsg += 'ERROR: PACKAGE_NAME is not specified\n'
    if not isinstance(version, str):
        emsg += 'ERROR: MODEL_VERSION is not specified\n'
    else:
        pattern = r'^[0-9]+\.[0-9]+\.[0-9]+$'
        if re.match(pattern, version) is None:
            emsg += ('ERROR: MODEL_VERSION does have X.Y.Z '
                     'semantic-versioning pattern\n')
    if not os.path.isfile(pkgbld.ANACONDA_TOKEN_FILE):
        emsg += ('ERROR: Anaconda token file '
                 '{} does not exist'.format(pkgbld.ANACONDA_TOKEN_FILE))
    if emsg:
        print(emsg)
        print('USAGE:', usage_str)
        return 1
    # call pkgbld release function with specified parameters
    pkgbld.release(repo_name, pkg_name, version)
    return 0
