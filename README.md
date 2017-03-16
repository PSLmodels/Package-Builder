# Build conda packages for *Tax-Calculator*, *OG-USA*, and *B-Tax*

Build conda packages and automatically upload them to anaconda.org

The snippet at the bottom shows how to run the script.  Here are some environment variables for controlling it:


By default it builds Tax-Calculator, B-Tax and OG-USA.  Use the following env vars to control if one or more of those is skipped:
 * `SKIP_TAXCALC`: if this is set to anything then skip Tax-Calculator build
 * `SKIP_OGUSA`: if this is set to anything then skip OG-USA build
 * `SKIP_BTAX`: if this is set to anything then skip B-Tax build

To just build packages with `conda build` and *not* upload them to [anaconda.org](https://anaconda.org/)
 * `SKIP_ANACONDA_UPLOAD`: if this is set to anything, then build but do not anaconda upload

To upload packages to [anaconda.org](https://anaconda.org/) make sure you have installed `anaconda-client` and logged into [anaconda.org](https://anaconda.org/ospc/):

```
conda install anaconda-client
anaconda login
```
The login username you give for `anaconda login` will be the user under which the packages are uploaded on the [anaconda.org](https://anaconda.org/), for example `psteinberg` or `ospc`.  Contact Matt Jensen (matt.jensen@aei.org) for access to the `ospc` user if you are uploading on behalf of Open Source Policy Center.

By default the `build_release.sh` script will clone from the [https://github.com/open-source-economics](https://github.com/open-source-economics) the master branches of each of the 3 repos, then fetch the tags.  Alternatively, the following environment variables can control pulling from an a personal fork of a repo:

 * `export OSPC_REPOS="https://github.com/open-source-economics"`
 * `export BTAX_REPO="${OSPC_REPOS}/B-Tax"`
 * `export TAXCALC_REPO="${OSPC_REPOS}/Tax-Calculator"`
 * `export OGUSA_REPO="${OSPC_REPOS}/OG-USA"`

To build from a local cloned directory, skip the logic above regarding `BTAX_REPO` and other `_REPO` env vars and define one or more of these:

 * `BTAX_CLONE`: directory where you have cloned B-Tax
 * `TAXCALC_CLONE`: directory where you have cloned Tax-Calculator
 * `OGUSA_CLONE`: directory where you have cloned OG-USA

Control which versions of Python are built:
 * `export OSPC_PYTHONS="2.7 3.4 3.5 3.6";`
 * By default it builds for `2.7 3.4 3.5 3.6` and may error out on some


```
git clone https://github.com/open-source-economics/policybrain-builder
conda install anaconda-client
cd policybrain-builder
. ./build_release.sh
```

Check for your packages on [anaconda.org](https://anaconda.org/ospc)