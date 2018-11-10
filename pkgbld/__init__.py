"""
Specify what is available to import from the pkgbld package.
"""
from pkgbld.release import release

from pkgbld._version import get_versions
__version__ = get_versions()['version']
del get_versions
