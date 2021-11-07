"""
Package rawspec, testing functions
test/reviewer.py

IMPORTANT: Runs only on BL compute node blpc0.

* cd <trial diretcory>
* For each .tbldat file in the <trial directory>, do the following:
    - Compare   <.tbldat file> to counterpart in the baseline
    - Compare   <.tblhdr file> to counterpart in the baseline
* In all cases, report SUCCESS or FAILURE.
"""

MY_NAME = "reviewer"

import sys
import os
import glob
from argparse import ArgumentParser

# Helper functions:
from common import BASELINE_DIR, MY_VERSION, RAWSPECTEST_TBL, TRIAL_DIR, \
                   oops, set_up_logger
from compare_2_csvs import compare_tbldat, compare_tblhdr, compare_tblnpols


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
    # Initialise error count to zero.
    logger = set_up_logger(MY_NAME)
    n_errors = 0

    # On the right system?
    osinfo = os.uname()
    logger.info("O/S name = {}, release = {}, version = {}"
                .format(osinfo.sysname, osinfo.release, osinfo.version))
    logger.info("Node name = {}, CPU type = {}, HOME = {}"
                .format(osinfo.nodename, osinfo.machine, os.environ["HOME"]))

    # BASELINE_DIR exist?
    if not os.path.exists(BASELINE_DIR):
        oops("Trial directory ({}) does NOT exist !!".format(BASELINE_DIR))

    # TRIAL_DIR exist?
    if not os.path.exists(TRIAL_DIR):
        oops("Trial directory ({}) does NOT exist !!".format(TRIAL_DIR))

    # For each unique .tbldat file in BASELINE_DIR,
    # compare it to its counterpart in TRIAL_DIR.
    for baseline_file in sorted(glob.glob("{}/*.tbldat".format(BASELINE_DIR))):
        basename = os.path.basename(baseline_file)
        logger.info(basename)
        trial_file = os.path.join(TRIAL_DIR, basename)
        n_errors += compare_tbldat(baseline_file, trial_file)

    # For each unique .tblhdr file in BASELINE_DIR,
    # compare it to its counterpart in TRIAL_DIR.
    for baseline_file in sorted(glob.glob("{}/*.tblhdr".format(BASELINE_DIR))):
        basename = os.path.basename(baseline_file)
        logger.info(basename)
        trial_file = os.path.join(TRIAL_DIR, basename)
        n_errors += compare_tblhdr(baseline_file, trial_file)

    # Compare trial to baseline versions o0f rawspectest .tblnpols files.
    baseline = BASELINE_DIR + RAWSPECTEST_TBL
    trial = TRIAL_DIR + RAWSPECTEST_TBL
    n_errors += compare_tblnpols(baseline, trial)

    # Bye-bye.
    if n_errors > 0:
        logger.fatal("*FAILURE* - Number of errors reported = {}".format(n_errors))
    logger.info("*SUCCESS* - No errors reported.")


if __name__ == "__main__":
    main()
