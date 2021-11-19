"""
Package rawspec_testing

Generate a table based on a Filterbank file header, using selected fields.
"""

MY_NAME = "hdr2tbl"

import sys
import os
from argparse import ArgumentParser
from blimpy import Waterfall

# Helpers:
from common import MY_VERSION, logger


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

    parser.add_argument("fbfile", type=str, default="", nargs="?",
                        help="Path of .fil or .h5 file to access")
    parser.add_argument("tblfile", type=str, default="", nargs="?",
                        help="Path of .tblhdr file to open for writing")
    parser.add_argument("-v", "--version", dest="show_version", default=False, 
                        action="store_true",
                        help="show the hdr2tbl version and exit")

    # Validate arguments.
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    if args.show_version:
        print("hdr2tbl: {}".format(MY_VERSION))
        sys.exit(0)

    if args.fbfile == "" or args.tblfile == "":
        os.system("python3 {} -h".format(__file__))
        sys.exit(86)

    if not os.path.exists(args.fbfile):
        print("\nInput file {} does not exist!\n".format(args.fbfile))
        sys.exit(86)

    # Open .h5 file for reading.
    wf = Waterfall(args.fbfile)

    # Extract comparator fields.
    wf.header["n_ints_in_file"] = wf.n_ints_in_file

    # Write header dict object to the output CSV file.
    with open(args.tblfile, "w") as csvfile:
        csvfile.write("{},{}\n".format("key", "value"))
        for key in wf.header.keys():
            csvfile.write("{},{}\n".format(key, wf.header[key]))

    logger(MY_NAME, "Saved {}".format(os.path.basename(args.tblfile)))


if __name__ == "__main__":
    main()
