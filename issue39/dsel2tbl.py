"""
Package rawspec_testing

Generate a table based on the data shape and selected data matrix elements.
"""

MY_NAME = "dsel2tbl"

import sys
import os
from argparse import ArgumentParser

# Helpers:
from common import MY_VERSION, logger
from blimpy import Waterfall


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
                        help="Path of .fil or .h5 file to open for reading")
    parser.add_argument("tblfile", type=str, default="", nargs="?",
                        help="Path of .tbldsel file to open for writing")
    parser.add_argument("-v", "--version", dest="show_version", default=False, 
                        action="store_true",
                        help="show the dsel2tbl version and exit")

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

    # Get Waterfall object.
    wf = Waterfall(args.fbfile)
    logger(MY_NAME, "Data shape for {} = ({}, {}, {})"
                .format(args.fbfile, wf.n_ints_in_file, wf.header["nifs"], wf.n_channels_in_file))
    assert wf.n_ints_in_file > 1
    assert wf.n_channels_in_file > 3

    # Define data postage stamps.
    nw = wf.data[0, 0, 0:3]
    ne = wf.data[0, 0, -4:-1]
    sw = wf.data[wf.n_ints_in_file - 1, 0, 0:3]
    se = wf.data[wf.n_ints_in_file - 1, 0, -4:-1]
    centre_row = wf.n_ints_in_file // 2
    centre_col = wf.n_channels_in_file // 2
    bullseye = wf.data[centre_row, 0, centre_col - 1 : centre_col + 2]

    # Create the output CSV file.
    with open(args.tblfile, "w") as csvfile:
        csvfile.write("{},{},{},{}\n"
                      .format("label", "value1", "value2", "value3"))
        csvfile.write("NW,{},{},{}\n"
                      .format(nw[0], nw[1], nw[2]))
        csvfile.write("NE,{},{},{}\n"
                      .format(ne[0], ne[1], ne[2]))
        csvfile.write("SW,{},{},{}\n"
                      .format(sw[0], sw[1], sw[2]))
        csvfile.write("SE,{},{},{}\n"
                      .format(se[0], se[1], se[2]))
        csvfile.write("Bullseye,{},{},{}\n"
                      .format(bullseye[0], bullseye[1], bullseye[2]))

    logger(MY_NAME, "Saved {}".format(os.path.basename(args.tblfile)))


if __name__ == "__main__":
    main()
