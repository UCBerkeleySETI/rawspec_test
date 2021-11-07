# Prepare for testing.
# Prerequisite: xinstall.sh (caution!)

URL='https://github.com/UCBerkeleySETI/rawspec'
BRANCH='master'

HERE=`pwd`
LOG=${HERE}/`basename $0`.log
> $LOG # Make the log nil.
set -e

function oops {
	echo
	echo '*** Oops *** '$1' !! ***'
	echo
	exit 86
}

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
git clone -b $BRANCH $URL 2>&1 | tee -a $LOG
if [ $? -ne 0 ]; then
    oops 'git clone FAILED'
fi
echo 2>&1 | tee -a $LOG
MSG='make rawspec .....'
echo $MSG 2>&1 | tee -a $LOG
cd rawspec
make 2>&1 | tee -a $LOG
if [ $? -ne 0 ]; then
    oops 'make FAILED'
fi

echo 2>&1 | tee -a $LOG
echo ======== 2>&1 | tee -a $LOG
echo FINISHED 2>&1 | tee -a $LOG
echo ======== 2>&1 | tee -a $LOG
echo There is a log of this session in $LOG

