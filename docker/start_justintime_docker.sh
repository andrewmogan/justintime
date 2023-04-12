#!/bin/bash

VOLUME_ID=1
IS_TEST=false

usage() { echo "Usage: $0 [-v <data volume id>] [-t]" 1>&2; exit 1; }

while getopts "v:t" o; do
    case "${o}" in
        v)
            VOLUME_ID=${OPTARG}
            ;;
        t)
            IS_TEST=true
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

BASE_PORT=18000
JINT_TAG=$(git describe --tags --exact-match 2> /dev/null \
  || git symbolic-ref -q --short HEAD \
  || git rev-parse --short HEAD)
DCKR_IMG=justintime:${JINT_TAG}
CHANNEL_MAP_NAME=VDColdbox

DATA_PATH="/data${VOLUME_ID}"
INSTANCE_NAME="justintime-data${VOLUME_ID}"
INSTANCE_PORT=$((VOLUME_ID+BASE_PORT))

if [[ "$IS_TEST" == "true" ]]; then
    DATA_PATH="${DATA_PATH}/test"
    INSTANCE_NAME="${INSTANCE_NAME}-test"
    INSTANCE_PORT=$((INSTANCE_PORT+1000))

fi


DCKR_OPTS="
    -it \
    --rm \
    -v /cvmfs/dunedaq.opensciencegrid.org:/cvmfs/dunedaq.opensciencegrid.org:ro \
    -v /cvmfs/dunedaq-development.opensciencegrid.org:/cvmfs/dunedaq-development.opensciencegrid.org:ro"


DCKR_RUN_CMD="docker run -d \
    --name ${INSTANCE_NAME} \
    ${DCKR_OPTS} \
    -v ${DATA_PATH}:/data:ro \
    -w /dunedaq/ \
    -p ${INSTANCE_PORT}:8001 \
    ${DCKR_IMG} ${CHANNEL_MAP_NAME} \
    "

echo ${DCKR_RUN_CMD}
${DCKR_RUN_CMD}