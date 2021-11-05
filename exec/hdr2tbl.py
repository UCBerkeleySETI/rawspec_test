r"""
Package rawspec, testing functions
test/hdr2tbl.py

Generate a table based on a turbo_seti .h5 file header, using selected fields.
"""

MY_NAME = "hdr2tbl"

import sys
import os
from argparse import ArgumentParser
import h5py
from astropy.coordinates import Angle

# Helpers:
from common import MY_VERSION, set_up_logger


def read_header(h5):
    """
    Read the .h5 header.  Populate a Python dictionary of key:value pairs.

    Parameters
    ----------
    h5 : HDF5 handle
        This is the open HDF5 file.

    Returns
    -------
    header : dict
        This is the header as a Python dict object.

    """

    header = {}

    for key, val in h5['data'].attrs.items():
        if isinstance(val, bytes):
            val = val.decode('ascii')
        if key == 'src_raj':
            header[key] = Angle(val, unit='hr')
        elif key == 'src_dej':
            header[key] = Angle(val, unit='deg')
        else:
            header[key] = val

    return header


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
    parser = ArgumentParser(description="hdr2tbl version {}."
                                        .format(MY_VERSION))

    parser.add_argument("h5file", type=str, default="", nargs="?",
                        help="Path of .h5 file to open for reading")
    parser.add_argument("tblfile", type=str, default="", nargs="?",
                        help="Path of .tblhdr file to open for writing")
    parser.add_argument("-v", "--version", dest="show_version", default=False, action="store_true",
                        help="show the hdr2tbl version and exit")

    # Validate arguments.
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    if args.show_version:
        print("hdr2tbl: {}".format(MY_VERSION))
        sys.exit(0)

    if args.h5file == "" or args.tblfile == "":
        os.system("python3 {} -h".format(__file__))
        sys.exit(86)

    if not os.path.exists(args.h5file):
        print("\nInput file {} does not exist!\n".format(args.h5file))
        sys.exit(86)

    # Set up logging.
    logger = set_up_logger(MY_NAME)

    # Open .h5 file for reading.
    h5 = h5py.File(args.h5file, mode="r")

    # Extract comparator fields.
    header = read_header(h5)
    header["n_ints_in_file"] = h5["data"].shape[0]

    # Write header dict object to the output CSV file.
    with open(args.tblfile, "w") as csvfile:
        csvfile.write("{},{}\n".format("key", "value"))
        for key in header.keys():
            csvfile.write("{},{}\n".format(key, header[key]))

    logger.info("Saved {}".format(args.tblfile))


if __name__ == "__main__":
    main()
