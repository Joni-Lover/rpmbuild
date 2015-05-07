#!/bin/bash -x
#===============================================================================
#
#          FILE: build-rpm.sh
#
#         USAGE: ./build-rpm.sh program.spec 6
#
#   DESCRIPTION: Download all Source from spec file, build srpm without
#                dependency and build rpm binary with mock
#
#       OPTIONS: name of spec, version of centos
#  REQUIREMENTS: flock, spectools, mock, rpmbuild
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Polonevich Ivan
#  ORGANIZATION:
#       CREATED: 05/07/2015 10:22
#      REVISION:  001
#===============================================================================

set -o nounset                               # Treat unset variables as an error

if [[ -z "$1" ]] || [[ -z "$2" ]]; then
    echo "Not specified spec or release (5 6 7 all) as script argument!" >&2
    echo "example: `basename $0` nginx.spec 5"
    exit 1
fi

SPEC=$1
RELEASE=$2
readonly SPEC_DIR="/home/mockbuild/rpmbuild/SPECS"
readonly LOCKFILE_DIR='/tmp'
readonly PROGNAME=$(basename "$0")
readonly LOCK_FD=200

lock() {
    local prefix=$1
    local fd=${2:-$LOCK_FD}
    local lock_file=$LOCKFILE_DIR/$prefix.lock

    # create lock file
    eval "exec $fd>$lock_file"

    # acquier the lock
    flock -n $fd \
        && return 0 \
        || return 1
}
eexit() {
    local error_str="$@"

    echo $error_str
    exit 1
}
main () {
    lock $PROGNAME || eexit "Only one instance of $PROGNAME can run at one time."

    if [ $RELEASE == 5 ]; then
        RPM_PACKAGE_NAME=$(rpmbuild --define "rhel 5" --define "_source_filedigest_algorithm md5" --define "_binary_filedigest_algorithm md5" --nodeps -bs ${SPEC_DIR}/${SPEC} | awk {'print $2'})
        echo el5
    else
        RPM_PACKAGE_NAME=$(rpmbuild --nodeps -bs $OPT ${SPEC_DIR}/${SPEC} | awk {'print $2'})
    fi

    spectool  -R -g ${SPEC_DIR}/${SPEC}

    case $RELEASE in
        5 ) REL='centos-5-x86_64'; flag=0 ;;
        6 ) REL='centos-6-x86_64'; flag=0;;
        7 ) REL='centos-7-x86_64'; flag=0;;
        all ) flag=1;;
        * ) echo "choose only 5, 6, 7 or all releases"
    esac

    if [ $flag -eq 1 ]; then
        for REL in centos-5-x86_64 centos-6-x86_64 centos-7-x86_64; do
            setarch x86_64 mock -r $REL $RPM_PACKAGE_NAME
        done
    else
        setarch x86_64 mock -r $REL $RPM_PACKAGE_NAME
    fi
}
main
