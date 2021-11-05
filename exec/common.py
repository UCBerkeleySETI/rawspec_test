"""
Package rawspec, testing functions
test/common.py

Common definitions and functions.
"""

import sys
import logging

MY_VERSION = "1.0"
CORRECT_NODE = "blpc0"
TS_SNR_THRESHOLD = 10

SOURCE_DIR_1 = "/mnt_blpd5/datax/FRB121102/BLP13/"
SOURCE_DIR_2 = "/mnt_blpd5/datax/FRB121102/BLP17/"

SELECTED = [
    SOURCE_DIR_1 + "blc13_guppi_57991_49836_DIAG_FRB121102_0010",
    SOURCE_DIR_2 + "blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008",
    ]

BASELINE_DIR = "/datax/scratch/rawspec_test_baseline/"
TRIAL_DIR = "/datax/scratch/rawspec_test_trial/"

LOGGER_FORMAT = "%(asctime)-8s  %(name)s  %(levelname)s  %(message)s"
TIME_FORMAT = "%H:%M:%S"

PANDAS_SEPARATOR = "\s+"
PANDAS_ENGINE = "python"

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
    logger = logging.getLogger(name=my_name)
    logging_format = LOGGER_FORMAT
    logging.basicConfig(format=logging_format,
                        datefmt=TIME_FORMAT)
    logger.setLevel(logging.INFO)
    logger.info("Logging set up complete.")
    
    return logger
