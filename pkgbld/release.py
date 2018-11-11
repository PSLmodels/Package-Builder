"""
Policy Simulaton Library (PSL) model Anaconda-Cloud package release logic.
"""
# CODING-STYLE CHECKS:
# pycodestyle release.py
# pylint --disable=locally-disabled release.py

import re


PYTHON_VERSIONS = ['3.6']
OS_PLATFORMS = ['osx-64', 'linux-64', 'win-32', 'win-64']

GITHUB_URL = 'https:/github.com/open-source-economics/'
CONDA_CHANNELS = ['pslmodels']
ANACONDA_USER = 'pslmodels'


def release(repo_name, pkg_name, version):
    """
    Conduct local build and upload to Anaconda Cloud of conda packages
    for each platform for specified Policy Simulation Library (PSL) model
    and version.

    Parameters
    ----------
    repo_name: string
        repository name appended to GITHUB_URL

    pkg_name: string
        package name for repository specified by repo_name

    version: string
        version string consistent with semantic versioning

    Raises
    ------
    ValueError:
        if parameters are not valid

    Returns
    -------
    Nothing

    Notes
    -----
    Example usage: release('Tax-Calculator', 'taxcalc', '0.23.0')
    """
    # check parameters
    if not isinstance(repo_name, str):
        raise ValueError('repo_name is not a string object')
    if not isinstance(pkg_name, str):
        raise ValueError('pkg_name is not a string object')
    if not isinstance(version, str):
        raise ValueError('version is not a string object')
    pattern = r'^[0-9]+\.[0-9]+\.[0-9]+$'
    if re.match(pattern, version) is None:
        msg = 'version=<{}> does not follow semantic-versioning rules'
        raise ValueError(msg.format(version))

    print('Hello from Package-Builder release function')
