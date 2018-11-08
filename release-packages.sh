#!/bin/bash
# Script to build locally and upload to the Anaconda Cloud conda packages
# for models in the Policy Simulation Library (PSL).
# The script uses the Package-Builder CLI, pb, to do the build/upload work.
# The script requires two command-line arguments:
#   NAME : name of the model packages to build and upload (e.g., btax)
#   TAG  : model release number (e.g., 0.2.2)
# The script can build/upload packages for two types of models:
# (1) independent models that do not depend on Tax-Calculator taxcalc;
# (2) dependent models that do depend on Tax-Calculator taxcalc, in which
#     case the latest version of taxcalc available in the Anaconda Cloud is
#     used.
# NOTE: for this script to work the NAME must be specified in
#       the get_packages function in pb/cli/config.py, and
#       the TAG must be a release in the NAME's repository.
# USAGE: ./release-packages.sh NAME TAG

DEBUG=false

# check script arguments
if [[ $# -ne 2 ]]; then
    echo "USAGE: ./release-packages.sh NAME TAG"
    exit 1
fi
NAME=$1
TAG=$2
regex="^(taxcalc|behresp|btax|ogusa)$"
if [[ ! $NAME =~ $regex ]]; then
    echo "ERROR: NAME=$NAME not recognized"
    exit 1
fi
regex="^[0-9]+\.[0-9]+\.[0-9]+$"
if [[ ! $TAG =~ $regex ]]; then
    echo "ERROR: TAG=$TAG not valid"
    exit 1
fi

# begin script execution
echo "STARTING : `date`"

echo "[$NAME] clearing-deck"

# uninstall local taxcalc package
conda list taxcalc | awk '$1~/taxcalc/{rc=1}END{exit(rc)}'
if [[ $? -eq 1 ]]; then
    conda uninstall taxcalc --yes 2>&1 > /dev/null
fi

# set pb release OPTIONS and possibly install taxcalc
if [[ "$NAME" == "taxcalc" ]]; then
    OPTIONS="--clean"
else
    OPTIONS="--clean --only-last taxcalc"
    echo "[$NAME] setting-up taxcalc"
    # install newest version of taxcalc package from the Anaconda Cloud
    conda install -c pslmodels taxcalc --yes 2>&1 > /dev/null
fi

# build and upload packages for other model that depends on taxcalc
if [[ "$DEBUG" == "true" ]]; then
    pb release $OPTIONS $NAME=$TAG
else    
    pb release $OPTIONS $NAME=$TAG 2>&1 | awk -v nstr="[$NAME]" '$1==nstr'
fi

echo "[$NAME] cleaning-up"

# uninstall taxcalc package used in building non-taxcalc packages
if [[ "$NAME" != "taxcalc" ]]; then
    conda uninstall taxcalc --yes 2>&1 > /dev/null
fi

# clean up local files created in the build+upload process
conda build purge 2> /dev/null
find ~/anaconda3/conda-bld -name "*tar.bz2" -exec rm -f {} \;
rm -rf ~/tmp/package-builder

echo "FINISHED : `date`"
exit 0
