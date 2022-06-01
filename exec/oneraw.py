"""
Package rawspec_testing

oneraw.py: Creates/recreates one fil file and its related tables in the rawspec testing baseline.

* For the specified .raw file stem in the baseline directory, do the following:
    - rawspec   <rawspec options>   <.raw file prefix>
* With the .fil file in the baseline directory produced by rawspec, do the following:
    - Create a .tblhdr file.
    - Create a .tbldsel file.
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
                            SELECTED, TESTING_NODE
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
    parser = ArgumentParser(description="install one raw file, version {}."
                                        .format(MY_VERSION))
    parser.add_argument("instem",
                        type=str,
                        help="Path of input .raw file stem to use as input to rawspec")
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
    except:
        oops("os.chdir({}) FAILED".format(BASELINE_DIR))

    # For each unique file stem, run rawspec.
    # Note: If a rawspec file is X.0000.raw then its rawstem is X.
    for ii, rawstem in enumerate(SELECTED):
        if rawstem == args.instem:
            rawspec_opts = RAWSPEC_OPTS[ii]
            cmd = "rawspec  {}  -g {}  {}".format(rawspec_opts, args.gpu_id, rawstem)
            run_cmd(cmd)
            break

    # For the .fil file that matches the input stem, run dat2tbl and hdr2tbl.
    for filfile in sorted(glob.glob(f"{args.instem}*.fil")):
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

        logger(MY_NAME, "Created tables for {}.".format(filfile))

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
