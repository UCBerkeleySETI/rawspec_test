# Package rawspec_testing
# Prepare the baseline directory for testing.

HERE=`pwd`
LOG=${HERE}/`basename $0`.log
> $LOG # Make the log nil.
set -e
set -o pipefail

function oops {
	echo
	echo '*** Oops *** '$1' !! ***' 2>&1 | tee -a $LOG
	echo
	exit 86
}

HERE=`pwd`
URL='https://github.com/UCBerkeleySETI/rawspec'
BRANCH='master'
PYOPTS='-g 3'

export CUDA_PATH=/usr/local/cuda 
export PATH=$HOME/rawspec:$PATH

# Install the baseline github copy of rawspec
echo 2>&1 | tee -a $LOG
cd $HOME
if [ -d rawspec ]; then
	MSG='Removing old copy of rawspec .....'
	echo $MSG 2>&1 | tee -a $LOG
    rm -rf rawspec 2>&1 | tee -a $LOG
else
	MSG='No pre-existing copy of rawspec present.'
	echo $MSG 2>&1 | tee -a $LOG
fi
echo 2>&1 | tee -a $LOG
MSG='git clone from URL '$URL', branch '$BRANCH' .....'
echo $MSG 2>&1 | tee -a $LOG
git clone -b $BRANCH $URL
if [ $? -ne 0 ]; then
    oops 'git clone FAILED'
fi

# Make the baseline github copy of rawspec
echo 2>&1 | tee -a $LOG
cd rawspec
echo 'Will make rawspec here: '`pwd` 2>&1 | tee -a $LOG
make 2>&1 | tee -a $LOG
if [ $? -ne 0 ]; then
    oops 'make FAILED'
fi

# Run the installer script.
echo 2>&1 | tee -a $LOG
cd $HERE
echo 'Will run installer.py here: '`pwd` 2>&1 | tee -a $LOG
python3 installer.py $PYOPTS 2>&1 | tee -a $LOG

echo 2>&1 | tee -a $LOG
echo ======== 2>&1 | tee -a $LOG
echo FINISHED 2>&1 | tee -a $LOG
echo ======== 2>&1 | tee -a $LOG
echo There is a log of this session in $LOG
