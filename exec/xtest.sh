# Package rawspec_testing
# Execute testing.
# Prerequisite: xprep.sh
#

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

function check_gpu_id {
    case "$1" in
        (*[!0-9]*)
            oops 'The specified GPU ID is not numeric: '$1
    esac
    if [ "$1" -gt 3 ]; then
        MSG='The specified GPU ID must be 0, 1, 2, or 3 but I saw '$1
        echo $MSG  2>&1 | tee -a $LOG
    fi
 }

function check_y_or_n {
    case "$1" in
        y)  echo "--fbh5"
            ;;
        n)  echo ""
            ;;
        (default)
            oops 'check_y_or_n expects y or n but saw this: '$1
    esac
 }

# One command line argument (optional): GPU ID.

NARGS=$#
[ $NARGS -ne 2 ] && oops '2 arguments must be supplied: GPU ID (0, 1, 2, or 3) and either y (.h5 output) or n (.fil output)'
GPU_ID=$1
Q_USE_H5=$2

check_gpu_id $GPU_ID
FBH5_OPT=$(check_y_or_n $Q_USE_H5)

export PATH=$HOME/rawspec:$PATH
export LD_LIBRARY_PATH=$HOME/rawspec

cd $HOME/rawspec_testing/exec
python3 runner.py $FBH5_OPT -g $GPU_ID 2>&1 | tee -a $LOG
if [ $? -eq 0 ]; then
    python3 reviewer.py 2>&1 | tee -a $LOG
fi

echo 2>&1 | tee -a $LOG
echo ======== 2>&1 | tee -a $LOG
echo FINISHED 2>&1 | tee -a $LOG
echo ======== 2>&1 | tee -a $LOG
echo There is a log of this session in $LOG

