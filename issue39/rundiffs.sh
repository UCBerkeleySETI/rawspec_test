GPUA=0

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

# One command line argument: GPU ID.

NARGS=$#
[ $NARGS -ne 1 ] && oops '1 argument must be supplied: GPU ID (0, 1, 2, or 3)'
GPUB=$1
check_gpu_id $GPUB

set -x
diff gpu$GPUA.ics.tbldsel gpu$GPUB.ics.tbldsel
diff gpu$GPUA.ant001.tbldsel gpu$GPUB.ant001.tbldsel
diff gpu$GPUA.ant000.tbldsel gpu$GPUB.ant000.tbldsel
