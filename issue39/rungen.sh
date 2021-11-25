set -e
set -o pipefail

export PATH=$HOME/rawspec:$PATH
export LD_LIBRARY_PATH=$HOME/rawspec
STEM=/mnt_blpd20/scratch/rawspec_testing/baseline//ATA_guppi_59229_47368_006379_40blocks
PARMS='-f 8192 -t 2 -S -i '1.0'  -d . '

function oops {
    echo
    echo '*** Oops *** '$1' !! ***' 2>&1 | tee -a $LOG
    echo
    exit 86
}

function testsession {
    LOG=gpu$1.log
    echo 2>&1 | tee $LOG
    echo Start GPU $1 2>&1 | tee -a $LOG
    (set -x; rawspec -g $1 $PARMS $STEM 2>&1 | tee -a $LOG)
    if [ $? -ne 0 ]; then
        oops rawspec exit status $?
    fi
    python3 dsel2tbl.py $STEM-ant000.rawspec.0000.fil gpu$1.ant000.tbldsel 2>&1 | tee -a $LOG
    if [ $? -ne 0 ]; then
        oops dsel2tbl.py exit status $?
    fi
    python3 dsel2tbl.py $STEM-ant001.rawspec.0000.fil gpu$1.ant001.tbldsel 2>&1 | tee -a $LOG
    python3 dsel2tbl.py $STEM-ics.rawspec.0000.fil gpu$1.ics.tbldsel 2>&1 | tee -a $LOG
}

rm gpu*.*

testsession 0
testsession 1
testsession 2
testsession 3

