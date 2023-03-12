DUNEDAQ_RELEASE=$1

echo "------------------------------------------"
echo "Setting up spack python"
echo "------------------------------------------"
source /cvmfs/dunedaq.opensciencegrid.org/spack/externals/stable/spack-0.18.1-gcc-12.1.0/spack-installation/share/spack/setup-env.sh
spack load python@3.10.4

source /cvmfs/dunedaq.opensciencegrid.org/setup_dunedaq.sh

echo "------------------------------------------"
echo "Loading daq-buildtool environment"
echo "------------------------------------------"
setup_dbt dunedaq-${DUNEDAQ_RELEASE}


echo "------------------------------------------"
echo "Loading daq-release workarea"
echo "------------------------------------------"
dbt-create   dunedaq-${DUNEDAQ_RELEASE} dunedaq-area

cd dunedaq-area
source ./env.sh

# Save environment filtering out read-only vars
declare -p | grep -v 'declare -[^ ]*r[^ ]* ' > quick_env.sh
