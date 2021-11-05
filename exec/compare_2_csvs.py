"""
Package rawspec, testing functions
test/compare_2_csvs.py

Compare 2 dataframes (baseline and trial), row by row, column by column.
"""

MY_NAME = "compare_2_csvs"

import numpy as np
import pandas as pd
from common import RTOL_VALUE, set_up_logger

n_complaints = 0
DEBUGGING = False
logger = None


def compare_lists(col_name, df_b, df_t, flag_isclose=False, rtol_value=0):
    global n_complaints, logger

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
                logger.info("Row {} for {} ok".format(ii, col_name))
            else:
                n_complaints += 1
                logger.error("Row {} baseline {}={} but trial value={}, using rtol={}"
                             .format(ii, col_name, b_list[ii], t_item, rtol_value))
        else: # Not real-number scalars; straight comparison works.
            if t_item == b_list[ii]:
                logger.info("Row {} for {} ok".format(ii, col_name))
            else:
                n_complaints += 1
                logger.error("Row {} baseline {}={} but trial value={}"
                             .format(ii, col_name, b_list[ii], t_item))


def compare_tbldat(baseline, trial):

    global logger
    logger = set_up_logger("compare_tbldat")

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
    compare_lists("top_hit_id", df_b, df_t)
    compare_lists("drift_rate", df_b, df_t, True, RTOL_VALUE)
    compare_lists("snr", df_b, df_t, True, RTOL_VALUE)
    compare_lists("frequency", df_b, df_t, True, RTOL_VALUE)
    compare_lists("total_num_hits", df_b, df_t)

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
    df : Pandas DataFrame object
        Transposed and fixed table.

    """
    df = pd.read_csv(csvpath).T # Load CSV file data and matrix-transpose it.
    new_header = df.iloc[0]     # Grab the first row for the new header.
    df = df[1:]                 # Take the data less the header row.
    df.columns = new_header     # Set the df header = the new header.
    return df


def compare_tblhdr(baseline, trial):

    global logger
    logger = set_up_logger("compare_tblhdr")

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
    compare_lists("fch1", df_b, df_t, True, RTOL_VALUE)
    compare_lists("foff", df_b, df_t, True, RTOL_VALUE)
    compare_lists("nbits", df_b, df_t)
    compare_lists("nchans", df_b, df_t)
    compare_lists("nifs", df_b, df_t)
    compare_lists("rawdatafile", df_b, df_t)
    compare_lists("source_name", df_b, df_t)
    compare_lists("tsamp", df_b, df_t, True, RTOL_VALUE)
    compare_lists("n_ints_in_file", df_b, df_t)

    # Return resul to caller.
    return n_complaints
