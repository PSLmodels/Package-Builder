"""
Command-line interface (CLI) to Package-Builder response function,
which can be accessed as 'pbrelease' from an installed pkgbld conda package.
"""
# CODING-STYLE CHECKS:
# pycodestyle cli.py
# pylint --disable=locally-disabled cli.py

import sys
import argparse
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
                              'called pslmodels (nee open-source-economics). '
                              'Example: Tax-Calculator'),
                        default=None)
    parser.add_argument('PACKAGE_NAME', nargs='?',
                        help=('Name of packages to build and upload. '
                              'Example: taxcalc'),
                        default=None)
    parser.add_argument('MODEL_VERSION', nargs='?',
                        help=('Model release string that is consistent '
                              'with semantic-versioning rules. '
                              'Example: 0.22.2'),
                        default=None)
    parser.add_argument('--version',
                        help=('optional flag that writes Package-Builder '
                              'release version to stdout and quits'),
                        default=False,
                        action="store_true")
    args = parser.parse_args()
    # show Package-Builder version and quit if --version option specified
    if args.version:
        version = pkgbld.__version__
        if version == 'unknown':
            version = 'locally.generated.package'
        sys.stdout.write('Package-Builder {}\n'.format(version))
        return 0
    # call pkgbld release function with specified parameters
    pkgbld.release(repo_name=args.REPOSITORY_NAME,
                   pkg_name=args.PACKAGE_NAME,
                   version=args.MODEL_VERSION)
    return 0
