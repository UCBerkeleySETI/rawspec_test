"""
Package rawspec_testing

Common definitions and functions.
"""

import os
import sys
from time import strftime, localtime

MY_VERSION = "1.2"
TS_SNR_THRESHOLD = 10 # for turbo_seti

FMT_LOGGER_TIMESTAMP = "%H:%M:%S "

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


def run_cmd(cmd, ignore_errors=False):
    """
    Run an operating system command.

    Parameters
    ----------
    cmd : str
        O/S command to run.
    stderr : str, optional
        If an error happens, log that there is a stderr file available.

    Returns
    -------
    None.

    """
    logger("run_cmd", "`{}` .....".format(cmd))
    try:
        here = os.path.dirname(__file__)
        stdout_path = "{}/stdout.txt".format(here)
        stderr_path = "{}/stderr.txt".format(here)
        extcmd = cmd + " 1>{} 2>{}".format(stdout_path, stderr_path)
        exit_status = os.system(extcmd)
        if ignore_errors:
            return
        stderr_size = os.path.getsize(stderr_path)
        if exit_status != 0 or stderr_size > 0:
            logger("run_cmd", "os.system({}) FAILED.\nReturned exit status {}, stderr follows:"
                         .format(cmd, exit_status))
            with open(stderr_path, "r") as fh:
                lines = fh.readlines()
                for line in lines:
                    print(line)
            oops("Cannot continue")
    except Exception as exc:
        oops("os.system({}) EXCEPTION {}"
             .format(cmd, exc))


def logger(my_name, msg):
    """
    Log a time-stamped message.

    Parameters
    ----------
    my_name : str
        The name of the caller.
    msg : str
        The message to log.

    Returns
    -------
    None
    """
    now = strftime(FMT_LOGGER_TIMESTAMP, localtime())
    print("{}  {}  {}".format(now, my_name, msg), flush=True)
