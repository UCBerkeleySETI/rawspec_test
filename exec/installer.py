"""
Package rawspec_testing

Creates/recreates the rawspec testing baseline.

* If an old version of the baseline artifacts are present, remove them.
* Copy over selected .raw files
    from one of the source directories
    to the baseline directory.
* For each .raw file in the baseline directory, do the following:
    - rawspec   <rawspec options>   <.raw file prefix>
* For each .fil file in the baseline directory produced by rawspec, do the following:
    - Optionally: turboSETI   -s 10   -g y   -d <GPU_ID>   <0000.fil/.h5 file>
    - Create a .tbldat file.
    - Create a .tblhdr file.
    - Create a .tbldsel file.
* Cleanup: rm  *.fil  *.h5  *.dat  *.log in the baseline directory.
"""

MY_NAME = "installer"

import sys
import os
import glob
import time
from datetime import timedelta
from argparse import ArgumentParser

# Helper functions:
from site_parameters import BASELINE_DIR, RAWSPEC_OPTS, RAWSPECTEST_TBL, \
                            RUN_TURBO_SETI, SELECTED, TESTING_NODE
from common import MY_VERSION, TS_SNR_THRESHOLD, oops, run_cmd, logger
import dat2tbl
import hdr2tbl
import npols2tbl
import dsel2tbl


def main(args=None):
    """
    Parameters
    ----------
    args : Namespace
        Command-line parameters. The default is None.

    Returns
    -------
    None.

    """

    # Create an option parser to get command-line input/arguments
    parser = ArgumentParser(description="installer version {}."
                                        .format(MY_VERSION))
    parser.add_argument("-g", "--gpu_id",
                        dest="gpu_id",
                        type=int,
                        required=True,
                        help="GPU device ID (0-3) to use in rawspec")
    parser.add_argument("-S", "--skip_cleanup",
                        dest="flag_skip_cleanup",
                        default=True,
                        action="store_true",
                        help="Flag: Skip cleanup at end?  Large files are left in baseline.")
    parser.add_argument("-v", "--version",
                        dest="show_version",
                        default=False,
                        action="store_true",
                        help="Flag: Show the installer version and exit")

    # Validate arguments.
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    if args.show_version:
        print("installer: {}".format(MY_VERSION))
        sys.exit(0)

    # Take a timestamp
    time1 = time.time()

    # Show system information.
    osinfo = os.uname()
    logger(MY_NAME, "O/S name = {}, release = {}, version = {}"
                .format(osinfo.sysname, osinfo.release, osinfo.version))
    logger(MY_NAME, "Node name = {}, CPU type = {}, HOME = {}"
                .format(osinfo.nodename, osinfo.machine, os.environ["HOME"]))
    if TESTING_NODE != "any":
        if osinfo.nodename != TESTING_NODE:
            oops("Node name must be {}".format(TESTING_NODE))

    # Initialisation is complete.
    # Go to BASELINE_DIR..
    try:
        os.chdir(BASELINE_DIR)
        logger(MY_NAME, "Current directory is now {}".format(BASELINE_DIR))
        cmd = "rm *.fil *.tbldsel *.tblhdr *.tblnpols"
        run_cmd(cmd, ignore_errors=True)
    except:
        oops("os.chdir({}) FAILED".format(BASELINE_DIR))

    # For each unique file stem, run rawspec.
    # Note: If a rawspec file is X.0000.raw then its rawstem is X.
    for ii, rawstem in enumerate(SELECTED):
        rawspec_opts = RAWSPEC_OPTS[ii]
        cmd = "rawspec  {}  -g {}  {}".format(rawspec_opts, args.gpu_id, rawstem)
        run_cmd(cmd)

    # For each unique .fil file, run turbo_seti (optionally), dat2tbl, and hdr2tbl.
    for filfile in sorted(glob.glob("*.fil")):
        if RUN_TURBO_SETI:
            cmd = "turboSETI  --snr {}  --gpu y  --gpu_id {}  --n_coarse_chan 64  {}" \
                  .format(TS_SNR_THRESHOLD, args.gpu_id, filfile)
            run_cmd(cmd)
            dat_name = filfile.split('/')[-1].replace(".fil", ".dat")
            tbldat_name = filfile.split('/')[-1].replace(".fil", '.tbldat')
            try:
                dat2tbl.main([dat_name, tbldat_name])
            except:
                oops("dat2tbl.main({}, {}) FAILED".format(dat_name, tbldat_name))
        tblhdr_name = filfile.split('/')[-1].replace(".fil", ".tblhdr")
        try:
            hdr2tbl.main([filfile, tblhdr_name])
        except:
            oops("hdr2tbl.main({}, {}) FAILED".format(filfile, tblhdr_name))
        tbldsel_name = filfile.split('/')[-1].replace(".fil", ".tbldsel")
        try:
            dsel2tbl.main([filfile, tbldsel_name])
        except:
            oops("dsel2tbl.main({}, {}) FAILED".format(filfile, tbldsel_name))

        logger(MY_NAME, "Created post-turbo_seti tables for {}.".format(filfile))

    # Create rawspectest baseline table.
    tblnpols_name = BASELINE_DIR + RAWSPECTEST_TBL
    npols2tbl.main([tblnpols_name])

    # Do post-run cleanup.
    if args.flag_skip_cleanup:
        logger(MY_NAME, "Skipping post-run cleanup.")
    else:
        cmd = "rm *.dat *.fil *.h5 *.log"
        run_cmd(cmd, ignore_errors=True)

    # Bye-bye.
    time2 = time.time()
    time_delta = timedelta(seconds=(time2 - time1))
    logger(MY_NAME, "End, elapsed hh:mm:ss = {}".format(time_delta))


if __name__ == "__main__":
    main()
