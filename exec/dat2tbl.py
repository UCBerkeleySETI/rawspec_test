r"""
Package rawspec_testing

Generate a table based on a turbo_seti .dat file, using selected columns.
"""

MY_NAME = "dat2tbl"

import sys
import os
from argparse import ArgumentParser
import pandas as pd

# Helpers:
from common import MY_VERSION, PANDAS_ENGINE, PANDAS_SEPARATOR, logger


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
    parser = ArgumentParser(description="{} version {}."
                                        .format(MY_NAME, MY_VERSION))

    parser.add_argument("datfile", type=str, default="", nargs="?",
                        help="Path of .dat file to open for reading")
    parser.add_argument("tblfile", type=str, default="", nargs="?",
                        help="Path of .tbldat file to open for writing")
    parser.add_argument("-v", "--version", dest="show_version", default=False, 
                        action="store_true",
                        help="show the dat2tbl version and exit")

    # Validate arguments.
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    if args.show_version:
        print("dat2tbl: {}".format(MY_VERSION))
        sys.exit(0)

    if args.datfile == "" or args.tblfile == "":
        os.system("python3 {} -h".format(__file__))
        sys.exit(86)

    if not os.path.exists(args.datfile):
        print("\nInput file {} does not exist!\n".format(args.datfile))
        sys.exit(86)

    # Read .dat file into a Pandas DataFrame.
    # There is no CSV header; comment lines have a '#' in column 1.
    df = pd.read_csv(args.datfile,
                     header=None,
                     sep=PANDAS_SEPARATOR,
                     engine=PANDAS_ENGINE,
                     usecols=(0, 1, 2, 3, 11),
                     comment="#")

    # Set headings into the DataFrame.
    df.columns = ("top_hit_id", "drift_rate", "snr", "frequency", "total_num_hits")

    # Save DataFrame to the output CSV file.
    df.to_csv(args.tblfile, header=True, index=False)
    logger(MY_NAME, "Saved {}".format(os.path.basename(args.tblfile)))


if __name__ == "__main__":
    main()
