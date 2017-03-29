#!/bin/bash
set -x
source deactivate
export ORIGINAL_DIR=`pwd`
conda config --set always_yes true
export CONDA_BUILD_DEFAULT_DIR="$(dirname $(dirname $(which python)))/conda-bld"
export OSPC_REPOS="http://github.com/open-source-economics"
export BTAX_REPO="${OSPC_REPOS}/B-Tax"
export TAXCALC_REPO="${OSPC_REPOS}/Tax-Calculator"
export OGUSA_REPO="${OSPC_REPOS}/OG-USA"
if [ "${OSPC_PYTHONS}" = "" ];then
    export OSPC_PYTHONS="2.7 3.4 3.5 3.6";
fi

if [ "$PKGS_TO_UPLOAD" = "" ];then
    export PKGS_TO_UPLOAD=~/code;
fi
if [ "$OSPC_CLONE_DIR" = "" ];then
    export OSPC_CLONE_DIR=~/ospc_clones;
fi

mkdir -p $PKGS_TO_UPLOAD
rm -rf $PKGS_TO_UPLOAD/*
mkdir -p $OSPC_CLONE_DIR

msg(){
    echo \#\#\#\#\#\#\#\# STATUS \#\# $* \#\#\#\#\#\#\#\# \#\#\#\#\#\#\#\#;
}
msg Build for Python $OSPC_PYTHONS
check_anaconda(){
    export IS_ANON=0;
    msg Check if anaconda-client has been conda installed
    which anaconda || return 1;
    msg Check whether logged into Anaconda client
    anaconda whoami | grep -i anonymous && export IS_ANON=1;
    if [ "$IS_ANON" = "1" ];then
        if [ "$SKIP_ANACONDA_UPLOAD" = "" ];then
            msg Cannot upload packages when anaconda user is anonymous or you did not do conda install anaconda-client and anaconda login;
            return 1;
        fi
    fi
    msg Logged into anaconda
    return 0;
}
clone(){
    cd $OSPC_CLONE_DIR && rm -rf $1;
    msg From $OSPC_CLONE_DIR Clone $1;
    export "$2_CLONE=${OSPC_CLONE_DIR}/$3";
    ls $3 && return 0;
    git clone $1 && cd $3 || return 1;
    return 0;
}
fetch_checkout(){
    msg cd $1;
    cd $1 || return 1;
    msg git fetch origin;
    git fetch origin;
    export latest_tag=$(git describe --abbrev=0 --tags)
    export "$2_TAG"="$latest_tag";
    msg Git Checkout $latest_tag
    git checkout $latest_tag || return 1;
    msg Git Archive ${PKGS_TO_UPLOAD}/$3.tar
    git archive --prefix=$3/ -o $PKGS_TO_UPLOAD/$3.tar $latest_tag || return 1;
}
clone_all(){
    if [ "$SKIP_TAXCALC" = "" ];then
        ls $TAXCALC_CLONE/setup.py || clone $TAXCALC_REPO TAXCALC Tax-Calculator || return 1;
        fetch_checkout $TAXCALC_CLONE TAXCALC Tax-Calculator || return 1;
    fi
    if [ "$SKIP_BTAX" = "" ];then
        ls $BTAX_CLONE/setup.py || clone $BTAX_REPO BTAX B-Tax || return 1;
        fetch_checkout $BTAX_CLONE BTAX B-Tax || return 1;
    fi
    if [ "$SKIP_OGUSA" = "" ];then
        ls $OGUSA_CLONE/setup.py || clone $OGUSA_REPO OGUSA OG-USA || return 1;
        fetch_checkout $OGUSA_CLONE OGUSA OG-USA || return 1;
    fi
}

anaconda_upload(){
    cd $PKGS_TO_UPLOAD || return 1;
    export ret=0;
    if [ "$SKIP_ANACONDA_UPLOAD" = "" ];then
        msg From $PKGS_TO_UPLOAD as pwd;
        msg anaconda upload --force $1;
        anaconda upload --force $1 || export ret=1;
    else
        msg Would have done - anaconda upload --force $1 || export ret=1;
    fi
    cd $OLDPWD || return 1;
    return $ret;
}
convert_packages(){
    export build_file=$1;
    export version=$2;
    cd $PKGS_TO_UPLOAD || return 1;
    msg Convert $build_file for platforms;
    if [ "$OSPC_PLATFORMS" = "" ];then
        export OSPC_PLATFORMS="win-32 win-64 linux-64 linux-32 osx-64";
    fi
    for platform in $OSPC_PLATFORMS;do
        msg conda convert -p $platform $build_file -o .
        conda convert -p $platform $build_file -o . || return 1;
    done
    for platform in $OSPC_PLATFORMS; do
        anaconda_upload ./${platform}/*-${version}-*.tar.bz2 || return 1;
    done
    anaconda_upload $build_file || return 1;
    return 0;
}

build_one_pkg(){
    msg cd $PKGS_TO_UPLOAD
    cd $PKGS_TO_UPLOAD || return 1;
    msg Check for $1.tar
    ls $1.tar || return 1;
    msg Untar $1.tar
    tar xvf $1.tar || return 1;
    msg cd $1;
    cd $1 || return 1;
    ls conda.recipe && export USE_PYTHON_RECIPE="conda.recipe" || export USE_PYTHON_RECIPE="Python/conda.recipe";
    export python_version=$3;
    msg Replace version string from ${USE_PYTHON_RECIPE}/meta.yaml;
    cd ${USE_PYTHON_RECIPE} && sed -i '' 's/version: .*/version: '${2}'/g' meta.yaml && cd ${PKGS_TO_UPLOAD}/$1 || return 1;
    msg RUN: conda build -c ospc --python $python_version ${USE_PYTHON_RECIPE};
    conda build -c ospc --python $python_version ${USE_PYTHON_RECIPE} || return 1;
    msg RUN: conda convert packages for python $python_version;
    convert_packages "$(conda build --python $python_version ${USE_PYTHON_RECIPE} --output)" ${2} || return 1;
    return 0;
}

build_all_pkgs(){
    check_anaconda || return 1;
    clone_all || return 1;
    for python_version in ${OSPC_PYTHONS};do
        msg STARTING BUILDS FOR PYTHON ${python_version};
        if [ "$SKIP_TAXCALC" = "" ];then
            build_one_pkg Tax-Calculator $TAXCALC_TAG $python_version || return 1;
        fi
        if [ "$SKIP_OGUSA" = "" ];then
            if [ "$python_version" = "2.7" ];then
                build_one_pkg OG-USA $OGUSA_TAG $python_version || return 1;
            fi
        fi
        if [ "$SKIP_BTAX" = "" ];then
            build_one_pkg B-Tax $BTAX_TAG $python_version || return 1;
        fi
        msg FINISHED BUILDS FOR PYTHON ${python_version};
    done
    return 0;
}

build_all_pkgs && msg && echo OK || echo FAILED
cd $ORIGINAL_DIR
