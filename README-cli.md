# Manage conda packages for *Tax-Calculator*, *OG-USA*, and *B-Tax*

This Python CLI replaces `build_release.sh` for building and uploading OSPC
conda packages. Instead of using environment variables to toggle the given
actions and packages, we now use subcommands for greater control. The CLI also
makes it easier to pin dependencies and build only one package at a time.

## Installation

```
git clone https://github.com/open-source-economics/policybrain-builder
cd policybrain-builder
python setup.py install
```

## Configuration

To upload packages to [anaconda.org](https://anaconda.org/), make sure you have
installed `anaconda-client` and logged into [anaconda.org](https://anaconda.org/ospc/):

```
conda install anaconda-client
anaconda login
```

The login username you give for `anaconda login` will be the user under which
the packages are uploaded on the [anaconda.org](https://anaconda.org/), for
example `psteinberg` or `ospc`.

Alternatively if you prefer not to login to anaconda-client but still want to
upload packages to anaconda.org, you can use the `OSPC_ANACONDA_TOKEN`
environment variable as an authentication argument that is passed from
`pb release` or `pb upload` to the anaconda-client's upload command (as the
`-t` argument to `anaconda`).

The environment variable `OSPC_ANACONDA_TOKEN`, if used at all, must be an
anaconda.org token valid for conda uploads and it may be the auth token string
itself (about 40 to 60 characters) or a path to a text file on local machine
that has the token as its only contents. Contact Matt Jensen
(matt.jensen@aei.org) for access to the `ospc` user if you are uploading on
behalf of Open Source Policy Center, or contact me
(Peter Steinberg - psteinberg@continuum.io) for help on using this repo.

## Usage

### Build and upload all packages (taxcalc, btax, ogusa)

To use the latest tag for each package and to use the token provided via
`~/.ospc_anaconda_token`:

```
pb release
```

To use the latest tag for each package and to use the token provided via
environment variable:

```
OSPC_ANACONDA_TOKEN="<token>" pb release
```

To use the latest tag for each package and to use the token provided via
the command line:

```
pb release --token "<token>"
```

### Build all packages (taxcalc, btax, ogusa)

This is useful for local verification.

```
pb build
```

### Only build one package with pinned dependency

This command will clone and build the `btax` package, while pinning `btax`'s
dependency for `taxcalc` to 0.9.1 without downloading `taxcalc`. This is useful
for local verification.

```
pb build --only-last taxcalc=0.9.1 btax
```

## Environment variables

  * `ANACONDA_FORCE`: Force a package upload regardless of errors (use for `release` and `upload`)
  * `OSPC_ANACONDA_CHANNEL`: Additional channel to search for packages (use for `build` and `release`)
  * `OSPC_ANACONDA_LABEL`: Add packages to a specific label (use for `release` and `upload`)
  * `OSPC_ANACONDA_TOKEN`: Authentication token (use for `release` and `upload`)
  * `OSPC_PYTHONS`: Set Python versions for building packages (use for `build` and `release`)
  * `WORKSPACE`: Directory used for cloning, building, and uploading (use for all subcommands)

## Additional Notes

Check for your packages on [anaconda.org](https://anaconda.org/ospc). Note you
may want to use the "Edit label" link on the "Files" page for your package(s)
to change a label from `dev` to `main` if you like a package and want to final
release it.
