
DCKR_BUILD_HERE:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DST_AREA=${DCKR_BUILD_HERE}/workarea
DCKR_BASE_IMG=ghcr.io/dune-daq/c8-minimal:latest
DUNEDAQ_RELEASE=v3.2.2
DCKR_TAG=justintime
JINT_BRANCH=$(shell git describe --tags --exact-match 2> /dev/null \
  || git symbolic-ref -q --short HEAD \
  || git rev-parse --short HEAD)
DCKR_VERSION=${JINT_BRANCH}

DCKR_OPTS=--user $(shell id -u):$(shell id -g) \
    -it \
    --rm \
    -v /etc/passwd:/etc/passwd:ro -v /etc/group:/etc/group:ro \
    -v /cvmfs/dunedaq.opensciencegrid.org:/cvmfs/dunedaq.opensciencegrid.org:ro \
    -v /cvmfs/dunedaq-development.opensciencegrid.org:/cvmfs/dunedaq-development.opensciencegrid.org:ro


connection-check: ## Check that GPN connection is available
	@curl  --connect-timeout 1 github.com &> /dev/null
	

.PHONY: all
all: connection-check  workarea gits dunedaq justintime image ## Build all targets

.PHONY: workarea ## Create dunedaq work area
workarea:
	@echo "------------------------------------------"
	@echo "🚧 Creating new  workarea 🚧"
	@echo "------------------------------------------"
	mkdir -p ${DST_AREA}
	docker run ${DCKR_OPTS} \
	    -v /nfs:/nfs:ro \
	    -v ${DST_AREA}:/dunedaq/run:z \
	    -v ${DCKR_BUILD_HERE}/create_workarea.sh:/dunedaq/bin/create_workarea.sh \
	    ${DCKR_BASE_IMG} \
	    -c "export PATH=\"/dunedaq/bin/:$$PATH\"; cd /dunedaq/run; create_workarea.sh ${DUNEDAQ_RELEASE}"

${DST_AREA}/dunedaq-area/sourcecode/detchannelmaps: connection-check
	git -C ${DST_AREA}/dunedaq-area/sourcecode/ clone https://github.com/DUNE-DAQ/detchannelmaps.git -b thea/inverse_map

${DST_AREA}/justintime: connection-check
	git -C ${DST_AREA} clone https://github.com/DUNE-DAQ/justintime.git -b ${JINT_BRANCH}

.PHONY: dunedaq 
dunedaq: ## Build extra dunedaq packages
	@echo "------------------------------------------"
	@echo "🛠 Building work area 🛠"
	@echo "------------------------------------------"
	docker run ${DCKR_OPTS} \
		-v ${DST_AREA}:/dunedaq/run:z \
		-w /dunedaq/run/dunedaq-area \
		${DCKR_BASE_IMG} \
		-c "source ./quick_env.sh; dbt-build"

.PHONY: justintime
justintime: ## Install just-in-time extra python packages
	@echo "------------------------------------------"
	@echo "🐍 Installing extra python packages 🐍"
	@echo "------------------------------------------"
	@docker run ${DCKR_OPTS} \
		-v /nfs:/nfs:ro \
		-v ${DST_AREA}:/dunedaq/run:z \
		--env HTTP_PROXY=${HTTP_PROXY} \
		--env HTTPS_PROXY=${HTTPS_PROXY} \
		--env NO_PROXY=${NO_PROXY} \
		-w /dunedaq/ \
		${DCKR_BASE_IMG} \
		-c "cd run/dunedaq-area; source quick_env.sh; cd ../justintime; pip install -r requirements.txt"

image: ## Build docker image
	@echo "------------------------------------------"
	@echo "📦 Building image 📦"
	@echo "------------------------------------------"
	set -x
	docker buildx build --tag ${DCKR_TAG}:${DCKR_VERSION} --tag ${DCKR_TAG}:latest ${DCKR_BUILD_HERE} 

.PHONY: clean
clean:
	@echo "------------------------------------------"
	@echo "🧹 Clearing old workarea 🧹"
	@echo "------------------------------------------"
	rm -rf ${DST_AREA}

.PHONY: gits
gits: ${DST_AREA}/dunedaq-area/sourcecode/detchannelmaps ${DST_AREA}/justintime

.PHONY: help
help: ## Display this help
	@IFS=$$'\n'; for line in `grep -h -E '^[a-zA-Z_#-]+:?.*?## .*$$' $(MAKEFILE_LIST)`; do if [ "$${line:0:2}" = "##" ]; then \
	echo $$line | awk 'BEGIN {FS = "## "}; {printf "\n\033[33m%s\033[0m\n", $$2}'; else \
	echo $$line | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'; fi; \
	done; unset IFS;


.PHONY: info
info: 
	@echo just-in-time tag/branch/hash: ${JINT_BRANCH}