#!/bin/bash
source deactivate
export ORIGINAL_DIR=`pwd`
conda config --set always_yes true
export CONDA_BUILD_DEFAULT_DIR="$(dirname $(dirname $(which python)))/conda-bld"
export OSPC_REPOS="http://github.com/open-source-economics"
export BTAX_REPO="${OSPC_REPOS}/B-Tax"
export TAXCALC_REPO="${OSPC_REPOS}/Tax-Calculator"
export OGUSA_REPO="${OSPC_REPOS}/OG-USA"
if [ "$WORKSPACE" = "" ];then
    export WORKSPACE="/tmp";
fi

export PKGS_TO_UPLOAD=$WORKSPACE/code
export OSPC_CLONE_DIR=$WORKSPACE/ospc_clones

mkdir -p $PKGS_TO_UPLOAD
rm -rf $PKGS_TO_UPLOAD/*
mkdir -p $OSPC_CLONE_DIR
rm -rf $OSPC_CLONE_DIR/*

msg(){
    echo \#\#\#\#\#\#\#\# STATUS \#\# $* \#\#\#\#\#\#\#\# \#\#\#\#\#\#\#\#;
}
msg Build for Python $OSPC_PYTHONS
check_anaconda(){
    if [ "$OSPC_UPLOAD_TOKEN" = "" ];then
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
    fi
    return 0;
}
clone(){
    cd $OSPC_CLONE_DIR && rm -rf $3;
    msg From $OSPC_CLONE_DIR Clone $1 to $3;
    export "$2_CLONE=${OSPC_CLONE_DIR}/$3";
    git clone $1 && cd $3 || return 1;
    return 0;
}
fetch_checkout(){
    msg cd $1;
    cd $1 || return 1;
    msg git fetch origin;
    git fetch origin;
    git fetch origin --tags;
    export latest_tag=$(git describe --abbrev=0 --tags);
    if [ "$TAXCALC_TAG" = "" ];then
        echo
    else
        pwd | grep Tax-Calculator && export latest_tag=$TAXCALC_TAG
    fi
    export "$2_TAG"="$latest_tag";
    msg Git Checkout $latest_tag;
    git checkout $latest_tag || return 1;
    msg Git Archive ${PKGS_TO_UPLOAD}/$3.tar;
    git archive --prefix=$3/ -o $PKGS_TO_UPLOAD/$3.tar $latest_tag || return 1;
}
clone_all(){
    if [ "$SKIP_TAXCALC" = "" ];then
        msg Tax-Calculator - $TAXCALC_REPO
        clone $TAXCALC_REPO TAXCALC Tax-Calculator || return 1;
        msg $TAXCALC_CLONE
        fetch_checkout $TAXCALC_CLONE TAXCALC Tax-Calculator || return 1;
    fi
    if [ "$SKIP_BTAX" = "" ];then
        clone $BTAX_REPO BTAX B-Tax || return 1;
        fetch_checkout $BTAX_CLONE BTAX B-Tax || return 1;
    fi
    if [ "$SKIP_OGUSA" = "" ];then
        clone $OGUSA_REPO OGUSA OG-USA || return 1;
        fetch_checkout $OGUSA_CLONE OGUSA OG-USA || return 1;
    fi
}

anaconda_upload(){
    cd $PKGS_TO_UPLOAD || return 1;
    export ret=0;
    export version=$2;
    export pkg=$3;

    if [ "$OSPC_ANACONDA_CHANNEL" = "" ];then
        export OSPC_ANACONDA_CHANNEL=dev;
    fi
    export file_exists=0;
    if [ "$ANACONDA_FORCE" = "" ];then
        export force=""
    else
        export force=" --force "
    fi
    if [ "$SKIP_ANACONDA_UPLOAD" = "" ];then
        msg From $PKGS_TO_UPLOAD as pwd;
        if [ "$OSPC_UPLOAD_TOKEN" = "" ];then
            msg anaconda upload $force --no-progress $1 --label $OSPC_ANACONDA_CHANNEL;
            anaconda upload $force  --no-progress $1 --label $OSPC_ANACONDA_CHANNEL || export ret=1;
        else
            msg anaconda -t TOKEN_REDACTED_BUT_PRESENT upload $force  --no-progress $1 --label $OSPC_ANACONDA_CHANNEL ;
            anaconda -t $OSPC_UPLOAD_TOKEN upload $force  --no-progress $1 --label $OSPC_ANACONDA_CHANNEL || export ret=1;
        fi
    else
        msg Would have done - anaconda upload  $force --no-progress $1 --label $OSPC_ANACONDA_CHANNEL || export ret=1;
    fi
    cd $OLDPWD || return 1;
    if [ "$ret" = "1" ];then
        msg Failed on anaconda upload likely because version already exists - continuing;
    fi
    return $ret;
}
convert_packages(){
    export build_file=$1;
    export version=$2;
    export pkg=$3;
    export tc_string="taxcalc-${TAXCALC_TAG}";
    cd $PKGS_TO_UPLOAD || return 1;
    msg Convert $build_file for platforms;
    msg conda convert -p all $build_file -o .;

    conda convert -p all $build_file -o . || return 1;
    for platform in win-32 win-64 linux-64 linux-32 osx-64; do
        ls -lrth
        export fname=$(ls ./${platform}/*-${version}-*.tar.bz2);
        msg Upload $fname
        ls $fname && anaconda_upload ${fname} "${version}" $pkg || return 1;
    done
    anaconda_upload $build_file || return 1;
    return 0;
}
replace_version(){
    replacement=$1;
    grepper=$2;
    old_ifs="$IFS";
    IFS='' ; while read line ;do echo "$line" | grep $grepper && echo "$replacement" >> meta2.yaml  || echo "$line" >> meta2.yaml  ; done < meta.yaml
    IFS=$old_ifs;
    mv meta2.yaml meta.yaml;
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
    replacement="  version: $2";
    cd ${USE_PYTHON_RECIPE} && replace_version "$replacement" version  || return 1;
    export is_ogusa=0;
    export is_btax=0;
    echo $1 | grep OG-USA && export is_ogusa=1;
    echo $1 | grep B-Tax && export is_btax=1;
    export replacement="    - taxcalc >=${TAXCALC_TAG}";
    if [ "$is_ogusa" = "1" ];then
        replace_version "$replacement" taxcalc;
        echo OGUSA CHANGED META: $(cat meta.yaml);
        export BUILDING_PKG=ogusa;
    elif [ "$is_btax" = "" ];then
        replace_version "$replacement" taxcalc;
        echo B-Tax CHANGED META: $(cat meta.yaml);
        export BUILDING_PKG=btax;
    else
        export BUILDING_PKG=taxcalc;
        echo Tax-Calculator CHANGED META: $(cat meta.yaml)
    fi
    cd ${PKGS_TO_UPLOAD}/$1 || return 1;
    msg RUN: conda build --use-local --python $python_version ${USE_PYTHON_RECIPE};
    conda build -c ospc --python $python_version ${USE_PYTHON_RECIPE} || return 1;
    msg RUN: conda convert packages for python $python_version;
    convert_packages "$(conda build --python $python_version ${USE_PYTHON_RECIPE} --output)" ${2} $1 || return 1;
    return 0;
}

build_all_pkgs(){
    if [ "${OSPC_PYTHONS}" = "" ];then
        return 1;
    fi

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
