# Prepare for testing.

function oops {
	echo
	echo '*** Oops *** '$1' !! ***'
	echo
	exit 86
}

set -e

URL='DUMMY'
BRANCH='DUMMY'

export CUDA_PATH=/usr/local/cuda 

if [ $URL == 'DUMMY' ]; then
	echo
	echo Edit URL first \!\!
	echo
	exit 86
fi

if [ $BRANCH == 'DUMMY' ]; then
	echo
	echo Edit BRANCH first \!\!
	echo
	exit 86
fi

cd $HOME
if [ -d rawspec ]; then
    rm -rf rawspec
fi
git clone -b $BRANCH $URL
if [ $? -ne 0 ]; then
    oops 'git clone FAILED'
fi
cd rawspec
make
if [ $? -ne 0 ]; then
    oops 'make FAILED'
fi

