"""
Package rawspec_testing

Compare 2 dataframes (baseline and trial), row by row, column by column.
"""

MY_NAME = "compare_2_csvs"

import numpy as np
import pandas as pd
from common import RTOL_VALUE, set_up_logger

# globals
DEBUGGING = False
logger = None


def compare_lists(col_name, df_b, df_t, flag_isclose=False, rtol_value=0):
    """
    Compare 2 lists made from 2 dataframes.

    Parameters
    ----------
    col_name : str
        Name of the dataframe column to use.
    df_b : Pandas Dataframe
        Baseline.
    df_t : Pandas Dataframe
       Trial.
    flag_isclose : boolean, optional
        Use numpy.isclose()? The default is False.
    rtol_value : float, optional
       See numpy.isclose(). The default is 0.

    Returns
    -------
    int
        Number of error complaints generated.
    """
    global logger
    n_complaints = 0

    b_list = df_b[col_name].tolist()
    t_list = df_t[col_name].tolist()
    if DEBUGGING:
        print("DEBUG b_list:", b_list)
        print("DEBUG df_b:\n", df_b)
    for ii, t_item in enumerate(t_list):
        if flag_isclose: # Real-number scalars.
            # NOTE that numpy.isclose() assumes that the 2nd parameter is the reference value.
            # Ref:  https://numpy.org/doc/stable/reference/generated/numpy.isclose.html?highlight=isclose#numpy.isclose
            if np.isclose(float(t_item), float(b_list[ii]), rtol=rtol_value):
                logger.debug("Row {} for {} ok".format(ii, col_name))
            else:
                n_complaints += 1
                logger.error("Row {} baseline {}={} but trial value={}, using rtol={}"
                             .format(ii, col_name, b_list[ii], t_item, rtol_value))
        else: # Not real-number scalars; straight comparison works.
            if t_item == b_list[ii]:
                logger.debug("Row {} for {} ok".format(ii, col_name))
            else:
                n_complaints += 1
                logger.error("Row {} baseline {}={} but trial value={}"
                             .format(ii, col_name, b_list[ii], t_item))

    return n_complaints


def compare_tbldat(baseline, trial):
    """
    Compare 2 .tbldat files.

    Parameters
    ----------
    baseline : Pandas Dataframe
        Baseline.
    trial : Pandas Dataframe
        Trial.

    Returns
    -------
    int
        Number of error complaints generated.
    """

    global logger
    logger = set_up_logger("compare_tbldat")
    n_complaints = 0

    # Load both Dataframes.
    df_b = pd.read_csv(baseline)
    df_t = pd.read_csv(trial)

    # Make sure they have the same number of rows.
    nrows_b = len(df_b)
    nrows_t = len(df_t)
    if DEBUGGING:
        print("DEBUG nrows_b={}, nrows_t={}".format(nrows_b, nrows_t))
    if nrows_t != nrows_b:
        logger.error("Baseline has {} rows but trial has {} rows"
                     .format(nrows_b, nrows_t))
        return 1

    # Check all the columns.
    n_complaints += compare_lists("top_hit_id", df_b, df_t)
    n_complaints += compare_lists("drift_rate", df_b, df_t, True, RTOL_VALUE)
    n_complaints += compare_lists("snr", df_b, df_t, True, RTOL_VALUE)
    n_complaints += compare_lists("frequency", df_b, df_t, True, RTOL_VALUE)
    n_complaints += compare_lists("total_num_hits", df_b, df_t)

    # Return resul to caller.
    return n_complaints


def compare_tblnpols(baseline, trial):
    """
    Compare 2 .tblnpols files.

    Parameters
    ----------
    baseline : Pandas Dataframe
        Baseline.
    trial : Pandas Dataframe
        Trial.

    Returns
    -------
    int
        Number of error complaints generated.
    """

    global logger
    logger = set_up_logger("compare_tblnpols")
    n_complaints = 0

    # Load both Dataframes.
    df_b = pd.read_csv(baseline)
    df_t = pd.read_csv(trial)

    # Make sure they have the same number of rows.
    nrows_b = len(df_b)
    nrows_t = len(df_t)
    if DEBUGGING:
        print("DEBUG nrows_b={}, nrows_t={}".format(nrows_b, nrows_t))
    if nrows_t != nrows_b:
        logger.error("Baseline has {} rows but trial has {} rows"
                     .format(nrows_b, nrows_t))
        return 1

    # Check all the columns.
    n_complaints += compare_lists("nbits", df_b, df_t)
    n_complaints += compare_lists("product", df_b, df_t)
    n_complaints += compare_lists("chan", df_b, df_t)
    n_complaints += compare_lists("npols", df_b, df_t)
    n_complaints += compare_lists("value1", df_b, df_t, True, RTOL_VALUE)
    n_complaints += compare_lists("value2", df_b, df_t, True, RTOL_VALUE)
    n_complaints += compare_lists("value3", df_b, df_t, True, RTOL_VALUE)
    n_complaints += compare_lists("value4", df_b, df_t, True, RTOL_VALUE)

    # Return resul to caller.
    return n_complaints


def hdfcsv2df(csvpath):
    """
    For a .tblhdr file,
    load, transpose, and fix data from a CSV file into a Pandas DataFrame.

    Parameters
    ----------
    csvpath : str
       Path to CSV file.

    Returns
    -------
    Pandas DataFrame object
        Transposed and fixed table.
    """
    df = pd.read_csv(csvpath).T # Load CSV file data and matrix-transpose it.
    new_header = df.iloc[0]     # Grab the first row for the new header.
    df = df[1:]                 # Take the data less the header row.
    df.columns = new_header     # Set the df header = the new header.
    return df


def compare_tblhdr(baseline, trial):
    """
    Compare 2 .tblhdr files.

    Parameters
    ----------
    baseline : Pandas Dataframe
        Baseline.
    trial : Pandas Dataframe
        Trial.

    Returns
    -------
    int
        Number of error complaints generated.
    """

    global logger
    logger = set_up_logger("compare_tblhdr")
    n_complaints = 0

    # Load both Dataframes.
    df_b = hdfcsv2df(baseline)
    df_t = hdfcsv2df(trial)

    # Make sure they have the same number of rows.
    nrows_b = len(df_b)
    nrows_t = len(df_t)
    if DEBUGGING:
        print("DEBUG nrows_b={}, nrows_t={}".format(nrows_b, nrows_t))
    if nrows_t != nrows_b:
        logger.error("Baseline has {} rows but trial has {} rows"
                     .format(nrows_b, nrows_t))
        return 1

    # Check all the columns.
    n_complaints += compare_lists("fch1", df_b, df_t, True, RTOL_VALUE)
    n_complaints += compare_lists("foff", df_b, df_t, True, RTOL_VALUE)
    n_complaints += compare_lists("nbits", df_b, df_t)
    n_complaints += compare_lists("nchans", df_b, df_t)
    n_complaints += compare_lists("nifs", df_b, df_t)
    n_complaints += compare_lists("rawdatafile", df_b, df_t)
    n_complaints += compare_lists("source_name", df_b, df_t)
    n_complaints += compare_lists("tsamp", df_b, df_t, True, RTOL_VALUE)
    n_complaints += compare_lists("n_ints_in_file", df_b, df_t)

    # Return resul to caller.
    return n_complaints
