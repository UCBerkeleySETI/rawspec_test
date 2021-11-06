# Execute testing.
# Prerequisite: xprep.sh
#

function oops {
	echo
	echo '*** Oops *** '$1' !! ***'
	echo
	exit 86
}

function check_id {
    case "$1" in
        (*[!0-9]*)
            oops 'The specified GPU ID is not numeric: '$1
    esac
    if [ "$1" -gt 3 ]; then
        oops 'The specified GPU ID must be 0, 1, 2, or 3 but I saw '$1
    fi
 }

set -e

# One command line argument (optional): GPU ID.

NARGS=$#
[ $NARGS -gt 1 ] && oops 'Exactly 1 argument is needed: GPU ID (0, 1, 2, or 3)'

if [ $NARGS == 0 ]; then
    echo 
    echo The operator did not supply a GPU ID so we will use GPU_ID=0
    echo
    GPU_ID=0
else
    GPU_ID=$1
fi

check_id $GPU_ID

export PATH=$HOME/rawspec:$PATH
export LD_LIBRARY_PATH=$HOME/rawspec

cd $HOME/rawspec_testing/exec
python3 runner.py -g $GPU_ID
if [ $? -eq 0 ]; then
    python3 reviewer.py
fi

