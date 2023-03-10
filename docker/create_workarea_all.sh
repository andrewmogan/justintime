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

echo "------------------------------------------"
echo "Clone DUNE-DAQ packages"
echo "------------------------------------------"
cd dunedaq-area/sourcecode
git clone https://github.com/DUNE-DAQ/detchannelmaps.git -b thea/inverse_map
cd ../

source env.sh
dbt-build

echo "------------------------------------------"
echo "Clone Just-in-Time"
echo "------------------------------------------"
cd ../../
git clone https://github.com/DUNE-DAQ/justintime.git -b ${JINT_BRANCH}
cd justintime
pip install -r requirements.txt

