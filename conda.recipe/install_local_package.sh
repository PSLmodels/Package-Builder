#!/bin/bash
# USAGE: ./install_local_package.sh
# ACTION: (1) uninstalls any installed package (remove_local_package.sh)
#         (2) executes "conda install conda-build" (if necessary)
#         (3) builds local pkgbld=0.0.0 package (conda build)
#         (4) installs local package (conda install)
# NOTE: for those with experience working with compiled languages,
#       building a local conda package is analogous to compiling an executable

echo "STARTING : `date`"

echo "BUILD-PREP..."

# uninstall any installed package
./remove_local_package.sh

# check version of conda package
conda list conda | awk '$1=="conda"{v=$2;gsub(/\./,"",v);nv=v+0;if(nv<444)rc=1}END{exit(rc)}'
if [[ $? -eq 1 ]]; then
    echo "==> Installing conda 4.4.4+"
    conda install conda>=4.4.4 --yes 2>&1 > /dev/null
    echo "==> Continuing to build new pkgbld package"
fi

# install conda-build package if not present
conda list build | awk '$1~/conda-build/{rc=1}END{exit(rc)}'
if [[ $? -eq 0 ]]; then
    echo "==> Installing conda-build package"
    conda install conda-build --yes 2>&1 > /dev/null
    echo "==> Continuing to build new pkgbld package"
fi

# build conda package for this version of Python
NOHASH=--old-build-string
pversion=3.6
conda build $NOHASH --python $pversion . 2>&1 | awk '$1~/BUILD/||$1~/TEST/'

# install conda package
echo "INSTALLATION..."
conda install pkgbld=0.0.0 --use-local --yes 2>&1 > /dev/null
# NOTE: the --use-local option was broken by conda 4.4.0 and fixed by 4.4.4
# NOTE: see https://github.com/conda/conda/issues/6520
# NOTE: interim usage was as follows:
# NOTE: conda install -c local pkgbld=0.0.0 --yes 2>&1 > /dev/null

# clean-up after package build
echo "CLEAN-UP..."
conda build purge 2> /dev/null
topdir=$(git rev-parse --show-toplevel)
pushd $topdir > /dev/null
rm -rf build/*
rmdir build/
rm -rf dist/*
rmdir dist/
rm -rf pkgbld.egg-info/*
rmdir pkgbld.egg-info/
popd > /dev/null

echo "FINISHED : `date`"
exit 0
