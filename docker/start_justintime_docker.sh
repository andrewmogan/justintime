VOLUME_ID=2
IS_TEST=true
BASE_PORT=18000
DCKR_IMG=justintime:v0.3.1
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