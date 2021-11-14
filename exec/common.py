"""
Package rawspec_testing

Common definitions and functions.
"""

import os
import sys
import logging

MY_VERSION = "1.1"
TS_SNR_THRESHOLD = 10

SOURCE_DIR_1 = "/mnt_blpd5/datax/FRB121102/BLP13/"
SOURCE_DIR_2 = "/mnt_blpd5/datax/FRB121102/BLP17/"

SELECTED = [
    SOURCE_DIR_1 + "blc13_guppi_57991_49836_DIAG_FRB121102_0010",
    SOURCE_DIR_2 + "blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008",
    ]

RAWSPEC_TEST_DIR = "/mnt_blpd20/scratch/rawspec_testing/"
BASELINE_DIR = RAWSPEC_TEST_DIR + "baseline/"
TRIAL_DIR = RAWSPEC_TEST_DIR + "trial/"
ATA_DIR = RAWSPEC_TEST_DIR + "ata/"
RAWSPECTEST_TBL = "rawspectest.tblnpols"

LOGGER_FORMAT = "%(asctime)-8s  %(name)s  %(levelname)s  %(message)s"
TIME_FORMAT = "%H:%M:%S"

PANDAS_SEPARATOR = "\s+"
PANDAS_ENGINE = "python"

RUN_TURBO_SETI = False

# Tolerance of the Relative TO Largest (RTOL).
# This is the maximum allowed difference between two real numbers
# relative to the larger absolute value.
# For example, to set a tolerance of 5%, then rel_tol=0.05
RTOL_VALUE = 0.0005 # 0.05 %


def oops(msg):
    """
    Parameters
    ----------
    msg : str
        Text depicting reason for aborting.

    Returns
    -------
    None.

    """
    print("\n*** OOPS, {} ***\n".format(msg))
    sys.exit(86)


def run_cmd(cmd, logger, ignore_errors=False):
    """
    Run an operating system command.

    Parameters
    ----------
    cmd : str
        O/S command to run.
    logger : logging object
        Announce the running command.
    stderr : str, optional
        If an error happens, log that there is a stderr file available.

    Returns
    -------
    None.

    """
    logger.info("Running `{}` .....".format(cmd))
    try:
        here = os.path.dirname(__file__)
        stdout = "{}/stdout.txt".format(here)
        stderr = "{}/stderr.txt".format(here)
        extcmd = cmd + " 1>{} 2>{}".format(stdout, stderr)
        exit_status = os.system(extcmd)
        if ignore_errors:
            return
        if exit_status != 0:
            logger.error("os.system({}) FAILED.\nReturned exit status {}, stderr follows:".format(cmd, exit_status))
            with open(stderr, "r") as fh:
                lines = fh.readlines()
                for line in lines:
                    print(line)
            oops("Cannot continue")
    except Exception as exc:
        oops("os.system({}) EXCEPTION {}"
             .format(cmd, exc))
 

def set_up_logger(my_name):
    """
    Set up the logger.

    Parameters
    ----------
    my_name : str
        The name of the caller.

    Returns
    -------
    logger : logging object
    """
    logging_format = LOGGER_FORMAT
    logging.basicConfig(format=logging_format,
                        datefmt=TIME_FORMAT,
                        level=logging.INFO)
    logger = logging.getLogger(name=my_name)
    logger.debug("Logging set up complete.")

    return logger
