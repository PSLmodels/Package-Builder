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
                 '                  [--help]  [--local LOCAL]  [--also37]\n'
                 '                  [--dryrun]  [--version]')
    parser = argparse.ArgumentParser(
        prog='',
        usage=usage_str,
        description=('Creates conda packages named PACKAGE_NAME for the PSL '
                     'model in REPOSITORY_NAME that has a GitHub release '
                     'named MODEL_VERSION.  The packages are build locally '
                     'in a temporary workspace and then uploaded to the '
                     'Anaconda Cloud PSLmodels channel for public '
                     'distribution.  The built/uploaded packages are '
                     'for Python 3.6 and optionally Python 3.7.')
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
                              'Example: 1.0.1'),
                        default=None)
    parser.add_argument('--local',
                        help=('optional flag where LOCAL is name of local '
                              'directory containing model source code used '
                              'to build package, which is installed on local '
                              'computer as version 0.0.0; no --local option '
                              'implies model source code is cloned from '
                              'GitHub REPOSITORY_NAME for MODEL_RELEASE '
                              'and packages are uploaded to Anaconda Cloud '
                              'PSLmodels channel for public distribution'),
                        default=None)
    parser.add_argument('--also37',
                        help=('optional flag that causes build/upload of '
                              'packages for Python 3.7'),
                        default=False,
                        action="store_true")
    parser.add_argument('--dryrun',
                        help=('optional flag that writes execution plan '
                              'to stdout and quits without executing plan'),
                        default=False,
                        action="store_true")
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
                 '{} does not exist\n'.format(pkgbld.ANACONDA_TOKEN_FILE))
    if args.local and args.also37:
        emsg += ('ERROR: cannot use --local and --also37 options '
                 'at the same time\n')
    if args.local and not os.path.isdir(args.local):
        emsg += 'ERROR: LOCAL directory {} does not exist\n'.format(args.local)
    if emsg:
        print(emsg)
        print('USAGE:', usage_str)
        return 1
    # call pkgbld release function with specified parameters
    pkgbld.release(repo_name, pkg_name, version,
                   localdir=args.local, also37=args.also37, dryrun=args.dryrun)
    return 0
