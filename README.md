[![PSL tool](https://img.shields.io/badge/PSL-tool-a0a0a0.svg)](https://www.PSLmodels.org)
[![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/release/python-360/)


Using Package-Builder's pbrelease tool
======================================

This document tells you how to use the command-line interface (CLI) to
Package-Builder, which is called the `pbrelease` tool, to build conda
packages for your Policy Simulation Library (PSL) model and upload
them to the Anaconda Cloud's `PSLmodels` channel for public
distribution.  If you have questions about using `pbrelease`, or
experience problems, or want to request an enhancement, create a new
issue
[here](https://github.com/PSLmodels/Package-Builder/issues)
that poses your question, or provides details on what you think is
wrong with `pbrelease`, or describes the enhancement you're
requesting.


What is pbrelease?
------------------

The code in this Package-Builder GitHub repository, which is part of
the `PSLmodels` GitHub organization, generates a conda package called
`pkgbld` that contains the `pbrelease` command-line tool.  For models
in the `PSLmodels` GitHub organization that meet certain criteria (see
below), `pbrelease` can be used to build conda packages (for Windows,
Linux, and Mac) for a specified model release version and then to
upload those built packages to the Anaconda Cloud's `PSLmodels`
channel for public distribution.

How to install pbrelease?
-------------------------

At the operating-system command prompt on a computer that has the
Anaconda distribution of Python 3.6 or 3.7 installed, execute this
command if you have never installed the package that contains the
`pbrelease` tool:

```
$ conda install -c PSLmodels pkgbld --yes
```

If you have previously installed that package, replace `install` with
`update` to upgrade to the most recent version of the package.

Next confirm that the installation/update went smoothly by executing
this command and getting something like this screen output:

```
$ pbrelease --version
Package-Builder 0.22.0
```

Then see the information that `pbrelease` expects by asking for help
and getting something like this screen output:

```
$ pbrelease --help
usage: pbrelease  REPOSITORY_NAME  PACKAGE_NAME  MODEL_VERSION
                  [--help]  [--local]  [--dryrun]  [--version]

Creates conda packages named PACKAGE_NAME for the PSL model in REPOSITORY_NAME
that has a GitHub release named MODEL_VERSION. The packages are built locally
in a temporary workspace and then uploaded to the Anaconda Cloud PSLmodels
channel for public distribution. The built/uploaded packages are for Python
3.6 and Python 3.7.

positional arguments:
  REPOSITORY_NAME  Name of repository in the GitHub organization called
                   PSLmodels. Example: Tax-Calculator
  PACKAGE_NAME     Name of packages to build and upload. Example: taxcalc
  MODEL_VERSION    Model release string that has X.Y.Z semantic-versioning
                   pattern. Example: 1.0.1

optional arguments:
  -h, --help       show this help message and exit
  --local          optional flag that causes package to be built from current
                   source code and installed on local computer without
                   packages being uploaded to Anaconda Cloud PSLmodels
                   channel.
  --dryrun         optional flag that writes execution plan to stdout and
                   quits without executing plan
  --version        optional flag that writes Package-Builder release version
                   to stdout and quits
```

Once you can get this kind of `pbrelease` screen output, you're ready
to make packages for your model release.


How to use pbrelease?
---------------------

In order to use the `pbrelease` tool, you need a file containing the
Anaconda Cloud upload token for the `PSLmodels` channel.  Get that
file by asking for it in a new Package-Builder issue.  You will be
sent via private email a zip file containing the token file.  Unzip
that file in your home directory.  After doing that, the
`.pslmodels_anaconda_token` file should be in your home directory.
Now you're ready to use the `pbrelease` tool.

After testing your model and commiting to the master branch all of
your changes, create a model release on GitHub.  Then to build and
upload packages for that model release, execute this command:

```
$ pbrelease  repo_name  pkg_name  version
```

where your replace `repo_name` with the name of your model's
repository and you replace `pkg_name` with the sub-directory name
containing your model's highest level `__init__.py` file and you
replace `version` with the release for which you want to make
model packages.

Here's an example that builds and uploads packages for
Behavioral-Responses release 0.5.0:

```
$ pbrelease Behavioral-Responses behresp 0.5.0
: Package-Builder will build model packages for:
:   repository_name = Behavioral-Responses
:   package_name = behresp
:   model_version = 0.5.0
:   python_versions = ['3.6', '3.7']
: Package-Builder will upload model packages to:
:   Anaconda channel = pslmodels
:   using token in file = /Users/mrh/.pslmodels_anaconda_token
: Package-Builder is starting at Thu Mar 14 07:25:21 2019
: Package-Builder is cloning repository code for 0.5.0
...
... <an enormous amount of screen output>
...
: Package-Builder is cleaning-up
: Package-Builder is finishing at Thu Mar 14 07:27:27 2019
```

To use `pbrelease` to make a **local package** from the current (even
uncommitted) code on your current branch, make the top-level directory
of the repo's source-code tree the current working directory.  Then
use the `--local` option as shown here:

```
$ cd Tax-Calculator
$ pbrelease Tax-Calculator taxcalc 0.0.0 --local
```

This will produce a local package on your computer for testing or
validation work.  The above example specifies version 0.0.0, but you
can specify any version you want.  You can uninstall this local
package at any time using this command:

```
$ conda uninstall taxcalc --yes
```

If your model relies on packages that are not found in the default
Anaconda channels or in the PSLmodels channel, then you need to
execute the following command before using the `pbrelease` tool:

```
$ conda config --add channels CHANNEL
```

where you replace `CHANNEL` with the name of the extra channel you
want `pbrelease` to search for packages that your model relies on.
So, for example, if your model relies on a package in the `conda-forge`
channel, replace `CHANNEL` with `conda-forge` in the command above.
You need to add an extra channel only once.  You can replace
`--add channels CHANNEL` with `--remove channels CHANNEL` or replace
it with `--show channels` to manage your conda channel configuration.


What are the package-building criteria?
---------------------------------------

The `pbrelease` tool makes certain assumptions about the PSL
model's source code.  These assumptions must be met for `pbrelease` to
work correctly.  Here are the model code criteria:

(1) Model code must be compatible with Anaconda's Python 3.6 and higher

(2) Model code must be organized as follows:

```
<repo_name>               <--- TOP-LEVEL DIRECTORY (e.g., Tax-Calculator)
    setup.py
    ...
    conda.recipe          <--- SUB-DIRECTORY
        meta.yaml
        build.sh
        bld.bat
        ...
    <pkg_name>            <--- SUB-DIRECTORY (e.g., taxcalc)
        __init__.py
        ...
```

(3) The `setup.py` file must contain a line like this: `version = '0.0.0'`

(4) The `meta.yaml` file must contain a line like this: `version: 0.0.0`

(5) The `__init__.py` file must contain a line like this: `__version__ = '0.0.0'`

The best place to look at code that meets all these criteria is the
PSLmodels Behavioral-Responses repository.

Version 0.0.0 indicates the earliest version; the `pbrelease` tool will
automatically replace (in a temporary copy of your model code) the
0.0.0 with the X.Y.Z version specified when you execute `pbrelease`.
