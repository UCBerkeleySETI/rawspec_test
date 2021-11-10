"""
Package rawspec, testing functions
npols2tbl.py

Generate a table based on rawspectest output.
"""
import os
import sys
from argparse import ArgumentParser
from common import MY_VERSION, oops, run_cmd, set_up_logger

RAWSPECTEST_DIR = os.environ["HOME"] + "/rawspec_testing/exec/"
RST_STDOUT = RAWSPECTEST_DIR + "stdout.txt"
RST_STDERR = RAWSPECTEST_DIR + "stderr.txt"


def do_nbits(wfh, nbits):
    """
    Create entries for one case, appending the output file.

    Parameters
    ----------
    wfh : O/S file handle object
        Write to the output file.
    nbits : int
        Set to the spectra element size in bits.

    Returns
    -------
    None.

    """
    logger = set_up_logger("npols2tbl.{}".format(nbits))
    cmd = "rawspectest {} 2> ".format(nbits) \
            + RST_STDERR \
            + " 1> " + RST_STDOUT
    run_cmd(cmd, logger, RST_STDERR)

    logger.info("Checking stderr (should be nil) ...")
    file_size = os.path.getsize(RST_STDERR)
    if file_size > 0:
        with open(RST_STDERR, "r") as rfh:
            content = rfh.read()
            print(content)
        oops("rawspectest FAILED")

    logger.info("Checking stdout (should not be nil) ...")
    file_size = os.path.getsize(RST_STDOUT)
    if file_size < 1:
        oops("rawspectest stdout was EMPTY")

    with open(RST_STDOUT, "r") as rfh: # Start reading rawspectest stdout file.
        lines = rfh.readlines() # Get all of the lines in the file.
        line_counter = 0

        for line in lines: # For every individual line in the file .....
            line = line.rstrip("\n")
            line_counter += 1
            tokens = line.split(" ") # Get all of the tokens in the current line.
            if tokens[0] != "output" or tokens[1] != "product" or tokens[3] != "chan":
                continue # skip uninteresting lines
            token_counter = len(tokens)
            if token_counter < 6:
                oops("Line {} <{}> should have at least 6 tokens but I saw {}"
                     .format(line_counter, line, token_counter))
            product = tokens[2]
            chan = tokens[4]
            if token_counter == 6: # Single polarisation?
                npols = 1
                pol_values = [tokens[5], 0.0, 0.0, 0.0]
            else: # 4 polarisations.
                if token_counter != 9:
                    oops("Line {} <{}> should have 6 or 9 tokens but I saw {}"
                         .format(line_counter, line, token_counter))
                npols = 4
                pol_values = [tokens[5], tokens[6], tokens[7], tokens[8]]
            wfh.write("{},{},{},{},{},{},{},{}\n"
                     .format(nbits, product, chan, npols,
                             pol_values[0], pol_values[1], pol_values[2], pol_values[3]))


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
    parser = ArgumentParser(description="gen_npols version {}."
                                        .format(MY_VERSION))

    parser.add_argument("tblfile", type=str, default="", nargs="?",
                        help="Path of .tblnpols file to open for writing")
    parser.add_argument("-v", "--version", dest="show_version", default=False, action="store_true",
                        help="show the gen_npols version and exit")

    # Validate arguments.
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    if args.show_version:
        print("hdr2tbl: {}".format(MY_VERSION))
        sys.exit(0)

    if args.tblfile == "":
        os.system("python3 {} -h".format(__file__))
        sys.exit(86)

    # Generate cases for 8- and 16-bit spectra elements.
    with open(args.tblfile, "w") as wfh:
        wfh.write("nbits,product,chan,npols,value1,value2,value3,value4\n")
        do_nbits(wfh,  4)
        do_nbits(wfh,  8)
        do_nbits(wfh, 16)

    logger = set_up_logger("npols2tbl")
    logger.info("Saved {}".format(os.path.basename(args.tblfile)))


if __name__ == "__main__":
    main()
