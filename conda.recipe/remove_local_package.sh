#!/bin/bash
# USAGE: ./remove_local_package.sh
# ACTION: (1) uninstalls any installed pkgbld package (conda uninstall)
# NOTE: for those with experience working with compiled languages,
#       removing a local conda package is analogous to a "make clean" operation

# uninstall any existing pkgbld conda package
conda list pkgbld | awk '$1=="pkgbld"{rc=1}END{exit(rc)}'
if [[ $? -eq 1 ]]; then
    conda uninstall pkgbld --yes 2>&1 > /dev/null
fi

exit 0
