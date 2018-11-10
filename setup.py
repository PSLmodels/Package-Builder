import versioneer
versioneer.VCS = 'git'
versioneer.versionfile_source = 'pkgbld/_version.py'
versioneer.versionfile_build = 'pkgbld/_version.py'
versioneer.tag_prefix = ''  # tags are like 1.2.0
versioneer.parentdir_prefix = 'pkgbld-'
# above dirname like 'pkgbld-1.2.0'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
        longdesc = f.read()

version = versioneer.get_version()
cmdclass = versioneer.get_cmdclass()

config = {
    'description': 'Package Builder',
    'url': 'https://github.com/open-source-economics/Package-Builder',
    'download_url': 'https://github.com/open-source-economics/Package-Builder',
    'description': 'pkgbld',
    'long_description': longdesc,
    'version': version,
    'cmdclass': cmdclass,
    'license': 'CC0 1.0 Universal public domain dedication',
    'packages': ['pkgbld'],
    'include_package_data': True,
    'name': 'pkgbld',
    'install_requires': ['conda'],
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: CC0 1.0 Universal public domain dedication',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    'tests_require': ['pytest']
}

setup(**config)
