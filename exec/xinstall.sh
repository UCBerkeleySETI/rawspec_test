# Prepare for testing.

function oops {
	echo
	echo '*** Oops *** '$1' !! ***'
	echo
	exit 86
}

set -e

HERE=`pwd`
URL='https://github.com/UCBerkeleySETI/rawspec'
BRANCH='master'
PYOPTS='-U -g 3'

export CUDA_PATH=/usr/local/cuda 
export PATH=$HOME/rawspec:$PATH

# Install the baseline github copy of rawspec
echo
cd $HOME
if [ -d rawspec ]; then
    rm -rf rawspec
fi
git clone -b $BRANCH $URL
if [ $? -ne 0 ]; then
    oops 'git clone FAILED'
fi

# Make the baseline github copy of rawspec
echo
cd rawspec
make
if [ $? -ne 0 ]; then
    oops 'make FAILED'
fi

# Run the installer script.
echo
cd $HERE
pwd
python3 installer.py $PYOPTS

