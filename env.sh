#------------------------------------------------------------------------------
HERE=$(cd $(dirname $(readlink -f ${BASH_SOURCE})) && pwd)

export PYTHONPATH="${HERE}/src:${PYTHONPATH}"
export PATH="${HERE}/test:${PATH}"
