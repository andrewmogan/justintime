#!/bin/bash
usage() {
    echo "Usage: $0 <dune|fd|nd>daq-<version>-<a9|c8>"
    echo "where the <version> format is vX.Y.Z"
    exit 1
}

if [ "$#" -ne 1 ]; then
    echo "You must provide a release name as a single argument"
    usage
fi

DUNEDAQ_RELEASE=$1
#if [[ "$DUNEDAQ_RELEASE" =~ ^(fd|nd)daq-v4.3.0-a9 ]]; then
#    DBT_CREATE_OPTS=""
#    DBT_VERSION=$DUNEDAQ_RELEASE
if [[ "$DUNEDAQ_RELEASE" = *"rc-"* ]]; then
    DBT_CREATE_OPTS="-b candidate"
fi

# Parse necessary dbt version from the release symbolic link
DBT_DIR=/cvmfs/dunedaq.opensciencegrid.org/tools/dbt/
if [ -e ${DBT_DIR}/$1 ]; then
    DBT_VERSION=$(readlink -f ${DBT_DIR}/$1 | rev | cut -d'/' -f1 | rev)
    echo "DBT version for $RELEASE: $DBT_VERSION"
else
    echo "Error: Symbolic link not found for $1 in $DBT_DIR."
    exit 1
fi

source /cvmfs/dunedaq.opensciencegrid.org/setup_dunedaq.sh
echo "------------------------------------------"
echo "Loading daq-buildtool environment"
echo "------------------------------------------"
echo "DBT version: $DBT_VERSION"
setup_dbt ${DBT_VERSION}

echo "------------------------------------------"
echo "Loading daq-release workarea"
echo "------------------------------------------"
dbt-create ${DBT_CREATE_OPTS} ${DUNEDAQ_RELEASE} dunedaq-area

cd dunedaq-area
source ./env.sh

# Save environment filtering out read-only vars
declare -p | grep -v 'declare -[^ ]*r[^ ]* ' > quick_env.sh
