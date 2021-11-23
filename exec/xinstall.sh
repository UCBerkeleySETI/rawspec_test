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

function check_id {
    case "$1" in
        (*[!0-9]*)
            oops 'The specified GPU ID is not numeric: '$1
    esac
    if [ "$1" -gt 3 ]; then
        MSG='The specified GPU ID must be 0, 1, 2, or 3 but I saw '$1
        echo $MSG  2>&1 | tee -a $LOG
    fi
 }

# One command line argument (optional): GPU ID.

NARGS=$#
[ $NARGS -gt 1 ] && oops 'Exactly 1 argument is needed: GPU ID (0, 1, 2, or 3)'

if [ $NARGS == 0 ]; then
    echo 
    MSG='The operator did not supply a GPU ID so we will use GPU_ID=0'
    echo $MSG 2>&1 | tee -a $LOG
    echo
    GPU_ID=0
else
    GPU_ID=$1
fi

check_id $GPU_ID

HERE=`pwd`
URL='https://github.com/UCBerkeleySETI/rawspec'
BRANCH='master'

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
MSG='git clone from baseline URL '$URL', branch '$BRANCH' .....'
echo $MSG 2>&1 | tee -a $LOG
git clone -b $BRANCH $URL
if [ $? -ne 0 ]; then
    oops 'git clone FAILED'
fi

# Make the baseline github copy of rawspec
echo 2>&1 | tee -a $LOG
cd rawspec
echo 'Begin make of rawspec .....' 2>&1 | tee -a $LOG
make 2>&1 | tee -a $LOG
if [ $? -ne 0 ]; then
    oops 'make FAILED'
fi
echo 'End make baseline rawspec.' 2>&1 | tee -a $LOG

# Run the installer script.
echo 2>&1 | tee -a $LOG
cd $HERE
python3 installer.py -g $GPU_ID 2>&1 | tee -a $LOG

echo 2>&1 | tee -a $LOG
echo ======== 2>&1 | tee -a $LOG
echo FINISHED 2>&1 | tee -a $LOG
echo ======== 2>&1 | tee -a $LOG
echo There is a log of this session in $LOG
