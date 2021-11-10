"""
Package rawspec, testing functions
test/installer.py
Creates/recreates the rawspec testing baseline.

IMPORTANT: Runs only on BL compute node blpc0.

* If an old version of the baseline directory is present, remove it.
* Create baseline directory.
* Copy over selected .raw files
    from one of the source directories
    to the baseline directory.
* For each .raw file in the baseline directory, do the following:
    - rawspec   -f 1048576   -t 51   <.raw file prefix>
* For each .fil file in the baseline directory produced by rawspec, do the following:
    - turboSETI   -n 64   -s 10   -g y   -d <GPU_ID>   <0000.fil file>
    - python3   dat2tbl.py     <.dat file>   <.tbldat file>
    - python3   installer.py   <.h5 file>    <.tblhdr file>
* Cleanup: rm  *.fil  *.h5  *.dat  *.log in the baseline directory.
"""

MY_NAME = "installer"

import sys
import os
import glob
import shutil
import time
from datetime import timedelta
from argparse import ArgumentParser

# Helper functions:
from common import BASELINE_DIR, MY_VERSION, RAWSPECTEST_TBL, \
                   SELECTED, TS_SNR_THRESHOLD, oops, run_cmd, set_up_logger
import dat2tbl
import hdr2tbl
import npols2tbl


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
                        help="GPU device ID (0-3) to use in rawspec and turbo_seti")
    parser.add_argument("-b", "--batch",
                        dest="flag_batch",
                        default=False,
                        action="store_true",
                        help="Flag: Run in batch mode i.e. no interactivity?")
    parser.add_argument("-S", "--skip_init",
                        dest="flag_skip_init",
                        default=False,
                        action="store_true",
                        help="Flag: Skip deadstart init and begin with rawspec?  Might be dangerous.")
    parser.add_argument("-T", "--skip_cleanup",
                        dest="flag_skip_cleanup",
                        default=False,
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

    # Set up logging.
    logger = set_up_logger(MY_NAME)

    # Take a timestamp
    time1 = time.time()

    # Skip initialisation?
    if args.flag_skip_init:
        logger.info("Skipping pre-rawspec initialisation at the operator's request")
    else:
        # Show system information.
        osinfo = os.uname()
        logger.info("O/S name = {}, release = {}, version = {}"
                    .format(osinfo.sysname, osinfo.release, osinfo.version))
        logger.info("Node name = {}, CPU type = {}, HOME = {}"
                    .format(osinfo.nodename, osinfo.machine, os.environ["HOME"]))

        # Interact with the operator if not in batch mode.
        if not args.flag_batch:
            logger.info("installer: This utility script is about to initialise the rawspec test baseline.")
            logger.info("installer: Baseline directory will be {}.".format(BASELINE_DIR))
            logger.info("installer: The first step is to remove old artifacts if they exist.")
            answer = input("\ninstaller: Okay to proceed? (yes/[anything else]: ")
            if answer != "yes":
                logger.warning("installer: Execution canceled by the operator.")
                sys.exit(0)

        # BASELINE_DIR exists?
        if not os.path.exists(BASELINE_DIR): # No, it does not.
            oops("Baseline {} does not exist !!".format(BASELINE_DIR))

        # Remove old artifacts.
        cmd = "rm -rf {}/*".format(BASELINE_DIR)
        run_cmd(cmd, logger)

        # Copy the selected files to BASELINE_DIR.
        counter = 0
        for one_item in SELECTED:
            the_raw_file_list = sorted(glob.glob("{}*.raw".format(one_item)))
            for one_file in the_raw_file_list:
                logger.info("Copying {} .....".format(one_file))
                try:
                    shutil.copy2(one_file, BASELINE_DIR)
                except:
                    oops("shutil.copy2({}, {}) FAILED !!".format(one_file, BASELINE_DIR))
                counter += 1
        logger.info("Copied {} files.".format(counter))

    # Initialisation is complete.
    # Go to BASELINE_DIR..
    try:
        os.chdir(BASELINE_DIR)
        logger.info("Current directory is now {}".format(BASELINE_DIR))
    except:
        oops("os.chdir({}) FAILED !!".format(BASELINE_DIR))

    # For each unique file stem, run rawspec.
    for path_prefix in SELECTED:
        rawstem = os.path.basename(path_prefix)
        cmd = "rawspec  -f 1048576  -t 51  -g {}  {}".format(args.gpu_id, rawstem)
        run_cmd(cmd, logger)

    # For each unique 0000.fil, run turbo_seti, dat2tbl, and hdr2tbl.
    for filfile in sorted(glob.glob("*.fil")):
        peekfile = filfile.split("/")[-1].replace(".fil", ".peeked")
        cmd = "peek  {} 2>&1 > {}" \
              .format(filfile, peekfile)
        run_cmd(cmd, logger)
        cmd = "turboSETI  --snr {}  --gpu y  --gpu_id {}  --n_coarse_chan 64  {}" \
              .format(TS_SNR_THRESHOLD, args.gpu_id, filfile)
        run_cmd(cmd, logger)
        dat_name = filfile.split('/')[-1].replace(".fil", ".dat")
        tbldat_name = filfile.split('/')[-1].replace(".fil", '.tbldat')
        try:
            dat2tbl.main([dat_name, tbldat_name])
        except:
            oops("dat2tbl.main({}, {}) FAILED !!".format(dat_name, tbldat_name))
        h5_name = filfile.split('/')[-1].replace(".fil", ".h5")
        tblhdr_name = filfile.split('/')[-1].replace(".fil", ".tblhdr")
        try:
            hdr2tbl.main([h5_name, tblhdr_name])
        except:
            oops("hdr2tbl.main({}, {}) FAILED !!".format(h5_name, tblhdr_name))
        logger.info("Created post-turbo_seti tables.")

    # Create rawspectest baseline table.
    tblnpols_name = BASELINE_DIR + RAWSPECTEST_TBL
    npols2tbl.main([tblnpols_name])

    # Do post-run cleanup.
    if args.flag_skip_cleanup:
        logger.info("Skipping post-run cleanup at the operator's request")
    else:
        cmd = "rm *.dat *.fil *.h5 *.log"
        run_cmd(cmd, logger)

    # Bye-bye.
    time2 = time.time()
    time_delta = timedelta(seconds=(time2 - time1))
    logger.info("End, elapsed hh:mm:ss = {}".format(time_delta))


if __name__ == "__main__":
    main()
