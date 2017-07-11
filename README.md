# Build conda packages for *Tax-Calculator*, *OG-USA*, and *B-Tax*

Build conda packages and automatically upload them to anaconda.org

The snippet at the bottom shows how to run the script.  Here are some environment variables for controlling it.

## Environment variables

By default it builds Tax-Calculator, B-Tax and OG-USA.  Use the following env vars to control if one or more of those is skipped:
 * `SKIP_TAXCALC`: TYPICALLY DO NOT `SKIP_TAXCALC` - it causes OG-USA and B-Tax to be pinned to wrong version
 * `SKIP_OGUSA`: if this is set to anything then skip OG-USA build
 * `SKIP_BTAX`: if this is set to anything then skip B-Tax build

To just build packages with `conda build` and *not* upload them to [anaconda.org](https://anaconda.org/)
 * `SKIP_ANACONDA_UPLOAD`: if this is set to anything, then build but do not anaconda upload

To upload packages to [anaconda.org](https://anaconda.org/) make sure you have installed `anaconda-client` and logged into [anaconda.org](https://anaconda.org/ospc/):

```
conda install anaconda-client
anaconda login
```
The login username you give for `anaconda login` will be the user under which the packages are uploaded on the [anaconda.org](https://anaconda.org/), for example `psteinberg` or `ospc`.  Alternatively if you prefer not to login to anaconda-client but still want to upload packages to anaconda.org, you can use the `OSPC_UPLOAD_TOKEN` environment variable as an authentication argument that is passed from `build_release.sh` to the anaconda-client's upload command (as the `-t` argument to `anaconda`).  The environment variable `OSPC_UPLOAD_TOKEN`, if used at all, must be an anaconda.org token valid for conda uploads and it may be the auth token string itself (about 40 to 60 characters) or a path to a text file on local machine that has the token as its only contents. Contact Matt Jensen (matt.jensen@aei.org) for access to the `ospc` user if you are uploading on behalf of Open Source Policy Center, or contact me (Peter Steinberg - psteinberg@continuum.io) for help on using this repo.

By default the `build_release.sh` script will clone from the [https://github.com/open-source-economics](https://github.com/open-source-economics) the master branches of each of the 3 repos, then fetch the tags.  

Control which versions of Python are built:
 * `export OSPC_PYTHONS="2.7 3.5 3.6";`
 * By default it builds for `2.7 3.5 3.6` and may error out on some

Another environment variable is `OSPC_ANACONDA_CHANNEL` this controls whether you are uploading to the `dev` or `main` label within your anaconda.org account.  A package labeled as `dev` is not installed by conda by default even if it is the highest version available.  Here's how to install from a `dev` labeled package within the `ospc` account:
```
conda install -c ospc/label/dev taxcalc ogusa btax
```
While most users for most usages of the package will use the `main` label by default:
```
conda install -c ospc taxcalc ogusa btax
```
## Running `build_release.sh`
After setting the environment variables described above, as needed, run `build_release.sh`:
```
git clone https://github.com/open-source-economics/policybrain-builder
conda install anaconda-client
cd policybrain-builder
. ./build_release.sh
```

Check for your packages on [anaconda.org](https://anaconda.org/ospc) . Note you may want to use the "Edit label" link on the "Files" page for your package(s) to change a label from `dev` to `main` if you like a package and want to final release it.
